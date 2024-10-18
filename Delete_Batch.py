import tkinter as tk
from tkinter import ttk, messagebox
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

COOKIE_FILE_PATH = "cookie.txt"

def update_cookie():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:81/login.php")
        username = "admin"
        password = "admin"
        input_username = driver.find_element(By.ID, "uname")
        input_password = driver.find_element(By.ID, "pwd")
        input_username.send_keys(username)
        input_password.send_keys(password)
        input_password.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)  # Đợi để đảm bảo đã đăng nhập
        
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
    status = "Đăng nhập thành công!" if os.path.exists(COOKIE_FILE_PATH) else "LỗI đăng nhập!"
    login_status_var.set(status)
    # Enable buttons if login is successful
    if os.path.exists(COOKIE_FILE_PATH):
        fetch_button.config(state="normal")
        delete_button.config(state="normal")
    else:
        fetch_button.config(state="disabled")
        delete_button.config(state="disabled")

def read_cookie():
    if os.path.exists(COOKIE_FILE_PATH):
        with open(COOKIE_FILE_PATH, "r") as f:
            cookie_value = f.read().strip()
        return {'PHPSESSID': cookie_value}
    return {}

def get_all_profiles():
    url = "http://localhost:81/enroll/getFaceList.php"
    params = {
        "ts": "1724385634133",
        "draw": "1",
        "start": "0",
        "length": "100",
        "group_idx": "65535"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = read_cookie()
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    if not response.ok or response.json().get("success", True) is False:
        print(f"Request failed with status code {response.status_code}. Attempting to update cookies and retry...")
        update_cookie()
        cookies = read_cookie()
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        
    return response.json()

def delete_profiles(face_uuids):
    url = "http://localhost:81/enroll/delFaceData.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    cookies = read_cookie()
    for face_uuid in face_uuids:
        data = f"face_uuid={face_uuid}"
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        if response.ok or response.json().get("success", True) is False:
            print(f"Deleted profile {face_uuid}")
        else:
            print(f"Request failed with status code {response.status_code}. Attempting to update cookies and retry...")
            update_cookie()
            cookies = read_cookie()
            response = requests.post(url, headers=headers, cookies=cookies, data=data)

def display_profiles_by_group(profiles):
    for item in tree.get_children():
        tree.delete(item)

    for profile in profiles:
        group = profile.get("group", "Unknown Group")
        face_uuid = profile.get("face_uuid", "Unknown UUID")
        name = profile.get("name", "Unknown Name")
        cardno = profile.get("cardno", "Unknown Card No")
        tree.insert("", "end", values=(group, face_uuid, name, cardno))

def fetch_and_display_profiles():
    profiles_data = get_all_profiles()
    if 'data' in profiles_data:
        profiles = profiles_data['data']
        display_profiles_by_group(profiles)
    else:
        print("No profiles found.")

def delete_selected_profiles():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select at least one profile to delete.")
        return

    face_uuids = [tree.item(item, "values")[1] for item in selected_items]

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected profiles?")
    if confirm:
        delete_profiles(face_uuids)
        fetch_and_display_profiles()

def create_gui():
    global login_status_var, tree, fetch_button, delete_button

    root = tk.Tk()
    root.title("PHẦN MỀM QUẢN LÝ RA VÀO")
    root.geometry("824x480")
    root.configure(bg="#F0F8FF")
    font_bold = ("Helvetica", 14, "bold")
    root.iconbitmap("ico.ico")

    frame = tk.Frame(root, bg="#F0F8FF")
    frame.pack(pady=10, padx=10, fill="x")

    login_button = tk.Button(frame, text="Đăng nhập", command=login, font=font_bold, bg="#ADD8E6")
    login_button.pack(pady=10)

    login_status_var = tk.StringVar()
    login_status_var.set("Đang chờ đăng nhập")
    login_status_label = tk.Label(frame, textvariable=login_status_var, font=font_bold, bg="#F0F8FF")
    login_status_label.pack(pady=10)

    columns = ("Group", "Face UUID", "Name", "Card No")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    fetch_button = tk.Button(frame, text="Hiển thị thông tin tất cả Profiles", command=fetch_and_display_profiles, state="disabled", font=font_bold, bg="#FFA500")
    fetch_button.pack(side="left", padx=5)

    delete_button = tk.Button(frame, text="Xóa Profiles đã chọn", command=delete_selected_profiles, state="disabled", font=font_bold, bg="#4682B4")
    delete_button.pack(side="right", padx=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
