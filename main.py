import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLib
import requests
import pygame
from gtts import gTTS
from openai import OpenAI

r = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "News_api_key"

# def speak_old(text):
#     engine.say(text)
#     engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  
        pygame.time.Clock().tick(10)  
    pygame.mixer.music.unload()
def play_song(song):
    link = musicLib.music.get(song)
    if link:
        webbrowser.open(link)
        speak(f"Playing {song}")
    
    else:
        speak(f"Sorry, I can't find {song}")
def processCommand(c):
    if("open google" in c.lower()):
        a = webbrowser.open("https://www.google.com")
        speak("Opening google")
    elif("open youtube" in c.lower()):
        webbrowser.open("https://www.youtube.com")
        speak("Opening youtube")
    elif("open facebook" in c.lower()):
        webbrowser.open("https://www.facebook.com")
        speak("Opening facebook")
    elif("open discord" in c.lower()):
        webbrowser.open("https://discord.com/app")
        speak("opening discord")
    elif ("play" in c.lower()):
        songs = c.split(" ")[1:]
        for song in songs:
            play_song(song)
    elif("news" in c.lower()):
        response = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
        data = response.json()

        titles = [article['title'] for article in data['articles']]
        for title in titles:
            speak(title)

    else:
        client = OpenAI(api_key="Openai_api_key")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant.Also give short responses"},
                {
                    "role": "user",
                    "content": c.lower()
                }
            ]
        )

        print(completion.choices[0].message.content)
        speak(completion.choices[0].message.content)

if (__name__ == "__main__"):
    speak("Initialising nova...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Nova is listening")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source , timeout=2,phrase_time_limit=1.5)
            word = r.recognize_google(audio)
            if ("nova" in word.lower()):
                speak("yup how can i help you?")
        
            with sr.Microphone() as source:
                print("nova is activated...")
                audio = r.listen(source)
            command = r.recognize_google(audio)
            processCommand(command)
        
        except Exception as e:
          print("Feel free to ask about anything")
