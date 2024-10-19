import os
import json
import requests
from flask import Flask, jsonify, request
import pyttsx3

app = Flask(__name__)

# Set your Gemini API key here
GEMINI_API_KEY = 'AIzaSyDxyGj1rtHHqp3YkDpQFn4YVg9e_2V0T8s'  # Replace with your actual Gemini API key

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to get a response from the Gemini API
def get_gemini_response(data):
    headers = {
        "Content-Type": "application/json",
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

# Function to convert text to speech and play it
def speak_text(text):
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Wait until the speech is finished

# Endpoint to handle GPS requests and ask "Where am I?" to Gemini API
@app.route('/gps', methods=['POST'])
def gps():
    gps_data = request.json  # Expecting GPS data in JSON format from the ESP32
    latitude = gps_data.get('latitude')
    longitude = gps_data.get('longitude')

    if latitude and longitude:
        print(f"Received GPS coordinates: Latitude={latitude}, Longitude={longitude}")
        location_question = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"My coordinates are Latitude: {latitude}, Longitude: {longitude}. Where am I?"
                        }
                    ]
                }
            ]
        }
        gemini_response = get_gemini_response(location_question)  # Send to Gemini API
        print(f"Response from Gemini: {gemini_response}")
        speak_text(gemini_response)  # Speak the response
        return jsonify({"question": location_question["contents"][0]["parts"][0]["text"], "response": gemini_response})
    return jsonify({"error": "Invalid GPS data received."}), 400

# Endpoint to handle general user questions
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')  # Expecting a question in JSON format

    if user_question:
        print(f"Received question: {user_question}")
        question_data = {
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
        gemini_response = get_gemini_response(question_data)  # Send to Gemini API
        print(f"Response from Gemini: {gemini_response}")
        speak_text(gemini_response)  # Speak the response
        return jsonify({"question": user_question, "response": gemini_response})
    return jsonify({"error": "No question provided."}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
