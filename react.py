# simple implementation of the ReAct pattern, 
# for more details see https://til.simonwillison.net/llms/python-react-pattern
import os
import openai
from chatgpt import ChatGPT
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('API_KEY')   

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

Always look things up on Wikipedia if you have the opportunity to do so.
Always try to use calculate to get the result of arithmetic operations. 

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()


bot = ChatGPT(system=prompt, character="JARVIS*", user_start=False)
bot.start_chat_with_actions()