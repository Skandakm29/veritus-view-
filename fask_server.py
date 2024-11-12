from flask import Flask, request
import pyttsx3
import speech_recognition as sr
import threading
import requests
import queue

app = Flask(__name__)

# Replace with your actual Gemini API key
GEMINI_API_KEY = ""

# Initialize the text-to-speech engine and queue
engine = pyttsx3.init()
speech_queue = queue.Queue()

# Function to speak the text
def speak_text(text):
    speech_queue.put(text)  # Put text into the queue

# Function to run the TTS engine in a separate thread
def run_tts():
    while True:
        text = speech_queue.get()  # Get text from the queue
        engine.say(text)
        engine.runAndWait()

# Start the TTS thread
threading.Thread(target=run_tts, daemon=True).start()

# Function for speech recognition (listens for user's input)
def listen_for_question():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question... Speak now.")
        audio = recognizer.listen(source)
        try:
            question = recognizer.recognize_google(audio)
            print(f"You said: {question}")
            return question
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Function to get a response from the Gemini API
def get_gemini_response(user_question):
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_question
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        try:
            gemini_data = response.json()
            generated_text = gemini_data['candidates'][0]['content']['parts'][0]['text']
            return generated_text
        except (KeyError, IndexError) as e:
            return f"Error parsing response: {e}. Response: {gemini_data}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to handle ESP32 button press trigger
def handle_esp32_trigger():
    print("ESP32 Trigger received! Asking for your question...")

    # Play a greeting and activate microphone
    greeting_text = "Hi, what can I help you with today?"
    speak_text(greeting_text)

    # Listen for the user's question
    user_question = listen_for_question()
    
    if user_question:
        # Get the response from the Gemini API
        gemini_response = get_gemini_response(user_question)
        print(f"Response: {gemini_response}")
        
        # Speak the response
        speak_text(gemini_response)

# Endpoint to receive trigger from ESP32
@app.route('/trigger', methods=['POST'])
def trigger():
    # Start the process to handle ESP32 trigger in a separate thread
    trigger_thread = threading.Thread(target=handle_esp32_trigger)
    trigger_thread.start()
    return "Trigger received from ESP32", 200

if __name__ == "__main__":
    # Flask will run and listen for the ESP32 trigger
    app.run(host="0.0.0.0", port=5000)
