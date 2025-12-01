import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from db import get_connection
# --- BIẾN TOÀN CỤC để lưu trữ các Entry Widgets và Biến điều khiển ---
user_entries = {}
study_entries = {}
gender_var = None

# --- HÀM LẤY VÀ XỬ LÝ DỮ LIỆU ---

def get_user_data():
    """Thu thập dữ liệu từ các trường nhập liệu của bảng users."""
    data = {k: v.get() for k, v in user_entries.items()}
    # Đảm bảo gender_var đã được khởi tạo
    if gender_var.get() == "Nam":
        data['gender'] = True
    else:
        data['gender'] = False
    return data

def get_study_data():
    """Thu thập và chuyển đổi dữ liệu từ các trường nhập liệu của bảng study_bg."""
    data = {k: v.get() for k, v in study_entries.items()}
    
    numerical_fields = {
        'gpa': float, 'act': float, 'gmat': float, 'sat': float, 
        'cat': float, 'gre': float, 'stat': float, 'ielts': float, 
        'toefl': float, 'pearson_test': float, 'cam_adv_test': float, 
        'inter_bac': float, 'graduate_year': int
    }
    
    for key, data_type in numerical_fields.items():
        value = data[key].strip()
        if value:
            try:
                data[key] = data_type(value)
            except ValueError:
                return None, f"Lỗi: Trường '{key}' phải là số."
        else:
            data[key] = None
    return data, None

def save_data():

    """Hàm xử lý việc lưu dữ liệu vào cơ sở dữ liệu."""
    user_data = get_user_data()
    study_data, error = get_study_data()
    
    if error:
        messagebox.showerror("Lỗi Nhập Liệu", error)
        return
        
    # --- LOGIC KẾT NỐI VÀ CHÈN DỮ LIỆU CƠ SỞ DỮ LIỆU TẠI ĐÂY ---
    # Thay thế phần này bằng code kết nối CSDL thực tế.
    
    try:
        # user_id = 101 # Giả lập ID người dùng
        
        # if study_data:
        #     study_data['user_id'] = user_id

        # print("--- Dữ liệu đã chuẩn bị cho DB ---")
        # print("users:", user_data)
        # print("study_bg (kèm user_id):", study_data)
        
        # messagebox.showinfo("Thành công", f"Đã lưu dữ liệu thành công cho User ID: {user_id}")
        # clear_form()
        mydb = get_connection()
        cursor = mydb.cursor()
        query = """
        INSERT INTO users
        (first_name, last_name, password, image, phone_number, gender, dob,
        country_id, email, main_lang, add_lang, ethnic_group, special, postal_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        gender = True if gender_var.get() == "Nam" else False
        values = (
            user_data.get("first_name"),
            user_data.get("last_name"),
            user_data.get("password"),
            user_data.get("image"),
            user_data.get("phone_number"),
            gender,      
            user_data.get("dob") if user_data.get("dob")!="" else None,         
            user_data.get("country_id") if user_data.get("country_id")!="" else None,  
            user_data.get("email"),
            user_data.get("main_lang"),
            user_data.get("add_lang"),
            user_data.get("ethnic_group"),
            user_data.get("special"),
            user_data.get("postal_code")
        )
        cursor.execute(query, values)
        
        user_id = cursor.lastrowid
        query = """
        INSERT INTO study_bg
        (user_id, level, major, academic_rate, gpa, graduate_year,
        act, gmat, sat, cat, gre, stat,
        ielts, toefl, pearson_test, cam_adv_test, inter_bac)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            study_data.get("level"),
            study_data.get("major"),
            study_data.get("academic_rate"),
            float(study_data.get("gpa") or 0),
            int(study_data.get("graduate_year") or 0),
            float(study_data.get("act") or 0),
            float(study_data.get("gmat") or 0),
            float(study_data.get("sat") or 0),
            float(study_data.get("cat") or 0),
            float(study_data.get("gre") or 0),
            float(study_data.get("stat") or 0),
            float(study_data.get("ielts") or 0),
            float(study_data.get("toefl") or 0),
            float(study_data.get("pearson_test") or 0),
            float(study_data.get("cam_adv_test") or 0),
            float(study_data.get("inter_bac") or 0)
        )
        cursor.execute(query, values)
        mydb.commit()
        messagebox.showinfo("Thành công","Thêm người dùng thành công")
    except Exception as e:
        messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi lưu dữ liệu: {e}")

