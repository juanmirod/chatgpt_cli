from gtts import gTTS
from time import sleep
from datetime import datetime
import os
import pyglet
from pathlib import Path
from openai import OpenAI


def openai_tts(txt, voice="alloy"):
    speech_file_path = Path(__file__).parent / f"tmp/tts_{voice}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    client = OpenAI()
    response = client.audio.speech.create(model="tts-1", voice=voice, input=txt)

    response.stream_to_file(speech_file_path)
    return speech_file_path


def google_tts(txt):
    tts = gTTS(text=txt, lang='en', tld='co.uk', slow=False)
    filename = 'tmp/temp.mp3'
    tts.save(filename)
    return filename


def say(text, tts="openai"):
    filename = ""
    if tts == "google":
        filename = google_tts(text)
    elif tts == "openai":
        filename = openai_tts(text)
    try:
        music = pyglet.media.load(filename, streaming=True)
        music.play()

        sleep(music.duration)  # prevent from killing
    except Exception as e:
        print(e)
        print("Error playing audio, please try again later")
