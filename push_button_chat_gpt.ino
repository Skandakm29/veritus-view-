#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "";
const char* password = "";

// Replace with your Flask server's IP address and port
String serverUrl = "http://192.168.51.xxx:5000/trigger";

// Microphone pin (adjust according to your wiring)
int micPin = 34;  // Example for analog microphone input
int buttonPin = 12;  // GPIO pin for button

void setup() {
  Serial.begin(115200);

  // Initialize microphone pin
  pinMode(micPin, INPUT);

  // Initialize button pin with internal pull-up
  pinMode(buttonPin, INPUT_PULLUP);  // Button pressed state will be LOW

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");
}

void loop() {
  // Read from microphone
  int micValue = analogRead(micPin);

  // Check if button is pressed (LOW state)
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("Button pressed!");
    sendTriggerToServer();
    delay(2000);  // Debounce delay to prevent multiple triggers
  }

  // Check if microphone detects sound (threshold can be adjusted)
  if (micValue > 500) {  // Example threshold
    Serial.println("Sound detected!");
    sendTriggerToServer();
    delay(2000);  // Avoid sending multiple requests rapidly
  }
}

void sendTriggerToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST("{}");  // Send empty JSON payload

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.println("Error sending POST request");
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}
