import speech_recognition as sr
import pyttsx3 as p
import subprocess
from functions import * 
import joblib
from datetime import datetime
import tkinter as tk  
import customtkinter as ctk
import threading
from PIL import Image
from datetime import datetime

engine = p.init()
rate = engine.setProperty('rate', 170)
r = sr.Recognizer()

classifier = joblib.load('saved_model/classifier_model.pkl')
vectorizer = joblib.load('saved_model/vectorizer_model.pkl')


def update_output(text):
    window.after(0, output_text.set, output_text.get() + "\n" + text)

def speak(text):
    update_output(text) 
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            update_output("You: " + text)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I could not understand the audio. Please try again.")
            return None
        except sr.RequestError as e:
            speak("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

def InformationTask():
    speak("You need information related to which topic?")
    infor = listen()
    speak("searching {} in wikipedia". format(infor))
    assist = info()     #chrome web-driver loaded
    assist.get_info(infor)  

def  PlayVideoTask():
    speak("What do you want to play?")
    user_wants_to_play = listen()
    if(user_wants_to_play != None):
        speak("playing {} on youtube". format(user_wants_to_play))
        assist = music()
        assist.play(user_wants_to_play)

def ReadNewsTask():
    speak("Here are top 5 news!")

    arr = news()
    for news_item in arr:
        speak(news_item)

def OpenNotepad():
    subprocess.Popen('notepad.exe')

def OpenCalculator():
    subprocess.Popen('calc.exe')
    
def ShowTime():
    current_time = datetime.now()
    time_12hr = current_time.strftime("%I:%M:%S %p")
    speak("It's "+time_12hr +" right now!")

def ShowDate():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    speak("Today is "+current_date)

def predictCategory(user_query):
    if user_query is not None:
        user_query = user_query.lower()  # Convert to lowercase for better matching

        new_text = user_query
        new_text_tfidf = vectorizer.transform([new_text])
        predicted_category = classifier.predict(new_text_tfidf)[0]
    return predicted_category

def handle_button_click():
    user_query = listen()
    predicted_category = predictCategory(user_query)

    category_to_function = {
        'information': InformationTask,
        'play_video': PlayVideoTask,
        'read_news': ReadNewsTask,
        'open_notepad': OpenNotepad,
        'time' : ShowTime,
        'date' :ShowDate,
        'open_calculator' : OpenCalculator,

    }

    if predicted_category in category_to_function:
        task = category_to_function[predicted_category]
        task()
    else:
        speak("Sorry, I couldn't understand your request. Please try again.")
    return

def button_click():
    threading.Thread(target=handle_button_click).start()
    

# Create the main GUI window
# window = tk.Tk()
window = ctk.CTk()
window.title("Voice Assistant")
window.geometry("1000x600")
window.wm_attributes('-topmost', True)

bg_image = ctk.CTkImage(dark_image= Image.open("image/banner.png"),size =(900,200))
banner = ctk.CTkLabel(window, text= "", image= bg_image)
banner.pack(pady=10, padx=10)

# Create output text area
output_text = ctk.StringVar()
custom_font = ("Ariel",20)
output_label = ctk.CTkLabel(window, textvariable=output_text, font = custom_font)
output_label.pack(fill=tk.BOTH, expand=True)

# Create button to activate listening
listen_button = ctk.CTkButton(window, text="Say Something", command=button_click, corner_radius=50, height = 30, width = 60)
listen_button.pack(side="bottom", padx=30, pady=30)
#btn.pack()

output_label.pack(fill=tk.BOTH, expand=True)
listen_button.pack()


def call_delayed_function():
    threading.Thread(target=speak, args=("Hello Sir, what can I do for you?",)).start()

def on_window_mapped(event):
    window.after(2000, call_delayed_function)
    window.unbind("<Map>")

window.bind("<Map>", on_window_mapped)
window.mainloop()
