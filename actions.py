import wikipedia
import warnings
from datetime import datetime

wikipedia.set_lang("en")

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

known_actions = {
    "wikipedia": wikipedia_summary,
    "calculate": calculate,
    "date": date,
}
