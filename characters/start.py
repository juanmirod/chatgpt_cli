import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from conversation_manager import ConversationManager

# simple prompt without functions or actions or big personality instructions
system = """Act as if you are JARVIS, the AI assistant of Tony Stark from the MCU.
You are an expert in several programming languages, including, but not only, Javascript, Python and Java."""

bot = ConversationManager(system=system, character="JARVIS*", model="gpt-4")
bot.start_chat_with_actions()
