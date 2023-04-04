import pytest
from unittest.mock import patch, mock_open
from chatgpt import ChatGPT


class TestChatGPT:
    @pytest.fixture
    def chat(self):
        return ChatGPT(system="Welcome!", character="ChatGPT", messages=[], history=[], termination_character=None)

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
        assert len(chat.history) == 2
        assert chat.history[0] == "**ChatGPT:**"
        assert chat.history[1] == "Hi there!"

    @patch("openai.ChatCompletion.create",
           return_value={"usage": {"total_tokens": 10},
                         "choices": [{"message": {"content": "Hi!"}}]})
    def test_execute(self, mock_create, chat):
        result = chat.execute()
        assert result == "Hi!"
        assert chat.token_total == 10

    @patch("builtins.input", side_effect=["Hello!", "q"])
    @patch.object(ChatGPT, "execute", return_value="Greetings!")
    @patch.object(ChatGPT, "_get_conversation_title", return_value="Hi")
    def test_full_conversation(self, mock_input, mock_execute, mock_title, chat):
        with patch('builtins.open', mock_open()) as mocked_file:
            chat()

            # assert if opened file on write mode 'w'
            mocked_file.assert_called_once()

            # assert if write(content) was called from the file opened
            # in another words, assert if the specific content was written in file
            mocked_file().write.assert_called_once_with(
                '**You:** _Hello!_\n\n**ChatGPT:**\n\nGreetings!\n\n**You:** _q_'
                )
