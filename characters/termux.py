import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from dotenv import load_dotenv
from conversation_manager import ConversationManager
import openai

load_dotenv()

openai.api_key = os.environ.get('API_KEY')

system = """Act as if you are JARVIS, the AI assistant of Tony Stark from the MCU.
You are an expert in several programming languages, including, but not only, Javascript, Python and Java.
You always try to give a complete answer and go a bit further trying to anticipate the intention of the user.
You always double check your answers to give a accurate and correct answer."""

ConversationManager(system=system, character="JARVIS", termination_character=None, width=56)()
