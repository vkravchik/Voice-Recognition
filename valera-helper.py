import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime


cfg = {
    'alias': ('валера', 'хэлпэр', 'помошник'),
    'tbr': ('скажи', 'покажи', 'расскажи', 'сколько', 'произнеси'),
    'cmd': {
        'current_time': ('текущее время', 'который час', 'сколько сейчас времени', 'какое время'),
    }
}

# Functions

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(rec, audio):
    try:
        voice = rec.recognize_google(audio, language='ru-RU')
        print('[log] Detected: ' + voice)

        if voice.startswith(cfg['alias']):
            cmd = voice
            for x in cfg['alias']:
                cmd = cmd.replace(x, '').strip()

            for x in cfg['tbr']:
                cmd = cmd.replace(x, '').strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print('[log] Voice Error')
    except sr.RequestError as error:
        print('[log] Some other error')

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in cfg['cmd'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if (cmd == 'current_time'):
        now = datetime.datetime.now()

        speak('Сейчас ' + str(now.hour) + ':' + str(now.minute))


# Run
recognizer = sr.Recognizer()
try:
    microphone = sr.Microphone(device_index=1)
except:
    microphone = sr.Microphone(device_index=0)

with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[1].id)

speak('Привет, я готов к работе')


stop_listening = recognizer.listen_in_background(microphone, callback)
while True: time.sleep(0.1)