def clear_form():
    """Xóa nội dung của tất cả các ô nhập liệu."""
    for entry in user_entries.values():
        entry.delete(0, tk.END)
    # if gender_var is not None:
    gender_var.set(value="Nam")
    
    for entry in study_entries.values():
        entry.delete(0, tk.END)

# --- HÀM THIẾT LẬP GIAO DIỆN FORM DỌC ---

def create_form_fields(parent_frame, fields_list, entries_dict):
    """Hàm trợ giúp tạo các trường nhập liệu theo cấu trúc dọc."""
    for i, (label_text, key) in enumerate(fields_list):
        ttk.Label(parent_frame, text=label_text, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky="w", padx=10, pady=2)
        entry = ttk.Entry(parent_frame, width=60)
        entry.grid(row=i, column=1, sticky="ew", padx=10, pady=2)
        entries_dict[key] = entry
    
    parent_frame.grid_columnconfigure(1, weight=1)


def setup_user_form(content_frame):
    """Tạo Form Thông tin Cá nhân."""
    global gender_var
    
    ttk.Label(content_frame, text="👤 THÔNG TIN CÁ NHÂN (USERS)", font=('Arial', 14, 'bold'), foreground='#0052cc').pack(fill='x', pady=15)
    
    user_form_frame = ttk.Frame(content_frame)
    user_form_frame.pack(fill='x', padx=20, pady=5)
    
    fields = [
        ("Tên:", "first_name"), ("Họ:", "last_name"), ("Mật khẩu:", "password"),
        ("URL Ảnh:", "image"), ("Số điện thoại:", "phone_number"), 
        ("Ngày sinh (YYYY-MM-DD):", "dob"), ("ID Quốc gia (INT):", "country_id"), 
        ("Email:", "email"), ("Ngôn ngữ chính:", "main_lang"), 
        ("Ngôn ngữ phụ:", "add_lang"), ("Nhóm dân tộc:", "ethnic_group"), 
        ("Thông tin đặc biệt:", "special"), ("Mã bưu điện:", "postal_code")
    ]
    
    create_form_fields(user_form_frame, fields, user_entries)
    
    # Thêm trường Giới tính (Boolean)
    # gender_var = tk.BooleanVar(value=True) 
    gender_var = tk.StringVar(value="Nam")
    gender_row = len(fields)
    ttk.Label(user_form_frame, text="Giới tính:", font=('Arial', 10, 'bold')).grid(row=gender_row, column=0, sticky="w", padx=10, pady=2)
    male_check = ttk.Radiobutton(user_form_frame, text="Nam", variable=gender_var, 
                                    value="Nam")
    female_check = ttk.Radiobutton(user_form_frame, text="Nữ", variable=gender_var, 
                                    value="Nu")
    male_check.grid(row=gender_row, column=1, sticky="w", padx=10, pady=2)
    female_check.grid(row=gender_row, column=1, sticky="w", padx=90, pady=2)
    
    # # Thêm nút Lưu Form
    # save_btn = tk.Button(user_form_frame, text="Lưu Thông Tin", command=save_data, foreground='white', background="#28a745")
    # save_btn.grid(row=gender_row + 1, column=1, sticky="e", padx=10, pady=10)

    ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=10, padx=20)


def setup_study_form(content_frame):
    """Tạo Form Học vấn."""
    
    ttk.Label(content_frame, text="🎓 THÔNG TIN HỌC VẤN (STUDY_BG)", font=('Arial', 14, 'bold'), foreground='#0052cc').pack(fill='x', pady=15)
    
    study_form_frame = ttk.Frame(content_frame)
    study_form_frame.pack(fill='x', padx=20, pady=5)

    fields = [
        ("Cấp độ:", "level"), ("Chuyên ngành:", "major"), ("Tỉ lệ học thuật:", "academic_rate"),
        ("GPA:", "gpa"), ("Năm tốt nghiệp:", "graduate_year"), 
        ("Điểm ACT:", "act"), ("Điểm GMAT:", "gmat"), 
        ("Điểm SAT:", "sat"), ("Điểm CAT:", "cat"), 
        ("Điểm GRE:", "gre"), ("Điểm STAT:", "stat"), 
        ("Điểm IELTS:", "ielts"), ("Điểm TOEFL:", "toefl"), 
        ("Điểm Pearson Test:", "pearson_test"), 
        ("Điểm Cam Advanced:", "cam_adv_test"),
        ("Điểm Tú tài Quốc tế:", "inter_bac")
    ]
    
    create_form_fields(study_form_frame, fields, study_entries)
    
    # Thêm nút Lưu Form Học vấn (Nếu bạn muốn lưu riêng)
    save_btn_study = tk.Button(study_form_frame, text="Lưu Học Vấn", command=save_data, foreground='white', background="#28a745")
    save_btn_study.grid(row=len(fields), column=1, sticky="e", padx=10, pady=10)


