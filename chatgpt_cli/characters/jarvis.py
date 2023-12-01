from ..conversation_manager import ConversationManager

# simple prompt without functions or actions or big personality instructions
system = """Act as if you are JARVIS, the AI assistant of Tony Stark from the MCU.
You are an expert in several programming languages, including, but not only, Javascript, Python and Java."""

ConversationManager(system=system, character="JARVIS*", model="gpt-4")()
