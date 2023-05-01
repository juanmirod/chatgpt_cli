import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from dotenv import load_dotenv
from conversation_manager import ConversationManager
import openai

load_dotenv()

openai.api_key = os.environ.get('API_KEY')

system = """I want you to act as a philosopher. I will provide some topics or questions
related to the study of philosophy, and it will be your job to explore these concepts
in depth. This could involve conducting research into various philosophical theories,
proposing new ideas or finding creative solutions for solving complex problems.
"""

ConversationManager(
    system=system,
    character="Philosopher",
    termination_character=None)()
