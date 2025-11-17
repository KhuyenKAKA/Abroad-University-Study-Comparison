import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from PIL import Image, ImageTk 

# Thiết lập đường dẫn tương đối (giả định)
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
except NameError:
    pass

# Danh sách toàn cục để giữ tham chiếu ảnh (quan trọng cho Tkinter)
images_reference = [] 

# ===============================================
# Hàm tạo Header (Giữ nguyên, đặt CỐ ĐỊNH)
# ===============================================
def create_header(root):
    """Tạo thanh điều hướng (Header) và đặt nó ở trên cùng của cửa sổ root."""
    global images_reference
    
    nav_frame = tk.Frame(root, bg="white", height=50)
    nav_frame.pack(fill='x', padx=0, pady=0)
    
    # Cấu hình grid cho nav_frame
    nav_frame.grid_columnconfigure(0, weight=0) 
    nav_frame.grid_columnconfigure(1, weight=1) 
    nav_frame.grid_columnconfigure(7, weight=0)

    tk.Label(nav_frame, text="UniCompare", font=("Arial", 16, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, padx=(20, 50), pady=10, sticky="w")
    
    menu_items = ["Rankings", "Discover", "Events", "Prepare", "Scholarships", "Chat To Students"]
    
    for i, item in enumerate(menu_items):
        tk.Button(nav_frame, text=item, font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=i+1, padx=5, pady=10, sticky="w")
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Free Counselling", foreground='white', background='#28a745', relief="flat").pack(side='left', padx=5)
    
    # Mô phỏng nút Search
    search_path = "assets/search.png"
    try:
        if os.path.exists(search_path):
            img = Image.open(search_path)
            img = img.resize((24, 24), Image.LANCZOS)
            search_photo = ImageTk.PhotoImage(img)
            images_reference.append(search_photo) 
            tk.Button(right_nav_frame, image=search_photo, bg='white', relief='flat').pack(side='left', padx=5)
        else:
            tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    except Exception:
        tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    
    tk.Button(right_nav_frame, text="Login", foreground='white', background="#1F3AB0", relief="flat").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Sign Up", foreground='white', background="#1F3AB0", relief="flat").pack(side='left', padx=5)

# ===============================================
# Hàm tạo Footer (Đặt trong khung cuộn)
# ===============================================
def create_footer(parent_frame): 
    """Tạo Footer và đặt nó trong khung nội dung cuộn được."""
    global images_reference
    
    footer_frame = tk.Frame(parent_frame, bg="white", padx=50, pady=40)
    footer_frame.pack(fill='x', pady=(20, 0)) # Đóng gói vào parent_frame (khung cuộn)
    
    for i in range(5):
        footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0, minsize=150)

    # Cột 0: Logo UniCompare (Mô phỏng)
    tk.Label(footer_frame, text="UniCompare", font=("Arial", 14, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, sticky="nw")
    tk.Label(footer_frame, text="© QS Quacquarelli Symonds Limited 1994 - 2025. All rights reserved.", 
             font=("Arial", 7), fg="gray", bg="white").grid(row=4, column=0, columnspan=2, sticky="sw", pady=(50, 0))
    
    # Cột 1, 2, 3, 4: Menu Links (Headers)
    menu_headers = ["About", "Contact", "Privacy", "Users"]
    menu_row = 0
    for col, header in enumerate(menu_headers):
        tk.Label(footer_frame, text=header, font=("Arial", 10, "bold"), bg="white").grid(row=menu_row, column=col+1, sticky="w")
        
    # Phần "Follow us" và Social Icons
    social_frame = tk.Frame(footer_frame, bg="white")
    social_frame.grid(row=0, column=4, sticky="ne")
    
    tk.Label(social_frame, text="Follow us", font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=(0, 10))
    
    social_icons = [
        "assets/104498_facebook_icon.png", "assets/1161953_instagram_icon.png", 
        "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
        "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"
    ] 
    
    ICON_SIZE = 18 
    
    for icon_path in social_icons:
        try:
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                icon_label = tk.Label(social_frame, image=photo, bg="white", width=ICON_SIZE, height=ICON_SIZE) 
                icon_label.pack(side="left", padx=3)
                images_reference.append(photo) 
            else:
                tk.Label(social_frame, text="●", fg="#1F3AB0", bg="white").pack(side="left", padx=3)
        except Exception:
            tk.Label(social_frame, text="●", fg="#1F3AB0", bg="white").pack(side="left", padx=3)
            
    # Các khối liên kết chính
    link_blocks = [
        ("For Students", ["Find courses", "Scholarships", "Events"]),
        ("For Institution", ["List courses", "Advertise"]),
        ("For Professionals", ["Career advice", "MBA rankings"])
    ]
    
    for i, (header, links) in enumerate(link_blocks):
        tk.Label(footer_frame, text=f"{header}", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=i, sticky="nw", pady=(20, 5))
        for j, link in enumerate(links):
            tk.Label(footer_frame, text=link, font=("Arial", 9), fg="gray", bg="white").grid(row=3+j, column=i, sticky="nw")
            
    # Khối T&C, Data Copyright...
    tk.Label(footer_frame, text="Cookies", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=3, sticky="nw", pady=(20, 5))
    tk.Label(footer_frame, text="Data Copyright", font=("Arial", 9), fg="gray", bg="white").grid(row=3, column=3, sticky="nw")
    tk.Label(footer_frame, text="Terms & Conditions", font=("Arial", 9), fg="gray", bg="white").grid(row=4, column=3, sticky="nw")
    
    # Khối Subscribe
    subscribe_frame = tk.Frame(footer_frame, bg="white")
    subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))
    
    tk.Label(subscribe_frame, text="Subscribe to our newsletter", font=("Arial", 10, "bold"), bg="white").pack(anchor="e")
    
    input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1)
    input_frame.pack(anchor="e", pady=5)
    
    tk.Entry(input_frame, width=25, font=("Arial", 9), relief="flat", borderwidth=0, bg="white").pack(side="left", padx=5)
    
    subscribe_btn = tk.Button(input_frame, text="→",width=5, fg="white",bg= "#1F3AB0", relief="flat")
    subscribe_btn.pack(side="left")


