from ..conversation_manager import ConversationManager

system = """Act as if you are a dog trainer and specialist in dogs psychology"""

ConversationManager(system=system, character="dog trainer", termination_character=None)()
