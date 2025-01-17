import cv2
from paddleocr import PaddleOCR
from gtts import gTTS
import pygame
import os
import numpy as np

# Initialize PaddleOCR for English
ocr_english = PaddleOCR(use_angle_cls=True, lang='en', drop_score=0.7)  # English OCR with high accuracy filtering
esp_32="http://192.168.13.161:81/stream"
# Initialize video capture
cap = cv2.VideoCapture(esp_32)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Initialize pygame mixer
pygame.mixer.init()

print("Press 'q' to quit the application.")

frame_counter = 0  # To manage frame skipping for real-time performance
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Convert the frame to grayscale for pre-processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_frame = clahe.apply(gray_frame)

    # Adaptive thresholding with fine-tuned parameters
    adaptive_thresh = cv2.adaptiveThreshold(
        clahe_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

    # Apply Morphological Transformations to remove noise and enhance text regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    adaptive_thresh = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    # Optional: Combine with Otsu's Binarization
    _, otsu_thresh = cv2.threshold(clahe_frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    combined_thresh = cv2.bitwise_or(adaptive_thresh, otsu_thresh)

    # Convert the original frame to RGB (PaddleOCR requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Skip frames to optimize performance
    if frame_counter % 5 == 0:  # Process every 5th frame
        # Perform OCR for English
        results_english = ocr_english.ocr(rgb_frame, cls=True)

        # Process detected English text
        if results_english and results_english[0]:
            extracted_text_en = ' '.join([result[1][0] for result in results_english[0]])
            print("Detected English Text:", extracted_text_en)

            # Convert English text to speech
            if extracted_text_en.strip():
                tts = gTTS(text=extracted_text_en, lang='en')
                audio_file_en = "temp_audio_en.mp3"
                tts.save(audio_file_en)

                pygame.mixer.music.load(audio_file_en)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    continue

                if os.path.exists(audio_file_en):
                    os.remove(audio_file_en)

    # Display the processed video feed
    cv2.imshow("Live Camera Feed - Press 'q' to Quit", combined_thresh)

    frame_counter += 1

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
