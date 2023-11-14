from unittest.mock import patch
from assistant import chat_completion


def test_chat_completion_calls_execute_with_system_prompt_and_messages():
    with patch("assistant.execute") as mock_execute:
        mock_execute.return_value = "Hi there!"
        result = chat_completion(
            "Welcome!", [{"role": "user", "message": "Hi"}], 0.5)
        mock_execute.assert_called_once_with(
            'Welcome!', [{'role': 'user', 'message': 'Hi'}], None, 0.5, 'gpt-3.5-turbo')
        assert result == "Hi there!"


def test_chat_completion_returns_the_error_when_there_is_an_exception():
    with patch("assistant.execute") as mock_execute:
        mock_execute.side_effect = Exception("Something went wrong!")
        result = chat_completion(
            "Welcome!", [{"role": "user", "message": "Hi"}], 0.5)
        assert result == ("Something went wrong!", 0)


# def test_memorize_writes_to_file():
#     with patch("assistant.Embedding.create") as mock_embeddings:
#         mock_embeddings.return_value = {
#             "data": [{
#                 "embedding": [1, 2, 3]
#             }]
#         }
#         with patch("builtins.open", mock_open()) as mocked_file:
#             memorize("This is a test")
#             mock_embeddings.assert_called_once_with(
#                 engine="text-embedding-ada-002",
#                 input="This is a test",
#             )
#             mocked_file.assert_called_with("db/tmp_db_rows.md", "a")
#             mocked_file().write.assert_called_with('{"text": "This is a test", "embedding": [1, 2, 3]}\n')
