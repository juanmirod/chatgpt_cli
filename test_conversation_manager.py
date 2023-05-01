import pytest
from unittest.mock import patch, mock_open, call
from conversation_manager import ConversationManager
from datetime import datetime


class TestConversationManager:
    @pytest.fixture
    def chat(self):
        return ConversationManager(
            system="Welcome!",
            character="ChatGPT",
            messages=[],
            termination_character=None)

    @patch("builtins.input", return_value="Hello!")
    def test_user_act(self, mock_input, chat):
        user_input = chat.user_act()
        assert user_input == "Hello!"
        assert len(chat.messages) == 2
        assert chat.messages[1]["role"] == "user"
        assert chat.messages[1]["content"] == "Hello!"

    @patch.object(ConversationManager, "execute", return_value="Hi there!")
    def test_assistant_act(self, mock_execute, chat):
        result = chat.assistant_act()
        assert result == "Hi there!"
        assert len(chat.messages) == 2
        assert chat.messages[1]["role"] == "assistant"
        assert chat.messages[1]["content"] == "Hi there!"

    @patch("openai.ChatCompletion.create",
           return_value={"usage": {"total_tokens": 10},
                         "choices": [{"message": {"content": "Hi!"}}]})
    def test_execute(self, mock_create, chat):
        result = chat.execute()
        assert result == "Hi!"
        assert chat.token_total == 10

    @patch("builtins.input", side_effect=["Hello!", "q"])
    @patch.object(ConversationManager, "execute", return_value="Greetings!")
    @patch.object(ConversationManager, "_get_conversation_title", return_value="Hi")
    def test_full_conversation(
            self,
            mock_input,
            mock_execute,
            mock_title,
            chat):
        with patch('builtins.open', mock_open()) as mocked_file:
            chat()

            mock_execute.assert_called_once()
            assert mocked_file.call_count == 2

            mocked_file.assert_called_with(
                f"history/Hi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", "w")
            mocked_file().write.assert_has_calls([
                call('**You:** Hello!\n\n**ChatGPT:** Greetings!'),
                call('**You:** Hello!\n\n**ChatGPT:** Greetings!\n\n**You:** q')
            ])
