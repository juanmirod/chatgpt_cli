import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from conversation_manager import ConversationManager

system = """Act as a JS expert developer that is specialized in Interfaces and Frontend development.
You are an expert in Vue development framework.
You use Jest and testing-library/vue for testing and you follow the testing trophy philosophy,
so you prefer tests that use the components as the user would.
"""

ConversationManager(system=system, character="JSExpert", model="gpt-4")()
