import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import speech_recognition as sr
import pyttsx3
import webbrowser
import MusicLibrary
import requests
import openai 
from gtts import gTTS
import pygame
import time
import contextlib


# Initialize TTS engine and recognizer
engine = pyttsx3.init()
recognizer = sr.Recognizer()
api_key=("9ed2f3554d73476aaf92ab7d2524efd9")
    

def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    temp_file = "temp.mp3"
    tts.save(temp_file)

    # Suppress pygame welcome message
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        pygame.mixer.init()

    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    # Wait until playback finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(temp_file)

        



openai.api_key = "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"

chat_history = [
{"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses."}
    ]
def AI_process(c):
    global chat_history

    chat_history.append({"role": "user", "content": c})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_history
        )
        assistant_reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": assistant_reply})
        print(f"Jarvis: {assistant_reply}")
        speak(assistant_reply)
    except Exception as e:
        speak("Sorry, I had trouble processing that.")
        print("OpenAI Error:", e)



                    


    

def process_command(c):
    # Add real command logic here
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkdin" in c.lower():
        webbrowser.open("https://linkdin.com")
    elif c.lower().startswith("play"):
        songs= c.lower().split(" ")[1]
        link = MusicLibrary.music[songs]
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}")
        # Convert response to JSON
        data = r.json()

        # Extract and print headlines
        if data['status'] == 'ok':
            articles = data['articles']
            for  article in articles:
                speak(f"{article['title']}")
    else:
        ouput=AI_process(c)
        speak(ouput)

    

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=7)

            user_input = recognizer.recognize_google(audio)
            
            process_command(user_input)

        except sr.WaitTimeoutError:
            print("Timeout. No speech detected.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except Exception as e:
            print("Error:", e)
