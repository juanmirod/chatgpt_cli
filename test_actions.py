import pytest
from unittest.mock import patch
from actions import find_actions, run_action, wikipedia_summary, calculate, date
from datetime import datetime


class TestActions:

    @patch("wikipedia.summary",
           return_value="This is a summary of the wikipedia page")
    def test_wikipedia_summary(self, mock_wikipedia_summary):
        assert wikipedia_summary(
            "wikipedia") == "This is a summary of the wikipedia page"

    def test_calculate(self):
        assert calculate("1+1") == 2

    def test_date(self):
        assert date(
            "today") == f'today is {datetime.now().replace(second=0, microsecond=0)}'

    def test_find_actions_with_one_action(self):
        assert find_actions("ACTION: wikipedia: search term") == ("wikipedia", "search term")

    def test_find_actions_with_two_actions_returns_the_first_one(self):
        assert find_actions("ACTION: date: today\nACTION: wikipedia: search term") == ("date", "today")

    def test_find_actions_with_no_actions_returns_None(self):
        assert find_actions("Greetings!") is None

    @patch("wikipedia.summary",
           return_value="This is a summary of the wikipedia page")
    def test_run_action(self, mock_wikipedia_summary):
        assert run_action("wikipedia", "search term") == "This is a summary of the wikipedia page"