def clickCourseRecommendation(event):
    pass

def create_ui():
    root = tk.Tk()
    root.title("UniCompare - Nhập Thông Tin Người Dùng")
    root.geometry("1000x800")
    
    root.config(bg="#f8f9fa")

    nav_frame = tk.Frame(root, bg="white", height=50)
    nav_frame.pack(fill='x', padx=0, pady=0)

    nav_frame.grid_columnconfigure(0, weight=0) 
    nav_frame.grid_columnconfigure(1, weight=1) 
    nav_frame.grid_columnconfigure(2, weight=0) 
    nav_frame.grid_columnconfigure(3, weight=0) 

    tk.Label(nav_frame, text="UniCompare", font=("Arial", 16, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, padx=(20, 50), pady=10)
    
    menu_items = ["Rankings", "Discover", "Events", "Prepare", "Scholarships", "Chat To Students"]
    # ... (Phần Menu giữ nguyên)
    
    # Bắt đầu tại cột 1 và tăng dần
    for i, item in enumerate(menu_items):
        tk.Button(nav_frame, text=item, font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=i+1, padx=5, pady=10, sticky="e")
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=len(menu_items)+1, sticky="e", padx=(0, 20)) # Đặt vào cột tiếp theo

    tk.Button(right_nav_frame, text="Free Counselling",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    # Xử lý ảnh (cần đảm bảo file ảnh tồn tại hoặc sử dụng biểu tượng thay thế)
    search_photo = None
    images_reference = []
    try:
        img = Image.open("assets/search.png")
        img = img.resize((24, 24), Image.LANCZOS)
        search_photo = ImageTk.PhotoImage(img)
        tk.Button(right_nav_frame, image=search_photo, bg= 'white', relief='flat').pack(side='left', padx=5)
        images_reference.append(search_photo) # Giữ tham chiếu
    except FileNotFoundError:
        tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    
    tk.Button(right_nav_frame, text="Login", foreground='white', background="#1F3AB0").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Sign Up", foreground='white', background="#1F3AB0").pack(side='left', padx=5)
    
# main canvas se dung de lam khung keo scroll
    main_canvas = tk.Canvas(root, bg="#f8f9fa")
    main_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    main_canvas.configure(yscrollcommand=scrollbar.set)
    
    # content_frame de lam khung chinh cho noi dung
    content_frame = tk.Frame(main_canvas, bg="#f8f9fa")

    # Hàm cấu hình Scroll
    def on_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfigure(content_window, width=main_canvas.winfo_width())
        
    def on_mouse_wheel(event):
        # Kiểm tra hệ điều hành để cuộn phù hợp (Windows vs Linux/Mac)
        if root.winfo_reqwidth() > 0: # Chỉ cuộn nếu cửa sổ đã được hiển thị
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def on_canvas_resize(event):
        main_canvas.itemconfigure(content_window, width=event.width)

    content_window = main_canvas.create_window((0, 0), window=content_frame, anchor="nw")
    content_frame.bind("<Configure>", on_frame_configure)
    main_canvas.bind('<Configure>', on_canvas_resize)
    main_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # ===============================================
    # PHẦN NỘI DUNG CHÍNH (FORMS NHẬP LIỆU)
    # ===============================================
    
    # Khung chứa nội dung Form chính
    form_container = ttk.Frame(content_frame, padding="20")
    form_container.pack(fill='both', expand=True, padx=50, pady=20)
    
    # Tiêu đề trang
    tk.Label(form_container, text="📝 Nhập Liệu Thông Tin Người Dùng và Học Vấn", 
             font=("Arial", 18, "bold"), fg="#1F3AB0", bg="#f8f9fa").pack(pady=10)
    
    # 1. Thêm Form Users
    setup_user_form(form_container)

    # 2. Thêm Form Study Background
    setup_study_form(form_container)

    # ===============================================
    # Phần Footer
    # ===============================================
    
    footer_frame = tk.Frame(content_frame, bg="white", padx=50, pady=40)
    footer_frame.pack(fill='x', pady=(20, 0))
    
    # Thiết lập lưới chính cho footer (giữ nguyên)
    for i in range(5):
        footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0) 

    # Cột 0: Logo UniCompare (Mô phỏng)
    tk.Label(footer_frame, text="UniCompare", font=("Arial", 14, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, sticky="nw")
    tk.Label(footer_frame, text="© QS Quacquarelli Symonds Limited 1994 - 2025. All rights reserved.", 
             font=("Arial", 7), fg="gray", bg="white").grid(row=4, column=0, columnspan=2, sticky="sw", pady=(50, 0))
    
    # Cột 1, 2, 3, 4: Menu Links (giữ nguyên)
    menu_headers = ["About", "Contact", "Privacy", "Users"]
    menu_row = 0
    for col, header in enumerate(menu_headers):
        tk.Label(footer_frame, text=header, font=("Arial", 10, "bold"), bg="white").grid(row=menu_row, column=col+1, sticky="w")
        
    # Phần "Follow us" và Social Icons (giữ nguyên)
    social_frame = tk.Frame(footer_frame, bg="white")
    social_frame.grid(row=0, column=4, sticky="e")
    
    tk.Label(social_frame, text="Follow us", font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=(0, 10))
    
    social_icon_paths = [
        "assets/104498_facebook_icon.png", 
        "assets/1161953_instagram_icon.png", 
        "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
        "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"
    ] 
    
    for icon in social_icon_paths:
        try:
            img = Image.open(icon)
            img = img.resize((15, 15), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            icon_label = tk.Label(social_frame, image=photo, bg="white", width=15, height=15) 
            icon_label.pack(side="left", padx=3)
            images_reference.append(photo) # Lưu tham chiếu ảnh
        except FileNotFoundError:
             tk.Label(social_frame, text="I", font=("Arial", 10), bg="white").pack(side="left", padx=3)
        
    # Các khối liên kết chính (giữ nguyên)
    link_blocks = [
        ("For Students", ["Find courses", "Scholarships", "Events"]),
        ("For Institution", ["List courses", "Advertise"]),
        ("For Professionals", ["Career advice", "MBA rankings"])
    ]
    
    for i, (header, links) in enumerate(link_blocks):
        tk.Label(footer_frame, text=f"{header}", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=i, sticky="nw", pady=(20, 5))
        for j, link in enumerate(links):
            tk.Label(footer_frame, text=link, font=("Arial", 9), fg="gray", bg="white").grid(row=3+j, column=i, sticky="nw")
            
    # Khối T&C, Data Copyright... (giữ nguyên)
    tk.Label(footer_frame, text="Cookies", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=3, sticky="nw", pady=(20, 5))
    tk.Label(footer_frame, text="Data Copyright", font=("Arial", 9), fg="gray", bg="white").grid(row=3, column=3, sticky="nw")
    tk.Label(footer_frame, text="Terms & Conditions", font=("Arial", 9), fg="gray", bg="white").grid(row=4, column=3, sticky="nw")
    
    # Khối Subscribe (giữ nguyên)
    subscribe_frame = tk.Frame(footer_frame, bg="white")
    subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))
    
    tk.Label(subscribe_frame, text="Subscribe to our newsletter", font=("Arial", 10, "bold"), bg="white").pack(anchor="e")
    
    input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1)
    input_frame.pack(anchor="e", pady=5)
    
    tk.Entry(input_frame, width=25, font=("Arial", 9), relief="flat", borderwidth=0, bg="white").pack(side="left", padx=5)
    
    subscribe_btn = tk.Button(input_frame, text="→",width=5, fg="white",bg= "#1F3AB0")
    subscribe_btn.pack(side="left")

    root.mainloop()

# if __name__ == "__main__":
#     create_ui()