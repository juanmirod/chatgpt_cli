import re
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from tts import say
import actions
import assistant
from long_term_memory import LongTermMemory

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
    # The temperature to use during text generation (0.0 - 1.0) use 0.0 for more deterministic results
    temperature: float = 0.2
    # The model to use during text generation
    model: str = "gpt-3.5-turbo"
    # The width of the text output
    width: int = 100
    # The character used to terminate text generation
    termination_character: str = '*'
    # If true, the manager will try to load and recover related texts using the long term memory class
    use_long_term_memory: bool = False
    # Adds an array of function definitions that the assistant can use to return an action instead of an answer
    functions = None

    def __post_init__(self):
        self.termination_re = None
        if self.termination_character:
            self.termination_re = re.compile(
                f'.*\\{self.termination_character}$')
        self.console = Console(width=self.width, record=True)
        if self.use_long_term_memory:
            self._memory = LongTermMemory()
            self._memory.load()

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
                action, action_input = actions.find_actions(assistant_response)
                while action:
                    self._gather_observation(action, action_input)
                    assistant_response = self.assistant_act()
                    action, action_input = actions.find_actions(assistant_response)
                self._autosave()
            else:
                return

    def _gather_observation(self, action, action_input):
        self._print_system_message(f"--running {action} {action_input}")
        observation = actions.run_action(action, action_input)
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
        (result, tokens) = assistant.chat_completion(
            'You are a helpful AI assistant.',
            self.messages,
            self.temperature,
            self.model
        )
        self.token_total += tokens
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
        path = f"history/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{summary}.md"
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

    def user_act(self):
        try:
            user_input = Prompt.ask("You")
            if self.termination_re:
                while not self.termination_re.match(user_input):
                    user_input += input()
                # remove the termination character
                user_input = user_input[:-1]
            # add context from long term memory
            if self.use_long_term_memory and (self.stop_str != user_input):
                context = self._memory.recover_memories_about(user_input)
                self._print_system_message(f"Recovered context:\n {context} \n")
                user_input += f"---context\n {context} \n---"
            self.messages.append({"role": "user", "content": user_input})
        except (KeyboardInterrupt, EOFError):
            self._print_system_message('\nUser interrupted the conversation.')
            user_input = self.stop_str
        return user_input

    def assistant_act(self):
        self._print_system_message(f"waiting for response...")
        (result, tokens) = assistant.chat_completion(
            self.system,
            self.messages,
            self.temperature,
            self.model,
            self.functions
        )
        self.token_total += tokens
        self.console.print(
            f"{self.character}:" if self.character else "",
            Markdown(result),
            highlight=False,
            style=ASSISTANT_TEXT_STYLE,
            sep=""
        )
        self.messages.append({"role": "assistant", "content": result})
        if self.tts:
            say(result)
        return result
