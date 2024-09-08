import webbrowser as web
import speech_recognition as sr
import pyttsx3
import os
import pywhatkit as kit
import google.generativeai as genai
from AppOpener import open as open_app
from AppOpener import open as AppNotFoundException
import psutil

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

os.environ['API_KEY'] = 'AIzaSyBqqJfjctuOomMhs0bbf6Xl8_JXmFQUsZ8'

# Configure Google Generative AI with your API key
genai.configure(api_key=os.environ['API_KEY'])

# Initialize the generative model
model = genai.GenerativeModel()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None
        return command
    
def is_app_running(app_name):
    for proc in psutil.process_iter(['name']):
        if app_name.lower() in proc.info['name'].lower():
            return True
    return False


def open_app_or_search(app_name):
    app_name = app_name.lower()
    
    # Attempt to open the app
    open_app(app_name)
    
    # Check if the app is running after attempting to open it
    if is_app_running(app_name):
        speak(f"Opening {app_name}")
    else:
        speak(f"{app_name} not found as an application.")
        if "on youtube" in app_name:
            search_query = app_name.replace("open ", "").replace("on youtube", "").strip()
            speak(f"Searching {search_query} on YouTube")
            web.open(f"https://www.youtube.com/results?search_query={search_query}")
        else:
            speak(f"Searching {app_name} on the web")
            web.open(f"https://www.google.com/search?q={app_name}")

def handle_query(query):
   try:
    response = model.generate_content(query +" give short response")

    # Access the generated text from the response object
    generated_text = response.text
    print(generated_text)
    speak(generated_text)
   except:
       speak("Sorry, I could not generate any text for you.")

def play_song_on_youtube(song_name):
    speak(f"Playing {song_name} on YouTube")
    kit.playonyt(song_name)

def execute_command(command):
    if "open" in command:
        app_name = command.replace("open ", "").strip()
        open_app_or_search(app_name)
    elif command.startswith(("what", "who", "how", "why", "where","describe","tell me")):
        handle_query(command)
    elif "play" in command or "song" in command:
        song_name = command.replace("play", "").replace("song", "").strip()
        play_song_on_youtube(song_name)
    else:
        speak("Command not recognized. Please try again.")

def main():
    while True:
        command = get_command()
        if command != "break" or command != "Stop" or command != "Quit":
            execute_command(command)
        

if __name__ == "__main__":
    print ("/n ............................Welcome to the RoboTalk...............")
    print ("* " * 30)
    main()