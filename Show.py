import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import sqlite3
from datetime import datetime

def init_new_db():
    conn = sqlite3.connect('new_system.db')
    cursor = conn.cursor()

    # Tạo bảng for thông tin trực ban
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS on_duty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        checkin_time DATETIME,
        checkout_time DATETIME
    )
    ''')

    # Chú ý tạo đúng thứ tự các bảng
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL,
        description TEXT
    )
    ''')

    # Tạo bảng individuals mới với cấu trúc yêu cầu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS individuals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        CCCD TEXT NOT NULL,
        name TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')) NOT NULL,
        public_Date DATE,
        reason TEXT,
        status TEXT CHECK(status IN ('Active', 'Inactive')) NOT NULL DEFAULT 'Active',
        create_At DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_At DATETIME DEFAULT CURRENT_TIMESTAMP,
        group_id INTEGER,
        FOREIGN KEY(group_id) REFERENCES groups(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guest_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guest_name TEXT NOT NULL,
        checkin_time DATETIME NOT NULL,
        checkout_time DATETIME,
        duration INTEGER GENERATED ALWAYS AS (ROUND((JULIANDAY(checkout_time) - JULIANDAY(checkin_time)) * 24 * 60)) VIRTUAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        event_date DATETIME NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation TEXT NOT NULL,
        operation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')


def insert_sample_data():
    conn = sqlite3.connect('new_system.db')
    cursor = conn.cursor()

    # Dữ liệu mẫu cho bảng on_duty
    cursor.executemany('''
    INSERT INTO on_duty (username, password, checkin_time, checkout_time)
    VALUES (?, ?, ?, ?)
    ''', [
        ('duty_officer1', 'password123', '2024-10-20 08:00:00', '2024-10-20 16:00:00'),
        ('duty_officer2', 'securepass', '2024-10-21 09:00:00', '2024-10-21 17:00:00')
    ])

    # Dữ liệu mẫu cho bảng groups
    cursor.executemany('''
    INSERT INTO groups (group_name, description)
    VALUES (?, ?)
    ''', [
        ('Group A', 'Cán bộ C06'),
        ('Group B', 'Khách')
    ])

    # Dữ liệu mẫu cho bảng individuals
    # Giả lập dữ liệu cho bảng individuals
    sample_individuals_data = [
        ('123456789010', 'Nguyễn Văn A', 'Male', '1990-01-01', 'Thăm thân', 'Active', '2024-10-20 08:00:00', '2024-10-20 08:00:00', 1),
        ('123456789011', 'Trần Thị B', 'Female', '1992-02-02', 'Công tác', 'Active', '2024-10-21 09:00:00', '2024-10-21 09:00:00', 1),
        ('123456789012', 'Lê Văn C', 'Male', '1995-03-03', 'Học hành', 'Inactive', '2024-10-22 10:00:00', '2024-10-22 10:00:00', 2),
        ('123456789013', 'Phạm Thị D', 'Female', '1993-04-04', 'Du lịch', 'Active', '2024-10-23 11:00:00', '2024-10-23 11:00:00', 2),
        ('123456789014', 'Hoàng Văn E', 'Other', '1991-05-05', 'Khám bệnh', 'Active', '2024-10-24 12:00:00', '2024-10-24 12:00:00', 1)
    ]

    cursor.executemany('''
    INSERT INTO individuals (CCCD, name, gender, public_Date, reason, status, create_At, update_At, group_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_individuals_data)


    # Dữ liệu mẫu cho bảng guest_visits
    cursor.executemany('''
    INSERT INTO guest_visits (guest_name, checkin_time, checkout_time)
    VALUES (?, ?, ?)
    ''', [
        ('Charlie', '2024-10-20 10:00:00', '2024-10-20 12:00:00'),
        ('Dave', '2024-10-21 11:00:00', '2024-10-21 13:30:00')
    ])

    # Dữ liệu mẫu cho bảng events
    cursor.executemany('''
    INSERT INTO events (event_name, event_date)
    VALUES (?, ?)
    ''', [
        ('Annual Meeting', '2024-11-01 09:00:00'),
        ('Tech Conference', '2024-11-15 10:00:00'),
        ('Workshop on AI', '2024-12-05 09:30:00')
    ])

    # Dữ liệu mẫu cho bảng system_logs
    cursor.executemany('''
    INSERT INTO system_logs (operation, operation_time)
    VALUES (?, ?)
    ''', [
        ('User login', '2024-10-20 08:10:00'),
        ('Data backup', '2024-10-21 02:00:00'),
        ('System update', '2024-10-21 03:00:00')
    ])


    # Xác nhận các thao tác chèn dữ liệu
    conn.commit()
    conn.close()


# Kết nối đến cơ sở dữ liệu
def create_conn():
    return sqlite3.connect('new_system.db')

# Khởi tạo cơ sở dữ liệu và người dùng mẫu nếu chưa tồn tại
def init_db():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT,
        middlename TEXT,
        lastname TEXT,
        username TEXT UNIQUE,
        password TEXT,
        avatar TEXT,
        last_login DATETIME,
        type INTEGER DEFAULT 0,
        date_added DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO users (firstname, lastname, username, password, type)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Admin', 'User', 'admin', 'admin', 1))
    
    conn.commit()
    conn.close()

# Xác thực người dùng
def authenticate_user(username, password):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Trang chủ
# Trang chủ
def home():
    st.title("Chào mừng đến với Hệ Thống Quản Lý")
    
    st.markdown("""
    ---
    Hệ thống này cung cấp sự quản lý toàn diện về việc truy cập cá nhân, ghi nhận khách và các hoạt động sự kiện. Dưới đây là các tính năng chính được minh họa bằng biểu tượng:
    """)

    # Giới thiệu các chức năng với biểu tượng
    features = [
        ("Quản lý trực ban", "Giám sát đăng nhập và ca làm việc của nhân viên trực ban.", "fa-user-clock"),
        ("Quản lý nhóm", "Phân loại cá nhân vào nhóm để tổ chức tốt hơn.", "fa-users"),
        ("Hồ sơ cá nhân", "Quản lý và xem thông tin chi tiết của các cá nhân đã đăng ký.", "fa-id-card"),
        ("Theo dõi khách", "Ghi nhận thời gian vào ra của khách và thời gian lưu trú.", "fa-calendar-check"),
        ("Lịch trình sự kiện", "Tổ chức và quản lý các sự kiện và đặt chỗ liên quan.", "fa-calendar-alt"),
        ("Nhật ký hệ thống", "Tổng quan về các hoạt động và nhật ký bảo mật của hệ thống.", "fa-cogs"),
        ("Nhật ký ra vào cá nhân", "Nhật ký chi tiết về thời gian ra vào của từng cá nhân.", "fa-door-open"),
    ]

    for title, description, icon in features:
        components.html(f"""
        <div style="display: flex; align-items: center; margin-top: 20px;">
            <i class="fas {icon}" style="font-size: 30px; margin-right: 15px;"></i>
            <div>
                <b style="font-size: 20px;">{title}</b>
                <p>{description}</p>
            </div>
        </div>
        """, height=100)

    st.markdown("""
    ---
    Sử dụng hệ thống này để quản lý, theo dõi hiệu quả các hoạt động trong tòa nhà và quản lý nhân sự.
    """)

# Module Đăng Nhập
def login_module():
    st.title("Login")
    
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign In"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.session_state.page = "dashboard"
        else:
            st.error("Invalid username or password")

######
def on_duty_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, checkin_time, checkout_time FROM on_duty")
    duties = cursor.fetchall()
    conn.close()

    st.title("On Duty List")
    st.markdown("---")

    duty_df = pd.DataFrame(duties, columns=["ID", "Username", "Check-in Time", "Check-out Time"])
    st.dataframe(duty_df)


def group_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, group_name, description FROM groups")
    groups = cursor.fetchall()
    conn.close()

    st.title("Group List")
    st.markdown("---")

    group_df = pd.DataFrame(groups, columns=["ID", "Group Name", "Description"])
    st.dataframe(group_df)


def individual_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT i.id, i.CCCD, i.name, i.gender, i.public_Date, i.reason, i.status, i.create_At, i.update_At, g.group_name 
        FROM individuals i
        LEFT JOIN groups g ON i.group_id = g.id
    ''')
    individuals = cursor.fetchall()
    conn.close()

    st.title("Danh Sách Cá Nhân")
    st.markdown("---")

    individual_df = pd.DataFrame(individuals, columns=[
        "ID", "CCCD", "Tên", "Giới Tính", "Ngày Công Khai", "Lý Do", "Trạng Thái", "Ngày Tạo", "Ngày Cập Nhật", "Nhóm"
    ])
    st.dataframe(individual_df)



def guest_visit_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, guest_name, checkin_time, checkout_time, duration FROM guest_visits
    ''')
    visits = cursor.fetchall()
    conn.close()

    st.title("Guest Visit List")
    st.markdown("---")

    visit_df = pd.DataFrame(visits, columns=["ID", "Guest Name", "Check-in Time", "Check-out Time", "Duration (minutes)"])
    st.dataframe(visit_df)


def event_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, event_name, event_date FROM events")
    events = cursor.fetchall()
    conn.close()

    st.title("Event List")
    st.markdown("---")

    event_df = pd.DataFrame(events, columns=["ID", "Event Name", "Event Date"])
    st.dataframe(event_df)


def system_log_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, operation, operation_time FROM system_logs")
    logs = cursor.fetchall()
    conn.close()

    st.title("System Logs")
    st.markdown("---")

    log_df = pd.DataFrame(logs, columns=["ID", "Operation", "Operation Time"])
    st.dataframe(log_df)

def personal_access_log_list():
    conn = create_conn()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT pal.id, i.name, pal.entry_time, pal.exit_time FROM personal_access_logs pal
        LEFT JOIN individuals i ON pal.individual_id = i.id
    ''')
    access_logs = cursor.fetchall()
    conn.close()

    st.title("Personal Access Logs")
    st.markdown("---")

    # Đảm bảo biến DataFrame được đặt tên đúng
    personal_access_log_df = pd.DataFrame(access_logs, columns=["ID", "Individual Name", "Entry Time", "Exit Time"])
    st.dataframe(personal_access_log_df)


