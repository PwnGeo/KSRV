import os
import re
import base64
import uuid
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Đường dẫn lưu ảnh và file thông tin
IMAGE_SAVE_PATH = 'cccd_images'
COOKIE_FILE_PATH = "cookie.txt"
SERVER_URL = "http://localhost:81/enroll/updateFaceData.php"

# Tạo thư mục để lưu trữ hình ảnh nếu chưa tồn tại
if not os.path.exists(IMAGE_SAVE_PATH):
    os.makedirs(IMAGE_SAVE_PATH)

# Đọc cookie từ file
def read_cookie():
    with open(COOKIE_FILE_PATH, "r") as f:
        return f.read().strip()

# Hàm gửi yêu cầu POST và kiểm tra response
def send_post_request(burp0_url, burp0_headers, burp0_cookies, burp0_data, file_path):
    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    print(response.text)

    if not response.ok or response.json().get("success", True) is False:
        print(f"Request failed with status code {response.status_code}. Attempting to update cookies and retry...")
        update_cookie()
        burp0_cookies["PHPSESSID"] = read_cookie()
        response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        print(response.text)
        if response.ok and response.json().get("success", True) is True:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    else:
        print("Request successful!")
    return response.text

def encode_image_to_base64(image_path):
    """Mã hóa hình ảnh thành base64."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def process_and_upload_image(file_path):
    # Định dạng tên file ảnh ví dụ: [N]Nghiêm Sỹ Thắng[G]0[P]0[CT]Wiegand26[CN]00003[D1]068078007031[D2]Nam.jpg
    # pattern = r'\[N\](?P<name>.*?)\[G\](?P<group_id>\d+)\[P\](?P<new_face>\d+)\[CT\](?P<wiegand_b64>.*?)\[CN\](?P<card_no>\d+)\[D1\](?P<id>\d+)\[D2\](?P<gender>.*?)\.jpg$'
    pattern = r'\[N\](?P<name>.*?)\[D1\](?P<id>\d+)\[D2\](?P<gender>.*?)\[CN\](?P<card_no>\d+)\.jpg$'    
    
    # Tách tên file từ đường dẫn
    file_name = os.path.basename(file_path)
    
    # Kiểm tra tên file bằng biểu thức chính quy
    match = re.match(pattern, file_name)
    if match:
        info = match.groupdict()
        print("Filename matches pattern!")
        print(f"Captured groups: {info}")

        # Mã hóa hình ảnh
        encoded_image_data = encode_image_to_base64(file_path)
        face_uuid = str(uuid.uuid4())

        # Lấy giá trị group_id từ Combobox
        group_id_display = group_id_var.get()
        group_id_mapping = {
            "Khách": "2",
            "Cán bộ C06": "0"
        }
        card_prefix_mapping = {
            "Khách": "002",
            "Cán bộ C06": "001"
        }
        group_id = group_id_mapping.get(group_id_display, "2")  # Mặc định là "2" nếu không tìm thấy
        card_prefix = card_prefix_mapping.get(group_id_display, "002")  # Mặc định là "002" nếu không tìm thấy

        burp0_data = {
            "face_uuid": face_uuid,
            "id": info.get("id", ''),
            "id2": info.get("gender", ''),
            "name": info.get("name", ''),
            "email": '',
            "wiegand_b64": '',
            "card_no": f"{card_prefix}-{info.get('card_no', '')}",
            "card_bits": "26",
            "group_id": group_id,
            "new_face": "1",
            "person_img": '',
            "img": f'["data:image/jpeg;base64,{encoded_image_data}"]'
        }

    
        # Gửi dữ liệu và xử lý phản hồi
        response = send_post_request(SERVER_URL, {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://localhost:81",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "http://localhost:81/enroll/Enroll.php",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "close"
        }, {"PHPSESSID": read_cookie()}, burp0_data, file_path)

        pattern = r'"status":\s*\[(\d+)\]'
        match = re.search(pattern, response)
        if match:
            status_value = int(match.group(1))
            if status_value == 0:
                return True, "Upload thành công!"
            else:
                return False, "Upload thất bại! Vui lòng thử lại."
        else:
            return False, "Không tìm thấy pattern 'status' trong response."
    else:
        return False, "Filename does not match the expected pattern."

def upload_batch():
    folder_path = filedialog.askdirectory(title="Chọn thư mục chứa ảnh")
    if not folder_path:
        return

    # Lấy danh sách tất cả các file ảnh trong thư mục
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for file_name in image_files:
        file_path = os.path.join(folder_path, file_name)
        success, message = process_and_upload_image(file_path)
        if success:
            tree.insert("", "end", values=(file_name, "Thành công"))
        else:
            tree.insert("", "end", values=(file_name, "Thất bại"))

def update_cookie():
    driver = webdriver.Chrome()  # or webdriver.Firefox()
    try:
        driver.get("http://localhost:81/login.php")
        username = "admin"
        password = "admin"
        input_username = driver.find_element(By.ID, "uname")
        input_password = driver.find_element(By.ID, "pwd")
        input_username.send_keys(username)
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)
        cookies = driver.get_cookies()
        with open(COOKIE_FILE_PATH, "w") as cookie_file:
            for cookie in cookies:
                if cookie['name'] == 'PHPSESSID':
                    cookie_file.write(cookie['value'] + "\n")
                    break
    finally:
        driver.quit()

def login():
    update_cookie()
    status = "Đăng nhập thành công!" if os.path.exists(COOKIE_FILE_PATH) else "Lỗi đăng nhập!"
    login_status_var.set(status)
    # Enable buttons if login is successful
    if os.path.exists(COOKIE_FILE_PATH):
        choice_button.config(state="normal")
    else:
        choice_button.config(state="disabled")
    

def create_gui():
    global login_status_var, tree, group_id_var, group_id_dropdown, choice_button

    root = tk.Tk()
    root.title("PHẦN MỀM ĐĂNG KÝ RA VÀO")
    root.geometry("824x480")
    root.configure(bg="#F0F8FF")
    font_bold = ("Helvetica", 14, "bold")
    root.iconbitmap("icon.ico")

    # Create frames for layout
    frame1 = tk.Frame(root, bg="#F0F8FF")
    frame1.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    frame2 = tk.Frame(root, bg="#F0F8FF")
    frame2.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    frame3 = tk.Frame(root, bg="#F0F8FF")
    frame3.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

    frame4 = tk.Frame(root, bg="#F0F8FF")
    frame4.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

    # Group selection
    tk.Label(frame1, text="Chọn Group:", font=font_bold, bg="#F0F8FF").pack(side="left", padx=5)

    group_id_var = tk.StringVar(value="Khách")  # Default is "Khách"
    group_id_dropdown = ttk.Combobox(frame1, textvariable=group_id_var, values=["Khách", "Cán bộ C06"], state="readonly")
    group_id_dropdown.pack(side="left", padx=5)

    # Buttons
    choice_button = tk.Button(frame3, text="Chọn thư mục", command=upload_batch, state="disabled", font=font_bold, bg="#87CEFA", fg="black")
    choice_button.pack(pady=10)
    # tk.Button(frame3, text="Chọn thư mục", command=upload_batch, state="disabled", font=font_bold, bg="#87CEFA", fg="black").pack(pady=10)

    tk.Button(frame4, text="Đăng nhập", command=login, font=font_bold, bg="#90EE90", fg="black").pack(pady=10)

    login_status_var = tk.StringVar()
    login_status_var.set("Đang chờ đăng nhập")
    tk.Label(frame4, textvariable=login_status_var, font=font_bold, bg="#F0F8FF").pack(pady=10)

    # Treeview for file upload status
    tree = ttk.Treeview(root, columns=("File", "Status"), show="headings")
    tree.heading("File", text="Tên File")
    tree.heading("Status", text="Trạng Thái")
    tree.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

    # Configure grid row and column weights for resizing
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
