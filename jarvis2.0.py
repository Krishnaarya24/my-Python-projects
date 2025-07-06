import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os

engine = pyttsx3.init()

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def take_command(timeout=3):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Silence detected. Exiting...")
            return None

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
    except sr.RequestError:
        speak("There was a network error.")
    return None

def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Say 'Hey Jarvis' to wake me up.")

def handle_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "play music" in command:
        music_folder = "C:/Users/Public/Music"  # Adjust this path
        songs = os.listdir(music_folder)
        if songs:
            os.startfile(os.path.join(music_folder, songs[0]))
            speak("Playing music.")
        else:
            speak("No songs found in your music folder.")

    elif "open notepad" in command:
        os.system("notepad")
        speak("Opening Notepad.")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        return False
    return True

def run_jarvis():
    wish_user()

    # Step 1: Wake Word Only Once
    while True:
        query = take_command(timeout=5)
        if query and "hey jarvis" in query:
            speak("I am online. How can I help?")
            break

    # Step 2: Now JARVIS stays active until user is silent
    while True:
        command = take_command(timeout=3)
        if not command:
            speak("No command detected. Going offline. Goodbye.")
            break

        keep_running = handle_command(command)
        if not keep_running:
            break

if __name__ == "__main__":
    run_jarvis()