def dashboard():
    st.sidebar.title("Menu Bảng Điều Khiển")
    menu_options = [
        "Trang Chủ", 
        "Danh Sách Trực Ban", 
        "Danh Sách Nhóm", 
        "Hồ Sơ Khách Đăng Ký", 
        "Danh Sách Sự Kiện", 
        "Nhật Ký Hệ Thống",
        "Thống Kê Số Lượng Khách",
        "Lịch Sử Ra Vào",         
        "Thông Tin Tìm Kiếm"
    ]
    choice = st.sidebar.selectbox("Lựa Chọn Mục", menu_options)

    if choice == "Trang Chủ":
        home()
    elif choice == "Danh Sách Trực Ban":
        on_duty_list()
    elif choice == "Danh Sách Nhóm":
        group_list()
    elif choice == "Hồ Sơ Khách Đăng Ký":
        individual_list()
    elif choice == "Danh Sách Sự Kiện":
        event_list()
    elif choice == "Nhật Ký Hệ Thống":
        system_log_list()
    elif choice == "Thống Kê Số Lượng Khách":
        guest_visit_list()
    elif choice == "Lịch Sử Ra Vào":
        st.write("Tính năng đang phát triển")
    elif choice == "Thông Tin Tìm Kiếm":
        st.write("Tính năng đang phát triển")

# Main app
def main():
    init_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_module()
    else:
        dashboard()

if __name__ == "__main__":
    init_new_db()
    insert_sample_data()
    main()
