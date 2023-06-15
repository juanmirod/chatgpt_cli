import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from conversation_manager import ConversationManager

system = """Act as a creative writer answering questions about world building."""

ConversationManager(system=system, character="Writer")()
