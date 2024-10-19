import os
import json
import requests
import speech_recognition as sr
import pyttsx3  # Import pyttsx3 for text-to-speech
import threading
from flask import Flask, jsonify, request
import streamlit as st

# Set your Gemini API key here
GEMINI_API_KEY = ""  # Add your Gemini API key

# Initialize Flask app
app = Flask(__name__)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

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
            # Remove any asterisks or unwanted symbols in the response
            clean_text = generated_text.replace("*", "")
            return clean_text
        except (KeyError, IndexError) as e:
            return f"Error parsing response: {e}. Response: {gemini_data}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to handle audio input from the microphone
def listen_for_question():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question...")
        audio = recognizer.listen(source)
        try:
            question = recognizer.recognize_google(audio)
            print(f"You said: {question}")
            return question
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Function to convert text to speech and play it in a separate thread
def speak_text(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()

    speech_thread = threading.Thread(target=run_speech)
    speech_thread.start()

# Flask API endpoint to listen for a user's question and respond via Gemini API
@app.route('/ask', methods=['GET'])
def ask():
    user_question = listen_for_question()  # Listen for the user's question
    if user_question:
        gemini_response = get_gemini_response(user_question)  # Get response from the Gemini API
        print(f"Response: {gemini_response}")  # Print response to the console
        speak_text(gemini_response)  # Speak the response
        return jsonify({"recognized_text": user_question, "response": gemini_response})
    return jsonify({"error": "No question recognized."}), 400

# Flask API endpoint to trigger the question-asking process, e.g., from ESP32
@app.route('/trigger', methods=['POST'])
def trigger():
    print("ESP32 Trigger received! Asking for your question...")
    return ask()  # Call the ask function to handle the question

# Streamlit frontend to interact with Flask API
def run_streamlit_app():
    st.title("Gemini API with Voice Interaction")

    # URL of the Flask server (local IP address for ESP32)
    flask_server_url = 'http://192.168.181.217:5000'

    # Button to trigger the voice-based question asking
    if st.button('Ask a Question via Voice'):
        # Send request to the Flask /ask endpoint
        st.write("Listening for your question via Flask...")
        response = requests.get(f'{flask_server_url}/ask')
        
        if response.status_code == 200:
            result = response.json()
            st.write(f"Recognized Text: {result['recognized_text']}")
            st.write(f"Gemini Response: {result['response']}")
        else:
            st.write("Error communicating with Flask API")

    # Display URL for ESP32 to send the POST request
    st.write(f"ESP32 should send POST requests to: {flask_server_url}/trigger")
    st.write(f"Flask Server URL: {flask_server_url}")

# Flask entry point
if __name__ == '__main__':
    # Launch Flask and Streamlit concurrently
    threading.Thread(target=lambda: app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)).start()  # Disable the reloader
    run_streamlit_app()  # Run Streamlit app
