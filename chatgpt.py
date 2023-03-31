import openai
import wikipedia
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from tts import say
import warnings

action_re = re.compile('^Action: (\\w+): (.*)$')
wikipedia.set_lang("en")


def wikipedia_summary(q):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            text = wikipedia.summary(q, sentences=5)
        except wikipedia.exceptions.DisambiguationError as e:
            # if there are several pages for that string, pick the first
            # suggestion
            text = wikipedia.summary(e.options[0], sentences=5)
    return text


def calculate(exp):
    return eval(exp)


known_actions = {
    "wikipedia": wikipedia_summary,
    "calculate": calculate,
}


@dataclass
class ChatGPT:
    system: str = None
    character: str = ""
    history = []
    stop_str: str = "q"
    tts: bool = False
    messages: List[dict] = field(default_factory=list)
    token_total: int = 0
    user_start: bool = True
    temperature: float = 1.0
    termination_character: str = '*'

    def __post_init__(self):
        self.termination_re = None
        if self.termination_character:
            self.termination_re = re.compile(
                f'.*\\{self.termination_character}$')
        self.console = Console(width=80, record=True)
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self):
        self._print_connected_message()
        self._start_chat()
        self._print_disconnected_message()
        self._save_chat_history()

    def _start_chat(self):
        user_input = ""
        while self.stop_str != user_input:
            user_input = self.user_act()
            if (self.stop_str != user_input):
                self.assistant_act()

    def start_chat_with_actions(self):
        self._print_connected_message()
        self._chat_with_actions_loop()
        self._print_disconnected_message()
        self._save_chat_history()

    def _find_actions(self, text):
        """
        Returns a list of known actions found in the given text
        """
        return [action_re.match(a)
                for a in text.split('\n') if action_re.match(a)]

    def _run_action(self, action, action_input):
        """
        Runs the given action with the provided input
        """
        if action not in known_actions:
            raise Exception(
                "Unknown action: {}: {}".format(
                    action, action_input))
        self.console.print(
            f"--running {action} {action_input}",
            highlight=False,
            style="italic dark_green",
        )
        observation = known_actions[action](action_input)
        next_prompt = f"--Observation: {observation}"
        self.console.print(
            next_prompt,
            highlight=False,
            style="italic dark_green",
        )
        self.messages.append({"role": "user", "content": next_prompt})

    def _chat_with_actions(self):
        """
        Runs a chat loop with actions until the stop string is entered 
        by the user
        """
        user_input = ""
        while self.stop_str != user_input:
            user_input = self.user_act()
            if self.stop_str != user_input:
                assistant_response = self.assistant_act()
                actions = self._find_actions(assistant_response)
                while actions:
                    action, action_input = actions[0].groups()
                    self._run_action(action, action_input)
                    assistant_response = self.assistant_act()
                    actions = self._find_actions(assistant_response)
            else:
                return

    def _print_system_message(self, msg):
        self.console.print(msg, highlight=False, style="italic dark_green")

    def _print_connected_message(self):
        self._print_system_message(f"{self.character} is connected...")

    def _print_disconnected_message(self):
        self._print_system_message(
            f"{self.character} has left the chat room.\n{self.token_total:,} total ChatGPT tokens used."
        )

    def _get_conversation_summary(self):
        self._print_system_message(f"Getting conversation summary...")
        self.messages.append({
            "role": "user",
            "content": 'Make a summary of the conversation in a short sentence, 5 words maximum.'
        })
        result = self.execute()
        return re.sub(r'[^\w]', '_', result)

    def _save_chat_history(self):
        summary = self._get_conversation_summary()
        with open(f"history/{summary}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "w") as file:
            file.write('\n\n'.join(self.history))

    def user_act(self, user_input=None):
        if not user_input:
            user_input = Prompt.ask("You")
            while self.termination_re and not self.termination_re.match(
                    user_input):
                new_line = input()
                user_input = user_input + new_line
            if self.termination_re:
                # remove the termination character
                user_input = user_input[:-1]
        self.messages.append({"role": "user", "content": user_input})
        self.history.append(f"**You:** _{user_input}_")
        return user_input

    def assistant_act(self):
        self._print_system_message(f"Sending request...")
        result = self.execute()
        self.history.append(f"**{self.character}:**" if self.character else "")
        self.history.append(result)
        self.console.print(
            f"{self.character}:" if self.character else "",
            Markdown(result),
            highlight=False,
            style="bright_green",
            sep=""
        )
        self.messages.append({"role": "assistant", "content": result})
        if self.tts:
            say(result)
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=self.temperature)
        self.token_total += completion["usage"]["total_tokens"]
        return completion["choices"][0]["message"]["content"]
