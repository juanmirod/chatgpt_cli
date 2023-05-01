import openai
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from tts import say
from actions import find_actions, run_action
import assistant

SYSTEM_TEXT_STYLE = "italic yellow"
ASSISTANT_TEXT_STYLE = "cyan"


@dataclass
class ConversationManager:
    # The system prompt
    system: str = None
    # The name of the character
    character: str = "ChatGPT"
    # the stop string to end the conversation by the user
    stop_str: str = "q"
    # Whether or not to use text-to-speech
    tts: bool = False
    # The list of messages in the conversation
    messages: List[dict] = field(default_factory=list)
    # The total number of tokens used during the conversation
    token_total: int = 0
    # The temperature to use during text generation
    temperature: float = 0.5
    # The width of the text output
    width: int = 100
    # The character used to terminate text generation
    termination_character: str = '*'

    def __post_init__(self):
        self.termination_re = None
        if self.termination_character:
            self.termination_re = re.compile(
                f'.*\\{self.termination_character}$')
        self.console = Console(width=self.width, record=True)

    def __call__(self):
        # if self.conversation:
        #     self.messages = load_conversation(self.conversation)
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
                self._autosave()

    def start_chat_with_actions(self):
        self._print_connected_message()
        self._chat_with_actions()
        self._print_disconnected_message()
        self._save_chat_history()

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
                actions = find_actions(assistant_response)
                while actions:
                    self._gather_observation(actions)
                    assistant_response = self.assistant_act()
                    actions = find_actions(assistant_response)
                self._autosave()
            else:
                return

    def _gather_observation(self, actions):
        action, action_input = actions
        self._print_system_message(f"--running {action} {action_input}")
        observation = run_action(action, action_input)
        next_prompt = f"OBSERVATION: {observation}"
        self._print_system_message(next_prompt)
        self.messages.append({"role": "user", "content": next_prompt})

    def _print_system_message(self, msg):
        self.console.print(msg, highlight=False, style=SYSTEM_TEXT_STYLE)

    def _print_connected_message(self):
        self._print_system_message(f"{self.character} is connected...")

    def _print_disconnected_message(self):
        self._print_system_message(
            f"{self.character} has left the chat room.\n{self.token_total:,} total ChatGPT tokens used."
        )

    def _get_conversation_title(self):
        self._print_system_message(f"Getting conversation summary...")
        self.messages.append({
            "role": "user",
            "content": 'Make a summary of the conversation in 5 words or less.'
        })
        try:
            result = self.execute()
        except Exception as e:
            result = 'No summary'
        return re.sub(r'[^\w]', '_', result)

    def _autosave(self):
        """
        Save the conversation always to the same file, this is intended to be used as failsafe
        or as a way to copy code from the conversation file instead of directly from the
        command line that has more formatting.
        """
        path = f"history/current.md"
        with open(path, "w") as file:
            file.write(self._messages_to_text())

    def _save_chat_history(self):
        summary = self._get_conversation_title()
        path = f"history/{summary}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(path, "w") as file:
            file.write(self._messages_to_text())

    def _messages_to_text(self):
        messages = filter(lambda msg: msg['role'] != 'system', self.messages)
        return '\n\n'.join(map(
            lambda msg: f"**{self._get_role_name(msg['role'])}:** {msg['content']}", messages))

    def _get_role_name(self, role):
        if role == 'user':
            return 'You'
        return self.character

    def user_act(self, user_input=None):
        if not user_input:
            try:
                user_input = Prompt.ask("You")
                while self.termination_re and not self.termination_re.match(
                        user_input):
                    new_line = input()
                    user_input = user_input + new_line
                if self.termination_re:
                    # remove the termination character
                    user_input = user_input[:-1]
                self.messages.append({"role": "user", "content": user_input})
            except (KeyboardInterrupt, EOFError):
                self._print_system_message(
                    '\nUser interrupted the conversation.')
                user_input = self.stop_str
        return user_input

    def assistant_act(self):
        self._print_system_message(f"waiting for response...")
        result = assistant.chat_completion(self.system, self.messages, self.temperature)
        self.token_total += result[1]
        self.console.print(
            f"{self.character}:" if self.character else "",
            Markdown(result[0]),
            highlight=False,
            style=ASSISTANT_TEXT_STYLE,
            sep=""
        )
        self.messages.append({"role": "assistant", "content": result[0]})
        if self.tts:
            say(result[0])
        return result[0]