# ===============================================
# Hàm chính tạo UI (Đã tích hợp cơ chế cuộn)
# ===============================================
def create_ui():
    """Tạo giao diện đăng ký người dùng với cuộn full-width"""
    
    root = tk.Tk()
    root.title("Biểu mẫu Đăng ký QS")
    # Tắt kích thước cố định để cửa sổ có thể co giãn
    root.geometry("1200x800") 
    
    # --- 1. TẠO HEADER (FIXED) ---
    create_header(root)
    
    # --- 2. KHU VỰC CUỘN CHÍNH (Chiếm hết không gian còn lại) ---
    main_scroll_area = tk.Frame(root, bg="#f0f0f0")
    main_scroll_area.pack(fill='both', expand=True) 

    canvas = tk.Canvas(main_scroll_area, bg="#f0f0f0")
    v_scrollbar = ttk.Scrollbar(main_scroll_area, orient="vertical", command=canvas.yview)
    
    # Khung chứa toàn bộ nội dung cuộn được (Form và Footer)
    scrollable_frame_wrapper = tk.Frame(canvas, bg="#f0f0f0") 
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame_wrapper, anchor="nw")
    
    canvas.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    def on_frame_configure(event):
        # Cập nhật vùng cuộn khi nội dung bên trong thay đổi
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    scrollable_frame_wrapper.bind("<Configure>", on_frame_configure)
    
    def on_canvas_configure(event):
        # Đảm bảo khung nội dung luôn rộng bằng canvas
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind('<Configure>', on_canvas_configure)
    
    # --- 3. Đặt FORM ĐĂNG KÝ vào khung CUỘN (scrollable_frame_wrapper) ---
    
    # Khung chứa chính giữa (để căn giữa form)
    center_aligner = ttk.Frame(scrollable_frame_wrapper, padding="50", style='CenterAligner.TFrame')
    center_aligner.pack(fill='x', expand=True)
    center_aligner.grid_columnconfigure(0, weight=1) # Cột trống bên trái
    center_aligner.grid_columnconfigure(1, weight=0) # Cột form (fixed width)
    center_aligner.grid_columnconfigure(2, weight=1) # Cột trống bên phải

    # Khung Form Chính (đặt vào giữa center_aligner)
    main_frame = ttk.Frame(center_aligner) 
    main_frame.grid(row=0, column=1, sticky='nsew')
    
    # Thiết lập trọng số cột cho main_frame để chia không gian (dùng grid bên trong)
    main_frame.grid_columnconfigure(0, weight=1, minsize=400) # Cột 0 (Trái)
    main_frame.grid_columnconfigure(1, weight=1, minsize=400) # Cột 1 (Phải)
    
    # Thiết lập style
    style = ttk.Style()
    style.configure('Left.TFrame', background='#7EA6F2') 
    style.configure('CenterAligner.TFrame', background='#f0f0f0') 

    # --- Phần 2: Cột bên trái (Thông tin khuyến khích) ---
    left_frame = ttk.Frame(main_frame, padding="30", style='Left.TFrame', width=400, height=800) # Tăng height
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.pack_propagate(False) 

    title_label = ttk.Label(left_frame, text="Đến lúc nắm quyền\nkiểm soát tương lai\ncủa bạn", 
                            font=("Arial", 16, "bold"), 
                            background='#7EA6F2', 
                            foreground="#333")
    title_label.pack(pady=(50, 20), anchor='w')

    bullets = [
        "Nhận hướng dẫn cá nhân hóa cho tìm kiếm đại học của bạn",
        "Là người đầu tiên biết khi bảng xếp hạng mới được phát hành",
        "Có quyền truy cập độc quyền vào tất cả các công cụ và tài nguyên để tìm khóa học hoàn hảo của bạn"
    ]
    
    for text in bullets:
        bullet_label = ttk.Label(left_frame, text=text, 
                                 font=("Arial", 10), 
                                 background='#7EA6F2', 
                                 foreground="#555",
                                 wraplength=300)
        bullet_label.pack(pady=5, anchor='w')
        
    ttk.Label(left_frame, background='#7EA6F2').pack(pady=40, fill='x')


    # --- Phần 3: Cột bên phải (Form Đăng ký) ---
    right_frame = ttk.Frame(main_frame, padding="30", width=400, height=800) # Tăng height
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.pack_propagate(False) 
    
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_columnconfigure(1, weight=1)
    
    # Hàng 0: Tiêu đề "Đăng ký"
    signup_title = ttk.Label(right_frame, text="Đăng ký", font=("Arial", 14, "bold"))
    signup_title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky='w')

    # --- Các trường nhập liệu (Hàng 1 đến Hàng 5) ---
    labels = ["Họ*", "Tên*", "Email*", "Mật khẩu*", "Xác nhận mật khẩu*"]
    entries = []
    for i, label_text in enumerate(labels):
        label = ttk.Label(right_frame, text=label_text, font=("Arial", 9))
        label.grid(row=1 + i*2, column=0, columnspan=2, pady=(10, 2), sticky='w')
        
        if i >= 3: 
            entry = ttk.Entry(right_frame, show="*")
        else:
            entry = ttk.Entry(right_frame)
        
        entry.grid(row=2 + i*2, column=0, columnspan=2, pady=(0, 10), sticky='ew', ipady=3)
        entries.append(entry)
        
    # Hàng 11 & 12: Checkboxes
    cb_var1 = tk.BooleanVar()
    cb1 = tk.Checkbutton(right_frame, text="Tôi rất vui khi nhận được các thông tin liên lạc và tài nguyên hữu ích từ QS liên quan đến sở thích học tập và hứa hẹn sự kiện của tôi.", variable=cb_var1, wraplength=350, justify='left', bg='white')
    cb1.grid(row=11, column=0, columnspan=2, pady=5, sticky='w')
    
    cb_var2 = tk.BooleanVar()
    cb2 = tk.Checkbutton(right_frame, text="Tôi rất vui khi nhận được tin nhắn từ các bên thứ ba bao gồm các tổ chức phù hợp với sở thích học tập của tôi.", variable=cb_var2, wraplength=350, justify='left', bg='white')
    cb2.grid(row=12, column=0, columnspan=2, pady=5, sticky='w')

    # Hàng 13: Nút "Đăng ký"
    def on_signup_click():
        # Lấy dữ liệu và kiểm tra checkbox (mô phỏng)
        agree_communication = cb_var1.get()
        agree_third_party = cb_var2.get()
        
        if not agree_communication or not agree_third_party:
            messagebox.showerror("Lỗi", "Vui lòng đánh dấu cả hai hộp kiểm để tiếp tục")
            return
        
        messagebox.showinfo("Thành công (Mô phỏng)", f"Đăng ký thành công cho Email: {entries[2].get()}")
        # ... logic đăng ký thực tế ...
        
    signup_button = tk.Button(right_frame, text="Đăng ký", bg="#1F3AB0", fg="white", font=("Arial", 10, "bold"), bd=0, padx=10, pady=8, command=on_signup_click)
    signup_button.grid(row=13, column=0, columnspan=2, pady=(20, 10), sticky='ew')

    # Hàng 14: Link "Đăng nhập"
    signin_frame = ttk.Frame(right_frame)
    signin_frame.grid(row=14, column=0, columnspan=2, pady=(10, 0), sticky='w')
    
    dont_have_label = ttk.Label(signin_frame, text="Bạn đã có tài khoản?", font=("Arial", 9))
    dont_have_label.pack(side=tk.LEFT)
    
    def go_to_signin():
        # ... logic chuyển trang (mô phỏng) ...
        messagebox.showinfo("Chuyển trang", "Chuyển đến trang Đăng nhập")
    
    signin_button = tk.Button(signin_frame, text="Đăng nhập", fg="#1F3AB0", bg="white", 
                              bd=0, font=("Arial", 9), cursor="hand2",
                              command=go_to_signin)
    signin_button.pack(side=tk.LEFT, padx=(5, 0))
    
    # --- 4. TẠO FOOTER (CUỘN CÙNG VỚI NỘI DUNG) ---
    create_footer(scrollable_frame_wrapper) 
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()