import streamlit as st
import cv2
import mediapipe as mp
import os
import subprocess
import sys
import keyboard

# Create "images" directory if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

mp_face_detection = mp.solutions.face_detection

def draw_frame(img, box_size=300):
    height, width = img.shape[:2]
    left = (width - box_size) // 2
    top = (height - box_size) // 2
    right = left + box_size
    bottom = top + box_size
    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 255), 2)
    return img

def detect_faces(image):
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return results

st.title("Đăng Ký Khuôn Mặt Ra Vào Cửa C06")

# Start webcam
cap = cv2.VideoCapture(0)

# Create placeholder for video feed
video_placeholder = st.empty()

# Create button to capture image and disable it after pressing
if 'capture_disabled' not in st.session_state:
    st.session_state.capture_disabled = False

if st.session_state.capture_disabled:
    st.write("Nhấn nút Xác nhận bên dưới để tiến hành chụp lại ảnh khác.")
    if st.button("Xác nhận"):
        # Refresh the current page
        # JavaScript to refresh the page after clicking "OK"
        keyboard.press_and_release('f5')  # Simulate F5 key press
        time.sleep(0.1)
else:
    # Centering button and setting its width
    col1, col2, col3 = st.columns([1, 2, 1])  # Using a layout of three columns

    with col2:  # Use the center column for the button
        capture_button = st.button("Chụp Ảnh", key="capture_button", help="Click to capture an image", use_container_width=True)

    frame = None
    captured_frame = None  # Store captured frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Không thể chụp khung hình từ camera. Kiểm tra kết nối camera.")
            break

        # Flip frame horizontally for selfie view
        frame_flip = cv2.flip(frame, 1)

        # Draw fixed frame
        frame_with_box = draw_frame(frame_flip.copy())

        # Detect faces
        results = detect_faces(frame_flip)

        # Draw faces if detected
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame_flip.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                             int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame_with_box, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert frame to RGB for Streamlit display
        frame_rgb = cv2.cvtColor(frame_with_box, cv2.COLOR_BGR2RGB)

        # Display frame
        video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

        # Check if capture button was pressed
        if capture_button:
            captured_frame = frame_flip.copy()  # Save original frame
            break

    # If capture button was pressed, save captured frame
    if captured_frame is not None:
        # Save captured image
        image_path = os.path.join("images", "captured_image.png")
        cv2.imwrite(image_path, captured_frame)  # Save the original frame as PNG

        # Remove all other images in the folder
        for file in os.listdir("images"):
            if file != "captured_image.png":
                os.remove(os.path.join("images", file))

        st.success("Ảnh đã được chụp và lưu thành công! Vui lòng quay trở lại trang đăng ký.")
        # st.success(f"Ảnh đã được lưu tại: {image_path}")

        # Set capture button state to disabled
        st.session_state.capture_disabled = True

# Release the webcam
cap.release()
