import speech_recognition as sr
import webbrowser
import time
import sounddevice as sd
import os
import random
from gtts import gTTS
from time import ctime
import numpy as np
from pydub import AudioSegment
from urllib.parse import quote_plus

r = sr.Recognizer()

def record_audio(ask=None):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak('Sorry, I did not get that')
        except sr.RequestError:
            speak('Sorry, my speech service is down')
        return voice_data if voice_data else ''

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    mp3_file = f'audio-{r}.mp3'
    wav_file = f'audio-{r}.wav'
    
    # Save as MP3
    tts.save(mp3_file)
    
    
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format='wav')
    
    # Play WAV file using sounddevice
    audio_data = np.array(sound.get_array_of_samples())
    sd.play(audio_data, samplerate=sound.frame_rate)
    sd.wait()  # Wait until the sound has finished playing
    
    # Clean up files
    os.remove(mp3_file)
    os.remove(wav_file)

def respond(voice_data):
    if not voice_data:
        return

    if 'what is your name' in voice_data:
        speak('My name is Bhagat.')
    elif 'what time is it' in voice_data:
        speak(ctime())
    elif 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        search_encoded = quote_plus(search)
        url = f'https://google.com/search?q={search_encoded}'
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search}.')
    elif 'find location' in voice_data:
        location = record_audio('What is the location?')
        location_encoded = quote_plus(location)
        url = f'https://google.nl/maps/place/{location_encoded}/'
        webbrowser.get().open(url)
        speak(f'Here is the location of {location}.')

# Initial prompt
speak('How can I help you?')
while True:
    voice_data = record_audio()
    respond(voice_data)

