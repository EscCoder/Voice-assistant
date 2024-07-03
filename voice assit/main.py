import speech_recognition as sr
import pyttsx3 as p
import subprocess
from functions import *
import joblib


engine = p.init()
rate = engine.setProperty('rate', 200)
r = sr.Recognizer()


classifier = joblib.load('saved_model/classifier_model.pkl')
vectorizer = joblib.load('saved_model/vectorizer_model.pkl')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        # r.adjust_for_ambient_noise(source, 1.2)
        print("Listening.. you can speak now\nHello Sir, What can I do for you?")
        
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(text)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio. Please try again.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text

def InformationTask():
    speak("You need information related to which topic?")
    infor = listen()
    speak("searching {} in wikipedia". format(infor))
    assist = info()     #chrome web-driver loaded
    assist.get_info(infor)  

def  PlayVideoTask():
    speak("What do you want to play?")
    user_wants_to_play = listen()
    speak("playing {} on youtube". format(user_wants_to_play))
    assist = music()
    assist.play(user_wants_to_play)

def ReadNewsTask():
    speak("Here are top 5 news!")
    arr = news()
    for i in range(len(arr)):
        print(arr[i])
        speak(arr[i])


speak("Hello Sir, What can I do for you?")
user_query = listen()
user_query = user_query.lower()

new_text = user_query
new_text_tfidf = vectorizer.transform([new_text])
predicted_category = classifier.predict(new_text_tfidf)[0]

category_to_function = {
    'information': InformationTask,
    'play_video': PlayVideoTask,
    'read_news': ReadNewsTask
}
if predicted_category in category_to_function:
    task = category_to_function[predicted_category]
    task()


# elif("open" and "notepad" in user_query):
#     subprocess.Popen('notepad.exe')
# elif("open" and "calculator" in user_query):
#     subprocess.Popen('calc.exe')
# elif("open" and "file explorer" in user_query):
#     subprocess.Popen('explorer.exe')
# elif("open" and "google" in user_query):
#     subprocess.call("C://Program Files//Google//Chrome//Application//chrome.exe")
