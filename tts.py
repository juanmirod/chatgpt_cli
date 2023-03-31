from gtts import gTTS
from time import sleep
import os
import pyglet


def say(txt):
    tts = gTTS(text=txt, lang='en', tld='co.uk')
    filename = '/tmp/temp.mp3'
    tts.save(filename)

    music = pyglet.media.load(filename, streaming=False)
    music.play()

    sleep(music.duration)  # prevent from killing
    os.remove(filename)  # remove temperory file
