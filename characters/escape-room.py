from dotenv import load_dotenv
from chatgpt import ChatGPT
import os
import openai
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

load_dotenv()

openai.api_key = os.environ.get('API_KEY')

system = """Act as the narrator of a escape room, first you have to set the scene and then the user will
ask questions to try to solve the puzzles and escape the room. But before starting the game please write
a list of the rooms in the game and a brief description of the setting, a bullet point list of all the 
puzzles and how to solve them. This won't be seen by the user, it will only be stored for reviewing the 
game afterwards and evaluating it. So please write that when I say to you "SUMMARY" and I when 
I say to you "START" you can set the scene for the user because that will be the first test they will see. 
After that the user will talk with you instead of me.
"""

ChatGPT(
    system=system,
    character="Narrator",
    user_start=False,
    termination_character=None)()
