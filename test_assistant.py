from unittest.mock import patch, call
from assistant import chat_completion


def test_chat_completion_calls_openai_with_system_prompt_and_messages():
    with patch("assistant.openai.ChatCompletion.create") as mock_chat_completion:
        mock_chat_completion.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Hi there!"
                    }
                }
            ],
            "usage": {
                "total_tokens": 100
            }
        }
        result = chat_completion("Welcome!", [{"role": "user", "message": "Hi"}], 0.5)
        mock_chat_completion.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Welcome!"}, {"role": "user", "message": "Hi"}],
            temperature=0.5
        )
        assert result == ("Hi there!", 100)


def test_chat_completion_returns_the_error_when_there_is_an_exception():
    with patch("assistant.openai.ChatCompletion.create") as mock_chat_completion:
        mock_chat_completion.side_effect = Exception("Something went wrong!")
        result = chat_completion("Welcome!", [{"role": "user", "message": "Hi"}], 0.5)
        assert result == ("Something went wrong!", 0)
