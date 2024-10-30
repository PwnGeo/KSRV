import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox
import os

# Tạo thư mục để lưu ảnh nếu chưa tồn tại
output_dir = 'faces'
os.makedirs(output_dir, exist_ok=True)

# Khởi tạo các đối tượng MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

# Kích thước khung hình
frame_width = 640
frame_height = 480

# Kích thước khung vàng
square_size = 300
center_x, center_y = frame_width // 2, frame_height // 2

def take_snapshot():
    global image, center_x, center_y, square_size

    # Cắt ảnh rõ nét bên trong khung vàng
    cropped_face = image[center_y - square_size // 2:center_y + square_size // 2,
                         center_x - square_size // 2:center_x + square_size // 2]

    # Kiểm tra kích thước khuôn mặt
    height, width, _ = cropped_face.shape

    if height < 150 or width < 150:
        messagebox.showwarning("Cảnh báo", "Kích thước khuôn mặt quá nhỏ. Vui lòng tiến lại gần hơn.")
        return

    # Mở rộng kích thước hình lưu lớn hơn 30% khung vàng
    new_square_size = int(square_size * 1.3)

    # Tạo một hình ảnh với kích thước mở rộng
    extended_cropped_face = cv2.resize(cropped_face, (new_square_size, new_square_size))

    # Lưu ảnh với chất lượng cao
    cv2.imwrite(os.path.join(output_dir, 'captured_face.png'), extended_cropped_face, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    
    messagebox.showinfo("Thông báo", "Đã chụp hình và lưu thành công!")

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Photo Capture")

# Nút chụp hình
capture_button = tk.Button(root, text="Chụp Hình", command=take_snapshot)
capture_button.pack(pady=20)

def update_frame():
    global image
    
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        return
    
    # Chuyển đổi hình ảnh sang RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    # Tạo mặt nạ cho khung vàng
    mask = np.zeros((frame_height, frame_width), dtype=np.uint8)
    cv2.rectangle(mask, 
                  (center_x - square_size // 2, center_y - square_size // 2), 
                  (center_x + square_size // 2, center_y + square_size // 2), 
                  255, 
                  -1)  # Mặt nạ màu trắng ở khung vàng
        
    # Làm mờ ảnh gốc
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Kết hợp các phần: giữ nguyên phần bên trong khung vàng, phần bên ngoài là mờ
    result_image = np.where(mask[:, :, np.newaxis] == 255, image, blurred_image)

    # Kiểm tra phát hiện khuôn mặt
    if results.multi_face_landmarks:
        # Vẽ khung chữ nhật dọc màu đỏ quanh khuôn mặt
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = image.shape
            
        # Tính toán bounding box từ landmarks
        x_min = int(min(landmark.x for landmark in face_landmarks.landmark) * w)
        x_max = int(max(landmark.x for landmark in face_landmarks.landmark) * w)
        y_min = int(min(landmark.y for landmark in face_landmarks.landmark) * h)
        y_max = int(max(landmark.y for landmark in face_landmarks.landmark) * h)

        # Vẽ khung chữ nhật dọc màu đỏ quanh khuôn mặt
        cv2.rectangle(result_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)  # Màu đỏ

    # Vẽ khung vàng
    cv2.rectangle(result_image, 
                  (center_x - square_size // 2, center_y - square_size // 2), 
                  (center_x + square_size // 2, center_y + square_size // 2), 
                  (0, 255, 255), 2)  # Màu vàng

    # Hiển thị hình ảnh đã xử lý
    cv2.imshow('Face Detection', result_image)

    root.after(10, update_frame)  # Tiếp tục cập nhật khung hình

# Bắt đầu quá trình cập nhật khung hình
update_frame()

# Đóng camera khi cửa sổ Tkinter bị đóng
def on_closing():
    cap.release()  # Giải phóng camera
    cv2.destroyAllWindows()  # Đóng tất cả cửa sổ OpenCV
    root.destroy()  # Đóng cửa sổ Tkinter

root.protocol("WM_DELETE_WINDOW", on_closing)  # Định nghĩa hành động khi cửa sổ bị đóng
root.mainloop()  # Bắt đầu vòng lặp giao diện người dùng
