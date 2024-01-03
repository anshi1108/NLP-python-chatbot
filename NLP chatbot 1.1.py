#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pyttsx3
import speech_recognition as sr
import subprocess
import re
import random
import webbrowser
import time


def txt_to_spch(words):
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(words)
    engine.runAndWait()


def spch_to_txt():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something...",end="\r")
            audio = r.listen(source, timeout=5)  # Adjust the timeout as needed
            print("Processing speech...",end="\r")
            user_input = r.recognize_google(audio).lower()
            if "link" in user_input:
                print("Please type the link...")
                txt_to_spch("Please type the link")
                user_input = input("> ").lower() 
            return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your speech.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.WaitTimeoutError:
        print("No speech detected.")
    return None


# Sample dictionary mapping app names to their executable paths
app_paths = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "camera": "explorer shell:AppsFolder\Microsoft.WindowsCamera_8wekyb3d8bbwe!App",
    "chrome": "chrome.exe",
    "mail": "https://mail.google.com/"  # Linking 'mail' command to Gmail
    # Add more app names and their corresponding executable paths here
}

# Function to open the specified app
def open_app(app_name):
    if app_name.lower() in app_paths:
        app_path = app_paths[app_name.lower()]
        if app_name.lower() == 'mail':
            webbrowser.open_new_tab(app_path)
            return f"Opening Gmail..."
        else:
            subprocess.Popen(app_path, shell=True)
            return f"Opening {app_name}..."
    else:
        return f"Sorry, I don't know how to open {app_name}."


# Function to open URL in Chrome
def open_url_in_chrome(url):
    webbrowser.open_new_tab(url)
    return f"Opening URL '{url}' in Chrome..."


# Conversation patterns
greetings_patterns = [r'(hi|hello|hey)']
how_are_you_patterns = [r'how are you\??']
help_patterns = [r'(help|support|assist|what can you do\??)']  # Modified to include regex patterns
open_app_patterns = [r'\b(notepad|calculator|camera|chrome|mail)\b']

# Responses
# Your existing code here...

# Responses
greetings_responses = ['Hello!', 'Hi there!', 'Hey!']
help_responses = ["I can help you with opening apps, opening links on Google, and more!"]
how_are_you_responses = ["I'm doing fine, thank you!", "I'm good, how about you?"]

# NLTK chatbot implementation
def nltk_chatbot():
    print("Hello! I'm your personal bot.")
    print("Say 'exit' to leave.")
    txt_to_spch("Hello! I'm your personal bot.")
    txt_to_spch("Say 'exit' to leave.")

    while True:
        user_input = spch_to_txt()  # Try speech-to-text first
        if user_input is None:  # If speech-to-text fails or is not used
            user_input = input("> ").lower()
        
        response = None  # Initialize response here

        if user_input == 'exit':# Check for exit command
            time.sleep(1)
            print("Goodbye! Hope to see you again soon!")
            txt_to_spch("Goodbye! hope to see you again soon")
            return

        if any(re.search(pattern, user_input) for pattern in greetings_patterns):
            response = random.choice(greetings_responses)
        elif any(re.search(pattern, user_input) for pattern in how_are_you_patterns):
            response = random.choice(how_are_you_responses)  # Include 'how_are_you_responses' here
        elif any(re.search(pattern, user_input) for pattern in help_patterns):
            response = random.choice(help_responses)  # Modified variable name here
        elif any(re.search(pattern, user_input) for pattern in open_app_patterns):
            app_name_match = re.search(r'\b(notepad|calculator|camera|chrome|mail)\b', user_input)
            if app_name_match:
                app_name = app_name_match.group(1)
                response = open_app(app_name)
        elif re.match(r'https?://', user_input):  # Check if input is a URL
            # Handling the URL
            response = open_url_in_chrome(user_input)
        
        if response:
            print("Bot:", response)
            txt_to_spch(response)
        else:
            print("Bot: Sorry, I didn't understand that.")
            txt_to_spch("Sorry, I didn't understand that.")

nltk_chatbot()


# In[ ]:




