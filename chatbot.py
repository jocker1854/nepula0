import json
import random

with open('intents2.json', 'r') as file:
    intents = json.load(file)['intents']

X = []  # Input patterns
y = []  # Intent tags

for intent in intents:
    for pattern in intent['patterns']:
        X.append(pattern)
        y.append(intent['tag'])

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB()
classifier.fit(X, y)

def chatbot_response(user_input):
    user_input_vectorized = vectorizer.transform([user_input])
    intent = classifier.predict(user_input_vectorized)[0]
    for intent_data in intents:
        if intent_data['tag'] == intent:
            responses = intent_data['responses']
            return random.choice(responses)
    return "I'm not sure how to respond to that."

import random
from gtts import gTTS
import os
import speech_recognition as sr

def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')
    # Save the converted speech to a file (you can use different file formats like 'mp3', 'wav', etc.)
    tts.save("output.mp3")
    # Play the converted speech (using a command-line player)
    os.system("mpg123 output.mp3")  # Install 'mpg123' if not already installed


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

while True:
    #user_input = input("You: ")
    user_input = speech_to_text()
    if user_input.lower() == 'exit':
        break
    response = chatbot_response(user_input)
    print("Chatbot:", response)
    text_to_speech(response)
