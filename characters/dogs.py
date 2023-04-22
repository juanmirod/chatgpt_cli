from chatgpt import ChatGPT
import os
import openai
from dotenv import load_dotenv
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

load_dotenv()

openai.api_key = os.environ.get('API_KEY')

system = """Act as if you are a dog trainer and specialist in dogs psychology"""

ChatGPT(system=system, character="dog trainer",
        user_start=False, termination_character=None)()
