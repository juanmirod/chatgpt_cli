import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from chatgpt import ChatGPT
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('API_KEY')

system = """Act as if you are a dog trainer and specialist in dogs psychology"""

ChatGPT(system=system, character="dog trainer",
        user_start=False, termination_character=None)()
