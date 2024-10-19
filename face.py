import os
import cv2
import torch
import pyttsx3
import speech_recognition as sr
import time

class FaceRecognitionSystem:
    def __init__(self):
        self.known_faces = {}
        self.load_known_faces()
        self.name_registered = False
        self.last_recognized_name = None
        self.last_recognition_time = time.time()
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def load_known_faces(self):
        """Load known faces from the faces directory."""
        if not os.path.exists('faces'):
            os.makedirs('faces')  # Create the directory if it doesn't exist
            print("Created 'faces' directory.")
            return

        for filename in os.listdir('faces'):
            if filename.endswith('.jpg'):
                name = filename[:-4]  # Remove the '.jpg' extension
                face_path = os.path.join('faces', filename)
                try:
                    face = cv2.imread(face_path)
                    if face is not None:
                        face_resized = cv2.resize(face, (100, 100))
                        self.known_faces[name] = face_resized
                        print(f"Loaded face for {name}.")
                    else:
                        print(f"Could not load image for {name}.")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def recognize_face(self, face):
        """Recognize the face by comparing it with stored faces."""
        if face is None:
            return None

        face_resized = cv2.resize(face, (100, 100))
        for name, stored_face in self.known_faces.items():
            difference = cv2.norm(stored_face, face_resized, cv2.NORM_L2)
            if difference < 50:  # Adjust threshold as necessary
                return name
        return None

    def greet_user(self, name):
        """Greet the recognized user."""
        greeting_message = f"Hey {name}, welcome back!"
        print(greeting_message)
        self.engine.say(greeting_message)
        self.engine.runAndWait()

    def listen_for_name(self):
        """Listen for a name from the microphone."""
        with sr.Microphone() as source:
            print("Please say your name:")
            self.engine.say("Please say your name:")
            self.engine.runAndWait()
            audio = self.recognizer.listen(source)
            try:
                name = self.recognizer.recognize_google(audio)
                print(f"You said: {name}")
                return name
            except sr.UnknownValueError:
                print("Sorry, I did not catch that.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service: {e}")
                return None

    def register_name(self, face, name):
        """Register a new name and save the face."""
        face_path = os.path.join('faces', f"{name}.jpg")
        cv2.imwrite(face_path, face)
        self.known_faces[name] = cv2.resize(face, (100, 100))
        self.engine.say(f"Nice to meet you, {name}!")
        self.engine.runAndWait()
        self.name_registered = True
        self.last_recognized_name = name
        self.last_recognition_time = time.time()

    def process_frame(self, frame, model):
        """Process each video frame for face detection and recognition."""
        try:
            results = model(frame)
            recognized_name = None

            # Process results: Filter for face (YOLO class id for face is 0)
            for *xyxy, conf, cls in results.xyxy[0]:
                if conf > 0.5 and int(cls) == 0:  # Filter only faces
                    x1, y1, x2, y2 = map(int, xyxy)
                    face = frame[y1:y2, x1:x2]

                    recognized_name = self.recognize_face(face)

                    # Greet the recognized user
                    if recognized_name:
                        # Check if we already greeted this user recently
                        if (self.last_recognized_name is None or
                                recognized_name != self.last_recognized_name or
                                (time.time() - self.last_recognition_time > 10)):
                            self.greet_user(recognized_name)
                            self.last_recognized_name = recognized_name
                            self.last_recognition_time = time.time()
                        break  # No need to continue if a face was recognized

            # Handle unknown face
            if recognized_name is None and not self.name_registered:
                if time.time() - self.last_recognition_time > 10:
                    print("No known face detected. Listening for name...")
                    name_from_speech = self.listen_for_name()
                    if name_from_speech:
                        self.register_name(face, name_from_speech)
                    else:
                        print("Failed to recognize name from speech.")

            return recognized_name

        except Exception as e:
            print(f"Error during frame processing: {e}")
            return None


def main():
    try:
        # Load YOLOv5 model
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        print("YOLOv5 model loaded successfully.")
    except Exception as e:
        print(f"Error loading YOLOv5 model: {e}")
        return

    # Initialize face recognition system
    face_recognition_system = FaceRecognitionSystem()

    try:
        # Open video capture (webcam)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video capture.")
            return
        print("Camera opened successfully.")

        # Timer to limit processing rate
        last_processed_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame.")
                break

            # Process the frame for face recognition only every 0.5 seconds
            current_time = time.time()
            if current_time - last_processed_time > 0.5:  # Limit processing to every 0.5 seconds
                face_recognition_system.process_frame(frame, model)
                last_processed_time = current_time

            # Show the frame in a window
            cv2.imshow('Face Recognition', frame)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error during video capture or processing: {e}")
    finally:
        # Release video capture and close any open windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
