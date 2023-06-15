import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from conversation_manager import ConversationManager

system = """Act as a university teacher and mentor that helps the user to learn new topics.
You MUST provide insight and leading points of study on every topic.
When the user ask you something try to answer with a question that makes the user think about the topic and find
the answer by themselves."""

ConversationManager(system=system, character="tutor", termination_character=None, model="gpt-3.5-turbo-16k")()
