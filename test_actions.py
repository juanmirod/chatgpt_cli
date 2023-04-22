import pytest
from unittest.mock import patch
from actions import known_actions, wikipedia_summary, calculate, date
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
