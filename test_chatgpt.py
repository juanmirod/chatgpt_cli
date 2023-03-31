import pytest
from unittest.mock import patch
from chatgpt import ChatGPT


class TestChatGPT:
    @pytest.fixture
    def chat(self):
        return ChatGPT(system="Welcome!", character="ChatGPT")

    @patch("builtins.input", return_value="Hello!")
    def test_user_act(self, mock_input, chat):
        user_input = chat.user_act()
        assert user_input == "Hello!"
        assert len(chat.messages) == 2
        assert chat.messages[1]["role"] == "user"
        assert chat.messages[1]["content"] == "Hello!"
        assert len(chat.history) == 1
        assert chat.history[0] == "**You:** _Hello!_"

    @patch.object(ChatGPT, "execute", return_value="Hi there!")
    def test_assistant_act(self, mock_execute, chat):
        result = chat.assistant_act()
        assert result == "Hi there!"
        assert len(chat.messages) == 2
        assert chat.messages[1]["role"] == "assistant"
        assert chat.messages[1]["content"] == "Hi there!"
        assert len(chat.history) == 3
        assert chat.history[1] == "**ChatGPT:**"
        assert chat.history[2] == "Hi there!"

    @patch("openai.ChatCompletion.create",
           return_value={"usage": {"total_tokens": 10},
                         "choices": [{"message": {"content": "Hi!"}}]})
    def test_execute(self, mock_create):
        chat = ChatGPT()
        result = chat.execute()
        assert result == "Hi!"
        assert chat.token_total == 10
