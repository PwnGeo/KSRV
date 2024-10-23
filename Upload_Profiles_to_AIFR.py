# Hàm này dùng để tải thông tin lên AIFR, cần phải có cookie để xác thực trước thì mới có thể hoạt động. Để lấy được cookie, hãy sử dụng file auto.py
def upload_info():
    cccd_info = cccd_info_entry.get()
    image_path = image_path_entry.get()
    group_id_display = group_id_var.get()
    group_id = group_id_mapping.get(group_id_display)
    
    if cccd_info and image_path:
        info = save_info(cccd_info)
        if info:
            face_uuid = str(uuid.uuid4())
            burp0_headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "http://localhost:81:81",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "http://localhost:81:81/enroll/Enroll.php",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "close"
            }
            burp0_cookies = {"PHPSESSID": read_cookie()}

            with open(image_path, "rb") as image_file:
                encoded_image_data = base64.b64encode(image_file.read()).decode('utf-8')

            if not os.path.exists(TEMP_FILE_PATH):
                with open(TEMP_FILE_PATH, "w") as temp_file:
                    temp_file.write("1")

            with open(TEMP_FILE_PATH, "r") as temp_file:
                current_card_no = int(temp_file.read())

            next_card_no = current_card_no + 1

            with open(TEMP_FILE_PATH, "w") as temp_file:
                temp_file.write(str(next_card_no).zfill(6))

            burp0_data = {
                "face_uuid": face_uuid,
                "id": info.get("Số CCCD", ''),
                "id2": info.get("Giới tính", ''),
                "name": info.get("Họ và tên", ''),
                "email": '',
                "wiegand_b64": '',
                "card_no": f"001-{str(next_card_no).zfill(5)}",
                "card_bits": "26",
                "group_id": group_id,
                "new_face": "1",
                "person_img": '',
                "img": f'["data:image/jpeg;base64,{encoded_image_data}"]'
            }

            response = send_post_request(SERVER_URL, burp0_headers, burp0_cookies, burp0_data, image_path)

            pattern = r'"status":\s*\[(\d+)\]'
            match = re.search(pattern, response)
            if match:
                status_value = int(match.group(1))
                if status_value == 0:
                    # Log the information on successful upload including username and timestamp
                    log_cccd_info(info, logged_in_user)  # Assuming logged_in_user stores the username of the logged account
                    messagebox.showinfo("Success", "Thông tin đã được tải lên thành công!")                
                    # messagebox.showinfo("Success", "Upload thành công và thông tin đã được lưu vào log_access.txt!")
                else:
                    messagebox.showerror("Failed", "Upload thất bại! Vui lòng thử lại.")
                    with open(TEMP_FILE_PATH, "w") as temp_file:
                        temp_file.write(str(current_card_no).zfill(6))
            else:
                messagebox.showerror("Failed", "Không tìm thấy pattern 'status' trong response")
                with open(TEMP_FILE_PATH, "w") as temp_file:
                    temp_file.write(str(current_card_no).zfill(6))
        else:
            messagebox.showerror("Error", "Thông tin CCCD không hợp lệ.")
    else:
        messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin và chọn ảnh.")
