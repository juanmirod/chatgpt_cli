import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from chatgpt import ChatGPT
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('API_KEY')

system = """Act as a university teacher and mentor
that helps the user to learn new topics. You must
provide insight and leading points of study on
every topic and when the user ask you something try
to use the socratic method to encourage the user to
find the answer himself."""

ChatGPT(system=system, character="tutor", termination_character=None)()
