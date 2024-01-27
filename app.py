import speech_recognition as sr
import os
from gtts import gTTS

def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')
    # Save the converted speech to a file (you can use different file formats like 'mp3', 'wav', etc.)
    tts.save("temp.mp3")
    os.system("mpg123 -q temp.mp3")  # Requires mpg123 to be installed

    # Remove the temporary file
    os.remove("temp.mp3")


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as audio:
        print('Listening...')
        r.pause_threshold = 1
        voice = r.listen(audio,timeout=10,phrase_time_limit=5)
    try:
        print("Recognizing..")
        text = r.recognize_google(voice)  # Use Google Web Speech API
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        # Handle network-related errors (e.g., poor internet connection)
        return f"Request error: {str(e)}"
    except Exception as e:
        # Handle other unexpected exceptions
        return f"An error occurred: {str(e)}"


