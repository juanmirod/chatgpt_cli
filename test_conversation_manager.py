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
        assert len(chat.messages) == 1
        assert chat.messages[0]["role"] == "user"
        assert chat.messages[0]["content"] == "Hello!"
        mock_input.assert_called_once()

    @patch("assistant.chat_completion", return_value=("Hi there!", 100))
    def test_assistant_act(self, mock_chat_completion, chat):
        result = chat.assistant_act()
        mock_chat_completion.assert_called_once()
        assert result == "Hi there!"
        assert len(chat.messages) == 1
        assert chat.messages[0]["role"] == "assistant"
        assert chat.messages[0]["content"] == "Hi there!"

    @patch("builtins.input", side_effect=["Hello!", "q"])
    @patch("assistant.chat_completion", return_value=("Greetings!", 100))
    @patch.object(ConversationManager, "_get_conversation_title", return_value="Hi")
    def test_full_conversation(
            self,
            mock_input,
            mock_chat_completion,
            mock_title,
            chat):
        with patch('builtins.open', mock_open()) as mocked_file:
            chat()

            mock_chat_completion.assert_called_once()
            assert mocked_file.call_count == 2

            mocked_file.assert_called_with(
                f"history/{datetime.now().strftime('%Y%m%d_%H%M%S')}_Hi.md", "w")
            mocked_file().write.assert_has_calls([
                call('**You:** Hello!\n\n**ChatGPT:** Greetings!'),
                call('**You:** Hello!\n\n**ChatGPT:** Greetings!\n\n**You:** q')
            ])


class TestConversationManagerWithActions:
    @pytest.fixture
    def chat(self):
        return ConversationManager(
            system="Welcome!",
            character="ChatGPT",
            messages=[],
            termination_character=None)

    @patch("builtins.input", side_effect=["Who is Barak Obama?", "q"])
    @patch("assistant.chat_completion", side_effect=[
        ("ACTION: wikipedia: Barak Obama", 100),
        ("I checked and Barak Obama is the 44th president of the United States.", 100),
    ])
    @patch.object(ConversationManager, "_get_conversation_title", return_value="Hi")
    @patch("actions.run_action", return_value=("", "Barak Obama is the 44th president of the United States."))
    def test_full_conversation_with_actions(
            self,
            mock_run_action,
            mock_chat_completion,
            mock_title,
            mock_input,
            chat):
        with patch('builtins.open', mock_open()) as mocked_file:
            chat.start_chat_with_actions()

            mock_run_action.assert_called_once_with("wikipedia", "Barak Obama")
            mock_chat_completion.assert_called_once()
            assert mock_input.call_count == 2
            assert mocked_file.call_count == 2
            mocked_file.assert_called_with(
                f"history/{datetime.now().strftime('%Y%m%d_%H%M%S')}_Hi.md", "w")
            mocked_file().write.assert_has_calls([
                call('**You:** Who is Barak Obama?\n\n**ChatGPT:** ACTION: wikipedia: Barak Obama\n\n'
                     '**You:** OBSERVATION: Barak Obama is the 44th president of the United States.\n\n'
                     '**ChatGPT:** I checked and Barak Obama is the 44th president of the United States.'),
                call('**You:** Who is Barak Obama?\n\n**ChatGPT:** ACTION: wikipedia: Barak Obama\n\n'
                     '**You:** OBSERVATION: Barak Obama is the 44th president of the United States.\n\n'
                     '**ChatGPT:** I checked and Barak Obama is the 44th president of the United States.\n\n'
                     '**You:** q')
            ])
