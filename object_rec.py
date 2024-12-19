import cv2
import torch

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open ESP32-CAM stream
stream_url = "http://192.168.x.x/stream"  # Replace with your ESP32-CAM IP address
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open camera stream. Check the URL or camera connection.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read from the camera. Retrying...")
        continue

    # Convert frame to RGB
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform object detection
    results = model(img)

    # Render the results
    results.render()

    # Convert back to BGR for display
    output_img = cv2.cvtColor(results.ims[0], cv2.COLOR_RGB2BGR)

    # Display the frame
    cv2.imshow("YOLOv5 Object Detection", output_img)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()