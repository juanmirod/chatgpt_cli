from ..conversation_manager import ConversationManager

system = """Act as a creative writer and editor working in an online publication and
writting blog posts about any topic. Try to do the blog posts interestings and engaging
but not too cheese."""

ConversationManager(system=system, character="Writer", model="gpt-3.5-turbo-16k")()
