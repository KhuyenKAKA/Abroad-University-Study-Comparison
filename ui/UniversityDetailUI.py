import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os 
from controller.UniversityController import UniversityController

# --- Dữ liệu giả định ---


# --- Hàm hỗ trợ chung ---

def create_dropdown_mock(parent_frame, title, indicator="v"):
    """Tạo một thanh mô phỏng dropdown (hoặc button) với tiêu đề và biểu tượng.
    Sử dụng highlight để mô phỏng viền mỏng màu xanh nhạt."""
    
    frame = tk.Frame(parent_frame, bg="white", relief="flat", borderwidth=0, 
                     highlightbackground="#99badd", highlightthickness=1)
    frame.pack(fill='x', padx=10, pady=5)
    
    # Text
    tk.Label(frame, text=title, font=("Arial", 10, "bold"), bg="white", anchor="w", fg="#1F3AB0").pack(side="left", padx=10, pady=10, fill="x", expand=True)
    
    # Indicator (v or ^)
    tk.Label(frame, text=indicator, font=("Arial", 12, "bold"), fg="#1F3AB0", bg="white").pack(side="right", padx=10)
    
    return frame

# Danh sách toàn cục để giữ tham chiếu ảnh (quan trọng cho Tkinter)
images_reference = [] 

# ===============================================
# Hàm tạo Header (Thanh điều hướng)
# ===============================================
def create_header(root):
    """Tạo thanh điều hướng (Header) và đặt nó ở trên cùng của cửa sổ root."""
    global images_reference
    
    nav_frame = tk.Frame(root, bg="white", height=50)
    nav_frame.pack(fill='x', padx=0, pady=0)
    nav_frame.grid_columnconfigure(0, weight=0) 
    nav_frame.grid_columnconfigure(1, weight=1) 
    nav_frame.grid_columnconfigure(7, weight=0)
    
    tk.Label(nav_frame, text="UniCompare", font=("Arial", 16, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, padx=(20, 50), pady=10, sticky="w")
    
    menu_items = ["Xếp hạng", "Khám phá", "Sự kiện", "Chuẩn bị", "Học bổng", "Chat với AI"]
    btnRankings =tk.Button(nav_frame, text=menu_items[0], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnDiscover = tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnEvents = tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnPrepare = tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnScholarships = tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnChatToStudents = tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)

    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Tư vấn miễn phí", foreground='white', background='#28a745', relief="flat").pack(side='left', padx=5)
    
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
    
    tk.Button(right_nav_frame, text="Đăng nhập", foreground='white', background="#1F3AB0", relief="flat").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Đăng ký", foreground='white', background="#1F3AB0", relief="flat").pack(side='left', padx=5)

# ===============================================
# Hàm tạo Footer
# ===============================================
def create_footer(parent_frame): # THAY ĐỔI: nhận parent_frame là khung cuộn
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
        "assets/104498_facebook_icon.png", 
        "assets/1161953_instagram_icon.png", 
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
# Hàm chính tạo UI (Đã tích hợp Header, Footer và điều chỉnh cấu trúc cuộn)
# ===============================================
def create_ui(id):
    root = tk.Tk()
    root.title("Thông tin Chi tiết Đại học | UniCompare")
    root.geometry("1000x800")
    root.configure(bg="#f0f0f0")

    # 1. TẠO HEADER (FIXED)
    create_header(root)
    
    # --- Khung chứa Nội dung chính (Sẽ cuộn) ---
    main_scroll_area = tk.Frame(root, bg="#f0f0f0")
    # Sử dụng expand=True để nó chiếm hết không gian còn lại sau Header
    main_scroll_area.pack(fill='both', expand=True) 

    canvas = tk.Canvas(main_scroll_area, bg="#f0f0f0")
    v_scrollbar = ttk.Scrollbar(main_scroll_area, orient="vertical", command=canvas.yview)
    
    # Khung chứa toàn bộ nội dung cuộn được (bao gồm Header cũ, Nội dung, và Footer)
    scrollable_frame_wrapper = tk.Frame(canvas, bg="#f0f0f0") 
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame_wrapper, anchor="nw")
    
    canvas.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    TEN_TRUONG = ""
    XEP_HANG = ""
    VI_TRI = ""
    data = UniversityController.get_uni(id)
    
    UniversityController.get_data_detail_2(id)
    if data:
        TEN_TRUONG = data[0]
        VI_TRI = data[1]
        XEP_HANG = data[2]
    def on_frame_configure(event):
        # Cập nhật vùng cuộn khi nội dung bên trong thay đổi
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    scrollable_frame_wrapper.bind("<Configure>", on_frame_configure)
    
    def on_canvas_configure(event):
        # Đảm bảo khung nội dung luôn rộng bằng canvas
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind('<Configure>', on_canvas_configure)
    
    # --- CONTENT FRAME (Mục lục & Nội dung chính) ---
    content_frame = tk.Frame(scrollable_frame_wrapper, bg="white")
    # Đóng gói content_frame vào scrollable_frame_wrapper (để nó cuộn)
    content_frame.pack(fill='x', expand=True, padx=0, pady=0) 
    
    content_frame.grid_columnconfigure(0, weight=1, minsize=200) 
    content_frame.grid_columnconfigure(1, weight=3) 
    content_frame.grid_rowconfigure(0, weight=0) # Header trường (row 0) không co giãn

    # --- Header Trường (Giữ nguyên cấu trúc cũ) ---
    header_frame = tk.Frame(content_frame, bg="#1F3AB0", height=150)
    # Đặt header_frame ở hàng 0, cột 0, span 2
    header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=(0,0), pady=(0, 10))
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text=TEN_TRUONG, font=("Arial", 20, "bold"), fg="white", bg="#1F3AB0").pack(anchor="w", padx=20, pady=(10, 0))
    tk.Label(header_frame, text=VI_TRI, font=("Arial", 10), fg="lightgray", bg="#1F3AB0").pack(anchor="w", padx=20)
    tk.Label(header_frame, text=XEP_HANG, font=("Arial", 12), bg="white", fg="#1F3AB0", padx=10, pady=5).place(x=20, y=90)
    
    # --- Mục lục và Nội dung Chính ---
    main_content_area = tk.Frame(content_frame, bg="white")
    # Đặt main_content_area ở hàng 1, cột 0, span 2
    main_content_area.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=0)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=200) 
    main_content_area.grid_columnconfigure(1, weight=3) 
    main_content_area.grid_rowconfigure(0, weight=1) 


    # --- Cột 1: Mục lục (TOC - Tương tự bản trước) ---
    toc_frame = tk.Frame(main_content_area, bg="white", width=250)
    toc_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    toc_frame.pack_propagate(False)
    tk.Label(toc_frame, text="Nội dung", font=("Arial", 14, "bold"), bg="white", anchor="w").pack(fill='x', padx=10, pady=(10, 5))
    for item in ["Tổng quan", "Thông tin học bổng", "Học phí","Xếp hạng - Đánh giá", "Chương trình học"]:
        link = tk.Label(toc_frame, text=item, font=("Arial", 10), bg="white", fg="blue", cursor="hand2", anchor="w")
        link.pack(fill='x', padx=10, pady=2)
        link.bind("<Enter>", lambda e, l=link: l.config(fg="red"))
        link.bind("<Leave>", lambda e, l=link: l.config(fg="blue"))

    # --- Cột 2: Nội dung Chính ---
    main_content_detail_frame = tk.Frame(main_content_area, bg="white")
    main_content_detail_frame.grid(row=0, column=1, sticky="nsew")

    # Scrollable Frame cho nội dung chi tiết
    scrollable_content_frame = tk.Frame(main_content_detail_frame, bg="white")
    scrollable_content_frame.pack(fill="both", expand=True)

    # --- Bắt đầu thêm nội dung vào scrollable_content_frame ---

    # 2. University information (Admission & Students & Staff)
    def create_university_info_section(parent_frame):
        tk.Label(parent_frame, text="Thông tin đầu vào", font=("Arial", 16, "bold"), bg="white", anchor="w").pack(fill='x', padx=10, pady=(20, 5))
        
        admission_content_frame = tk.Frame(parent_frame, bg="white", padx=10, pady=10)
        admission_content_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(admission_content_frame, text="Bằng cử nhân", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill='x', pady=(0, 5))
        
        bachelor_info_frame = tk.Frame(admission_content_frame, bg="white")
        bachelor_info_frame.pack(fill='x', pady=5, anchor='w')

        def create_info_box(master, title, value, unit=""):
            box = tk.Frame(master, bg="#e0e0e0", padx=15, pady=10)
            box.pack(side="left", padx=(0, 10), anchor='w') 
            tk.Label(box, text=title, font=("Arial", 9), bg="#e0e0e0").pack()
            tk.Label(box, text=f"{value}", font=("Arial", 18, "bold"), bg="#e0e0e0", fg="#3b4a68").pack()
            if unit:
                 tk.Label(box, text=unit, font=("Arial", 10), bg="#e0e0e0").pack()
        keys = ["SAT", "GRE", "GMAT", "ACT", "ATAR", "GPA", "TOEFL", "IELTS"]
        data_bacherlor = UniversityController.get_uni_detail_entry(1, id)
        data_master = UniversityController.get_uni_detail_entry(2, id)
        if data_bacherlor :
            for key, val in zip(keys, data_bacherlor):
                if val == "0" or val is None:
                    continue
                else :
                    create_info_box(bachelor_info_frame, key, val)
        
        
        # create_info_box(bachelor_info_frame, "TOEF", "100")

        tk.Label(admission_content_frame, text="Bằng thạc sĩ", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill='x', pady=(10, 5))
        
        master_info_frame = tk.Frame(admission_content_frame, bg="white")
        master_info_frame.pack(fill='x', pady=5, anchor='w')
        if data_master :
            for key, val in zip(keys, data_master):
                if val == "0" or val is None:
                    continue
                else :
                    create_info_box(master_info_frame, key, val)
        
        # create_info_box(master_info_frame, "GMAT", "728", "+")
        # create_info_box(master_info_frame, "IELTS", "7+", " ")
        # create_info_box(master_info_frame, "TOEF", "90+", " ")

        tk.Label(parent_frame, text="Thông tin học sinh", font=("Arial", 16, "bold"), bg="white", anchor="w").pack(fill='x', padx=10, pady=(20, 5))
        student_content_frame = tk.Frame(parent_frame, bg="white", padx=10, pady=10)
        student_content_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        def create_student_bar(parent, title, total, ug_percent, pg_percent):
            
            card = tk.Frame(parent, bg="white", padx=15, pady=10, relief="flat", borderwidth=0, highlightbackground="#99badd", highlightthickness=1)
            card.pack(side="left", padx=(0, 20), anchor="nw")
            
            tk.Label(card, text=title, font=("Arial", 10), fg="gray", bg="white", anchor="w").pack(fill="x")
            tk.Label(card, text=total, font=("Arial", 20, "bold"), fg="#3b4a68", bg="white", anchor="w").pack(fill="x", pady=(0, 5))
            
            TOTAL_BAR_WIDTH = 200 
            ug_width = int(TOTAL_BAR_WIDTH * (ug_percent / 100.0))
            pg_width = TOTAL_BAR_WIDTH - ug_width
            
            bar_container = tk.Frame(card, bg="#FFFFFF", height=8) 
            bar_container.pack(fill='x', pady=5)
            bar_container.pack_propagate(False)
            bar_container.config(width=TOTAL_BAR_WIDTH)

            ug_bar = tk.Frame(bar_container, bg="#99badd", width=ug_width, height=8)
            ug_bar.pack(side="left")

            pg_bar = tk.Frame(bar_container, bg="#3b4a68", width=pg_width, height=8)
            pg_bar.pack(side="left")
            
            legend_frame = tk.Frame(card, bg="white")
            legend_frame.pack(fill="x", pady=(5, 0))
            
            def create_legend_item(master, color, label, percent):
                item = tk.Frame(master, bg="white")
                item.pack(side="left", padx=(0, 15))
                
                tk.Label(item, text="●", fg=color, bg="white", font=("Arial", 8)).pack(side="left")
                tk.Label(item, text=f"{label}", font=("Arial", 9), bg="white").pack(side="left", padx=(2, 5))
                tk.Label(item, text=f"{percent}%", font=("Arial", 12, "bold"), fg="#3b4a68", bg="white").pack(side="left")

            create_legend_item(legend_frame, "#99badd", "UG students", ug_percent)
            create_legend_item(legend_frame, "#3b4a68", "PG students", pg_percent)
        data_bar = UniversityController.get_data_detail_2(id)

        create_student_bar(student_content_frame, "Tổng số học sinh", f'{data_bar[4]}', data_bar[5], data_bar[6])
        create_student_bar(student_content_frame, "Tổng số học sinh quốc tế", f'{data_bar[7]}', data_bar[8],data_bar[9])


    create_university_info_section(scrollable_content_frame)

    # 3. Scholarships
    def create_scholarships_section(parent_frame):
        data_bar = UniversityController.get_data_detail_2(id)
        tk.Label(parent_frame, text="Thông tin học bổng", font=("Arial", 16, "bold"), bg="white", anchor="w").pack(fill='x', padx=10, pady=(20, 5))
        
        scholarship_text = (f"Hiện nay chúng tôi đang cập nhật thông tin học bổng, tính đến thời điểm hiện tại trường {TEN_TRUONG} đang {data_bar[1]} học bổng.")
        tk.Label(parent_frame, text=scholarship_text, font=("Arial", 10), bg="white", justify="left", wraplength=700).pack(fill='x', padx=10, pady=(5, 10))
        
        tk.Label(parent_frame, text="Để tìm hiểu thêm chi tiết xem tại đường link: https://www.topuniversities.com/scholarships", font=("Arial", 10), bg="white", justify="left").pack(fill='x', padx=10, pady=0)
    
    create_scholarships_section(scrollable_content_frame)

    # 4. Fees
    def create_fees_section(parent_frame):
        data_bar = UniversityController.get_data_detail_2(id)
        tk.Label(parent_frame, text="Học phí", font=("Arial", 16, "bold"), bg="white", anchor="w").pack(fill='x', padx=10, pady=(20, 5))
        if data_bar[0] == 0.0:
            fee = " Chưa có thông tin"
        else: fee = f"{data_bar[0]} USD/ năm"
        tk.Label(parent_frame, text=fee, font=("Arial", 10), bg="white", justify="left", wraplength=700).pack(fill='x', padx=10, pady=(5, 10))
    create_fees_section(scrollable_content_frame)

    # 5. Rankings & Ratings
    def create_rankings_section(parent_frame):
        tk.Label(parent_frame, text="Xếp hạng - Đánh giá", font=("Arial", 16, "bold"), bg="white", anchor="w").pack(fill='x', padx=10, pady=(20, 5))
        data_rank = UniversityController.get_uni(id)
        ranking_text = f" TRường {TEN_TRUONG} hiện tại đang đứng ở vị trí # {data_rank[2]} QS World University Rankings 2026."
        tk.Label(parent_frame, text=ranking_text, font=("Arial", 10), bg="white", justify="left", wraplength=700).pack(fill='x', padx=10, pady=(0, 10))

        rank_cards_frame = tk.Frame(parent_frame, bg="white")
        rank_cards_frame.pack(fill='x', padx=10, pady=10, anchor='w')

        def create_rank_card(master, rank, title):
            card = tk.Frame(master, bg="white", relief="flat", borderwidth=0, highlightbackground="#99badd", highlightthickness=1)
            card.pack(side="left", padx=(0, 10), pady=5)
            
            rank_label = tk.Label(card, text=rank, font=("Arial", 18, "bold"), fg="#3b4a68", bg="white", padx=10, pady=5)
            rank_label.pack(anchor="w")
            
            title_label = tk.Label(card, text=title, font=("Arial", 9), fg="gray", bg="white", padx=10)
            title_label.pack(anchor="w", pady=(0, 5))
        
        create_rank_card(rank_cards_frame, f"#{data_rank[2]}", "QS World University Rankings")
    create_rankings_section(scrollable_content_frame)
    
    # 6. Programmes
    def create_programmes_section(parent_frame):
        
        title = tk.Label(parent_frame, text=" Chương trình học", font=("Arial", 16, "bold"),
                        bg="white", fg="#3b4a68", anchor="w")
        title.pack(fill="x", pady=(20, 10), padx=10)

        program_list = [
            "MBA in Finance",
            "MBA in Marketing",
            "MBA in International Business",
            "MBA in Data Analytics"
        ]

        is_mba_open = tk.BooleanVar(value=False)

        mba_frame = tk.Frame(parent_frame, bg="white", relief="flat", borderwidth=0,
                            highlightbackground="#99badd", highlightthickness=1)
        mba_frame.pack(fill="x", padx=10, pady=5)

        mba_content_container = tk.Frame(parent_frame, bg="white", padx=10) 

        def toggle_mba_dropdown(event=None):
            if is_mba_open.get():
                mba_content_container.pack_forget()
                mba_indicator_label.config(text="v")

                BG = "white"
                mba_frame.config(bg=BG)
                mba_button.config(bg=BG)
                mba_indicator_label.config(bg=BG)

                is_mba_open.set(False)
            else:
                mba_content_container.pack(fill="x", padx=10, pady=(0, 5)) 
                mba_indicator_label.config(text="^")

                BG = "#f0f7ff"
                mba_frame.config(bg=BG)
                mba_button.config(bg=BG)
                mba_indicator_label.config(bg=BG)

                is_mba_open.set(True)

            parent_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        mba_button = tk.Button(
            mba_frame,
            text="MBA",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#3b4a68",
            anchor="w",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=toggle_mba_dropdown
        )
        mba_button.pack(side="left", pady=10, padx=(10, 5), fill="x", expand=True)
        mba_button.bind("<Button-1>", toggle_mba_dropdown) 

        mba_indicator_label = tk.Label(
            mba_frame,
            text="v",
            font=("Arial", 12, "bold"),
            fg="#3b4a68",
            bg="white"
        )
        mba_indicator_label.pack(side="right", padx=10)

        def create_program_item(container, text):
            frame = tk.Frame(container, bg="white")
            frame.pack(fill="x", pady=3)

            label = tk.Label(frame, text=text, font=("Arial", 10), bg="white", fg="#3b4a68")
            label.pack(anchor="w", padx=10)

        for p in program_list:
            create_program_item(mba_content_container, p)

    create_programmes_section(scrollable_content_frame)
    
    # --- KẾT THÚC NỘI DUNG CUỘN CỦA TRANG ---
    
    # 7. TẠO FOOTER (CUỘN CÙNG VỚI NỘI DUNG)
    create_footer(scrollable_frame_wrapper) 
    
    # Chạy vòng lặp sự kiện chính
    root.mainloop()

if __name__ == "__main__":
    create_ui()