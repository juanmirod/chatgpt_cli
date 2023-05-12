from unittest.mock import patch, mock_open
from assistant import chat_completion, memorize


def test_chat_completion_calls_openai_with_system_prompt_and_messages():
    with patch("assistant.ChatCompletion.create") as mock_chat_completion:
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
    with patch("assistant.ChatCompletion.create") as mock_chat_completion:
        mock_chat_completion.side_effect = Exception("Something went wrong!")
        result = chat_completion("Welcome!", [{"role": "user", "message": "Hi"}], 0.5)
        assert result == ("Something went wrong!", 0)


def test_memorize_calculates_embeddings_and_stores_them_in_a_file():
    with patch("assistant.Embedding.create") as mock_embeddings:
        mock_embeddings.return_value = {
            "data": [{
                "embedding": [1, 2, 3]
            }]
        }
        with patch("builtins.open", mock_open()) as mocked_file:
            memorize("This is a test")
            mock_embeddings.assert_called_once_with(
                engine="text-embedding-ada-002",
                input="This is a test",
            )
            mocked_file.assert_called_with("memories/db", "a")
            mocked_file().write.assert_called_with('{"text": "This is a test", "embedding": [1, 2, 3]}\n')
