import os
import cv2
import easyocr
from gtts import gTTS
import playsound
import streamlit as st

# Function to capture an image and perform OCR
def capture_image_and_perform_ocr():
    # Set up directories to save captured images and audio
    os.makedirs('captured_images', exist_ok=True)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    st.write("This feature captures an image, performs OCR, and reads the text aloud.")

    # Button to capture an image
    if st.button('Capture Image'):
        # Initialize video capture
        cap = cv2.VideoCapture(0)  # Replace with your camera ID if needed

        if not cap.isOpened():
            st.error("Error: Could not open video stream.")
        else:
            # Capture an image from the webcam
            ret, frame = cap.read()

            if not ret:
                st.error("Error: Could not retrieve frame.")
            else:
                # Save the captured image
                image_name = 'captured_images/captured_image.jpg'
                cv2.imwrite(image_name, frame)
                st.success(f"Image captured and saved: {image_name}")

                # Display the captured image in Streamlit
                st.image(image_name, caption='Captured Image', use_column_width=True)

            # Release the video capture
            cap.release()

    # Button to perform OCR on the captured image
    if st.button('Extract Text from Image'):
        image_name = 'captured_images/captured_image.jpg'
        
        if os.path.exists(image_name):
            img = cv2.imread(image_name)

            # Perform OCR to extract text
            results = reader.readtext(img)
            extracted_text = ' '.join([result[1] for result in results])
            st.write("Extracted Text:")
            st.write(extracted_text)

            # Convert extracted text to speech and play the audio
            if extracted_text.strip():
                tts = gTTS(text=extracted_text, lang='en')
                audio_file = 'captured_images/extracted_audio.mp3'
                tts.save(audio_file)
                st.success(f"Audio saved: {audio_file}")

                try:
                    playsound.playsound(audio_file)
                    st.success("Playing extracted text as audio.")
                except Exception as e:
                    st.error(f"Error playing audio: {e}")
            else:
                st.warning("No text extracted from the image.")
        else:
            st.error("No captured image found. Please capture an image first.")
