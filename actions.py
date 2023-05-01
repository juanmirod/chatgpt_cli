import wikipedia
import warnings
import re
from datetime import datetime
from imagine import imagine

wikipedia.set_lang("en")
action_re = re.compile('^ACTION: (\\w+): (.*)$')


def wikipedia_summary(q):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            text = wikipedia.summary(q, sentences=5)
        except wikipedia.exceptions.DisambiguationError as e:
            # if there are several pages for that string, pick the first
            # suggestion
            text = wikipedia.summary(e.options[0], sentences=5)
    return text


def calculate(exp):
    return eval(exp)


def date(when):
    return f'today is {datetime.now().replace(second=0, microsecond=0)}'


def find_actions(text):
    """
    Returns a list of known actions found in the given text
    """
    actions = [action_re.match(a) for a in text.split('\n') if action_re.match(a)]
    return actions[0].groups() if actions else None


def run_action(action, action_input):
    """
    Runs the given action with the provided input
    """
    if action not in known_actions:
        raise Exception("Unknown action: {}: {}".format(action, action_input))
    return known_actions[action](action_input)


known_actions = {
    "wikipedia": wikipedia_summary,
    "calculate": calculate,
    "date": date,
    "imagine": imagine,
}
