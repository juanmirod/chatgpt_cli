import openai
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from datetime import datetime
from typing import List
from dataclasses import dataclass, field

@dataclass
class ChatGPT:
    system: str = None
    character: str = ""
    history = []
    stop_str: str = "q"
    messages: List[dict] = field(default_factory=list)
    token_total: int = 0
    user_start: bool = True
    temperature: float = 1.0

    def __post_init__(self):
        self.console = Console(width=80, record=True)
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self):
        self.console.print(
            f"{self.character} is connected...",
            highlight=False,
            style="italic dark_green",
        )

        user_input = ""
        while self.stop_str != user_input:
            user_input = self.user_act()
            if(self.stop_str != user_input):
                self.assistant_act()

        self.console.print(
            f"{self.character} has left the chat room.\n{self.token_total:,} total ChatGPT tokens used.",
            highlight=False,
            style="italic",
        )
        with open(f"history/chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "w") as file:                                           
            file.write('\n\n'.join(self.history)) 
    
    def user_act(self, user_input=None):
        if not user_input:
            user_input = Prompt.ask("You")
        self.messages.append({"role": "user", "content": user_input})
        self.history.append(f"**You:** _{user_input}_")
        return user_input

    def assistant_act(self):
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
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages, temperature=self.temperature
        )
        self.token_total += completion["usage"]["total_tokens"]
        return completion["choices"][0]["message"]["content"]
