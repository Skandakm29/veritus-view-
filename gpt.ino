#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your WiFi credentials
const char* ssid = "";
const char* password = "";

// Server URL
String serverURL = "http://192.168.51.xxx:5000/process-audio";  // Replace with your server IP and port

// Microphone pin
const int micPin = 34;  // GPIO pin connected to the microphone
const int bufferSize = 1024;  // Audio buffer size

// Function to connect to WiFi
void connectToWiFi() {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
}

// Function to capture audio from the microphone
String captureAudio() {
    String audioData = "";

    // Capture audio from microphone
    for (int i = 0; i < bufferSize; i++) {
        int micValue = analogRead(micPin);  // Read microphone input
        audioData += String(micValue) + ",";  // Append audio values as comma-separated string
        delay(1);  // Adjust delay for sampling rate
    }
    
    return audioData;
}

// Function to send audio to the server
void sendToServer(String audioData) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverURL);  // Specify server URL
        http.addHeader("Content-Type", "application/json");  // Sending JSON data
        
        String jsonPayload = "{\"audio\": \"" + audioData + "\"}";  // Create JSON with audio data
        
        int httpResponseCode = http.POST(jsonPayload);  // Send the POST request
        String response = http.getString();  // Get the response
        http.end();

        if (httpResponseCode == 200) {
            Serial.println("Server response: " + response);  // Print the response
        } else {
            Serial.println("Error: " + String(httpResponseCode));  // Print the error
        }
    } else {
        Serial.println("WiFi Disconnected");
    }
}

void setup() {
    Serial.begin(115200);
    connectToWiFi();  // Connect to WiFi
}

void loop() {
    // Capture audio from the microphone
    String audioData = captureAudio();
    
    // Send the audio data to the server
    sendToServer(audioData);
    
    delay(5000);  // Wait 5 seconds before next capture
}
