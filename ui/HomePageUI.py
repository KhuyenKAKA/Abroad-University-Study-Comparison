import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def clickCourseRecommendation(event):
    pass
def create_ui():
    root = tk.Tk()
    root.title("UniCompare - Course Recommendation")
    root.geometry("1000x800")
    
    root.config(bg="#f8f9fa")

    nav_frame = tk.Frame(root, bg="white", height=50)
    nav_frame.pack(fill='x', padx=0, pady=0)

    main_canvas = tk.Canvas(root, bg="#f8f9fa")
    main_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    main_canvas.configure(yscrollcommand=scrollbar.set)
    
    content_frame = tk.Frame(main_canvas, bg="#f8f9fa")

    main_canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfigure(content_window, width=main_canvas.winfo_width())
    def on_mouse_wheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    content_frame.bind("<Configure>", on_frame_configure)
    
    def on_canvas_resize(event):
        main_canvas.itemconfigure(content_window, width=event.width)

    content_window = main_canvas.create_window((0, 0), window=content_frame, anchor="nw")
    main_canvas.bind('<Configure>', on_canvas_resize)
    main_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    
    def create_padded_frame(parent=content_frame, padding_y=20, bg_color="white"):
        frame = tk.Frame(parent, bg=bg_color)
        frame.pack(fill='x', pady=(padding_y, 0))
        return frame
        
    nav_frame.grid_columnconfigure(0, weight=0) 
    nav_frame.grid_columnconfigure(1, weight=1) 
    nav_frame.grid_columnconfigure(2, weight=0) 
    nav_frame.grid_columnconfigure(3, weight=0) 

    tk.Label(nav_frame, text="UniCompare", font=("Arial", 16, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, padx=(20, 50), pady=10)
    
    menu_items = ["Rankings", "Discover", "Events", "Prepare", "Scholarships", "Chat To Students"]
    btnRankings = tk.Button(nav_frame, text=menu_items[0], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnDiscover = tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnEvents = tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnPrepare = tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnScholarships = tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnChatToStudents = tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Free Counselling",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    try:
        img = Image.open("assets\\search.png")
        img = img.resize((24, 24), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        tk.Button(right_nav_frame, image=photo,bg= 'white',relief='flat').pack(side='left', padx=5)
    except FileNotFoundError:
        tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    
    tk.Button(right_nav_frame, text="Login", foreground='white', background="#1F3AB0").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Sign Up", foreground='white', background="#1F3AB0").pack(side='left', padx=5)

    style = ttk.Style() 
    style.configure('B.TButton', foreground='white', background='#007bff', font=('Arial', 10, 'bold'))
    style.map('B.TButton', background=[('active', '#0056b3')])
    
    header_frame = tk.Frame(content_frame, bg="#eaf4ff", padx=50, pady=40)
    header_frame.pack(fill='x')
    CourseRecommendationLabel = tk.Label(header_frame, text="Course Recommendation", font=("Arial", 10), fg="#007bff", bg="#eaf4ff")
    CourseRecommendationLabel.pack(anchor='w')
    CourseRecommendationLabel.bind("<Button-1>",clickCourseRecommendation)

    tk.Label(header_frame, text="Connect with your dream university today", 
             font=("Arial", 22, "bold"), bg="#eaf4ff").pack(anchor='w', pady=(5, 10))
             
    points_frame = tk.Frame(header_frame, bg="#eaf4ff")
    points_frame.pack(anchor='w')
    
    def add_point(parent, text):
        tk.Label(parent, text="✔ " + text, font=("Arial", 10), bg="#eaf4ff", fg="black").pack(anchor='w')
        
    add_point(points_frame, "Get personalised admission support for the top universities")
    add_point(points_frame, "Get academic details from universities in just a few clicks.")
    
    cards_container = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=30)
    cards_container.pack(fill='x')
    
    cards_container.grid_columnconfigure(0, weight=1)
    cards_container.grid_columnconfigure(1, weight=1)
    cards_container.grid_columnconfigure(2, weight=1)
    card_data = [
        {"title": "UC World University Rankings 2026", "desc": "Discover the top-performing universities around the world"},
        {"title": "UC World University Rankings by Subject 2025", "desc": "Find out which universities excel in your chosen subject"},
        {"title": "UC World University Rankings: Asia 2026", "desc": "Discover the top universities in Asia with the UC Asia University Rankings."}
    ]
    # Explore 1
    border_frame = tk.Frame(cards_container, bg="#1F3AB0", bd=2, relief="solid") 
    card_frame = tk.Frame(border_frame, bg="white", padx=15, pady=15)
    card_frame.pack(fill='both', expand=True, padx=2, pady=2) 
    
    # Tiêu đề
    tk.Label(card_frame, text=card_data[0]["title"], font=("Arial", 12, "bold"), bg="white").pack(pady=(10, 5))
    # Mô tả
    tk.Label(card_frame, text=card_data[0]["desc"], font=("Arial", 10), wraplength=220, bg="white").pack(pady=5)
    
    # Nút Explore ->
    explore1_btn = tk.Button(card_frame, text="Explore →", foreground='white', background='#1F3AB0', font=('Arial', 10, 'bold') )
    explore1_btn.pack(pady=(20, 10))
    
    border_frame.grid(row=0, column=0, padx=15, sticky="nsew")

    # Explore 2
    border_frame = tk.Frame(cards_container, bg="#1F3AB0", bd=2, relief="solid") 
    card_frame = tk.Frame(border_frame, bg="white", padx=15, pady=15)
    card_frame.pack(fill='both', expand=True, padx=2, pady=2) # Lòng thẻ bên trong đường viền
    
    # Tiêu đề
    tk.Label(card_frame, text=card_data[1]["title"], font=("Arial", 12, "bold"), bg="white").pack(pady=(10, 5))
    # Mô tả
    tk.Label(card_frame, text=card_data[1]["desc"], font=("Arial", 10), wraplength=220, bg="white").pack(pady=5)
    
    # Nút Explore ->
    explore2_btn = tk.Button(card_frame, text="Explore →", foreground='white', background='#1F3AB0', font=('Arial', 10, 'bold') )
    explore2_btn.pack(pady=(20, 10))
    
    border_frame.grid(row=0, column=1, padx=15, sticky="nsew")

    # Explore 3
    border_frame = tk.Frame(cards_container, bg="#1F3AB0", bd=2, relief="solid") 
    card_frame = tk.Frame(border_frame, bg="white", padx=15, pady=15)
    card_frame.pack(fill='both', expand=True, padx=2, pady=2) # Lòng thẻ bên trong đường viền
    
    # Tiêu đề
    tk.Label(card_frame, text=card_data[2]["title"], font=("Arial", 12, "bold"), bg="white").pack(pady=(10, 5))
    # Mô tả
    tk.Label(card_frame, text=card_data[2]["desc"], font=("Arial", 10), wraplength=220, bg="white").pack(pady=5)
    
    # Nút Explore ->
    explore3_btn = tk.Button(card_frame, text="Explore →", foreground='white', background='#1F3AB0', font=('Arial', 10, 'bold') )
    explore3_btn.pack(pady=(20, 10))
    
    border_frame.grid(row=0, column=2, padx=15, sticky="nsew")

    # ===============================================
    # 5. Phần Nhận Xét (WHAT STUDENTS SAY )
    # ===============================================

    reviews_frame = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=50)
    reviews_frame.pack(fill='x')
    
    # Tiêu đề
    tk.Label(reviews_frame, text="What students say", 
             font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=(0, 5))
    tk.Label(reviews_frame, text="Hear how we've supported students like you to find their perfect study destination", 
             font=("Arial", 10), fg="gray", bg="#f8f9fa").pack(pady=(0, 30))
             
    # Khung chứa 3 nhận xét
    cards_container_rev = tk.Frame(reviews_frame, bg="#f8f9fa")
    cards_container_rev.pack(fill='x')
    
    # Thiết lập 3 cột cho 3 khung nhận xét
    cards_container_rev.grid_columnconfigure(0, weight=1)
    cards_container_rev.grid_columnconfigure(1, weight=1)
    cards_container_rev.grid_columnconfigure(2, weight=1)

    # Dữ liệu giả nhận xét
    review_data = [
        {
            "quote": "My counsellor's assistance at every step has been invaluable, and I cannot thank him enough for making my dreams a reality.",
            "name": "Pranay Kasat",
            "info": "Master of Science in Global Logistics, W.P Carey School of Business, Arizona State University",
            "bg_color": "#eaf4ff" # Màu xanh nhạt cho khung 1
        },
        {
            "quote": "Trên đời này không có chuyện đúng sai, chỉ có kẻ yếu và kẻ không biết mình yếu! Thế thôi!",
            "name": "Đệ anh Bảnh",
            "info": "Master of Science in Global Bốc Phét, Khu 2, Hoàng Thương, Thanh Ba, Phú Thọ",
            "bg_color": "white" # Màu trắng cho khung giữa
        },
        {
            "quote": "QS were a huge help from the very beginning. When I felt overwhelmed, it was my counsellor who helped me to clarify my goals and find a programme best suited for my future.",
            "name": "Bibit Jose",
            "info": "BSc in Mechanical Engineering, Arizona State University",
            "bg_color": "#eaf4ff" # Màu xanh nhạt cho khung 3
        }
    ]

    def create_review_card(parent, row, col, data):
        card_frame = tk.Frame(parent, bg=data["bg_color"], padx=20, pady=20, relief="flat")
        card_frame.grid(row=row, column=col, padx=10, sticky="nsew")

        tk.Label(card_frame, text="“", font=("Arial", 40, "bold"), fg="#cccccc", bg=data["bg_color"]).pack(anchor="nw")

        tk.Label(card_frame, text=data["quote"], font=("Arial", 10, "italic"), wraplength=250, justify="left", bg=data["bg_color"]).pack(pady=(5, 15))
        
        tk.Label(card_frame, text="”", font=("Arial", 40, "bold"), fg="#cccccc", bg=data["bg_color"]).pack(anchor="se", pady=(10, 0))

        student_info_frame = tk.Frame(card_frame, bg=data["bg_color"])
        student_info_frame.pack(fill='x', pady=(10, 0))
        
        if col != 1: 
            photo_placeholder = tk.Label(student_info_frame, text="👤", font=("Arial", 12), width=3, height=1, bg="#007bff", fg="white")
            photo_placeholder.pack(side="left", padx=(0, 10))

        text_info_frame = tk.Frame(student_info_frame, bg=data["bg_color"])
        text_info_frame.pack(side="left", fill='x', expand=True)

        tk.Label(text_info_frame, text=data["name"], font=("Arial", 10, "bold"), bg=data["bg_color"]).pack(anchor="w")
        tk.Label(text_info_frame, text=data["info"], font=("Arial", 8), wraplength=200, justify="left", fg="gray", bg=data["bg_color"]).pack(anchor="w")


    for i, data in enumerate(review_data):
        create_review_card(cards_container_rev, 0, i, data)
    # Done

    # ===============================================
    # 6. Phần Đối Tác (PARTNER UNIVERSITIES)
    # ===============================================
    
    partners_frame = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=50)
    partners_frame.pack(fill='x')
    
    # Tiêu đề
    tk.Label(partners_frame, text="Over 650 global partner universities", 
             font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=(0, 30))
             
    # Khung chứa Logo
    logo_container = tk.Frame(partners_frame, bg="white", padx=20, pady=20, relief="solid", borderwidth=1) 
    logo_container.pack(fill='x', padx=50)
    
    # Thiết lập 5 cột cho các Logo
    for i in range(5):
        logo_container.grid_columnconfigure(i, weight=1)

    # Dữ liệu mô phỏng cho Logo (Sử dụng Label thay cho Hình ảnh)
    # try:
    #     img = Image.open("E:\\Tunz\\Python\\ProjectPythonNC\\Abroad-University-Study-Comparison\\assets\\search.png")
    #     img = img.resize((24, 24), Image.LANCZOS)
    #     photo = ImageTk.PhotoImage(img)
    #     tk.Button(right_nav_frame, image=photo,bg= 'white',relief='flat').pack(side='left', padx=5)
    # except FileNotFoundError:
    #     tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    logo_texts = [
        "University 1\nLogo", "AMERICAN\nUNIVERSITY", "Audiencia", "CARDIFF\nUNIVERSITY", "Logo 5",
        "CNAM-NWS", "Logo 7", "DALHOUSIE\nUNIVERSITY", "DEAKIN", "Logo 10",
        "UNIVERISTY\nOF MELBOURNE", "JEDHEC", "TU/E", "Logo 14", "Logo 15"
    ]
    
    row_count = 3
    col_count = 5
    
    for i, text in enumerate(logo_texts):
        row = i // col_count
        col = i % col_count
        
        # Mô phỏng ô chứa logo (Thực tế phải là hình ảnh)
        logo_box = tk.Frame(logo_container, bg="white", bd=1, relief="solid", height=80, width=150)
        logo_box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        logo_box.grid_propagate(False) # Ngăn frame thay đổi kích thước theo nội dung
        
        tk.Label(logo_box, text=text, font=("Arial", 8, "bold"), bg="white", wraplength=100, justify="center").pack(expand=True, fill='both')

    # ===============================================
    # 7. Phần Footer
    # ===============================================
    
    footer_frame = tk.Frame(content_frame, bg="white", padx=50, pady=40)
    footer_frame.pack(fill='x', pady=(20, 0))
    
    # Thiết lập lưới chính cho footer (5 cột chính)
    for i in range(5):
        footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0) # Cột 0 là Logo, còn lại là menu

    # Cột 0: Logo UniCompare (Mô phỏng)
    tk.Label(footer_frame, text="UniCompare", font=("Arial", 14, "bold"), fg="#1e90ff", bg="white").grid(row=0, column=0, sticky="nw")
    tk.Label(footer_frame, text="© QS Quacquarelli Symonds Limited 1994 - 2025. All rights reserved.", 
             font=("Arial", 7), fg="gray", bg="white").grid(row=4, column=0, columnspan=2, sticky="sw", pady=(50, 0))
    
    # Cột 1, 2, 3, 4: Menu Links
    menu_headers = ["About", "Contact", "Privacy", "Users"]
    menu_row = 0
    for col, header in enumerate(menu_headers):
        tk.Label(footer_frame, text=header, font=("Arial", 10, "bold"), bg="white").grid(row=menu_row, column=col+1, sticky="w")
        
    # Phần "Follow us" và Social Icons
    social_frame = tk.Frame(footer_frame, bg="white")
    social_frame.grid(row=0, column=4, sticky="e")
    
    tk.Label(social_frame, text="Follow us", font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=(0, 10))
    
    # Mô phỏng Social Icons (sử dụng Label với màu nền)
    social_icons = ["\uf09a", "\uf099", "\uf0d5", "\uf0e1"] # F, T, L, I (cần Font Awesome để hiển thị)
    for icon in social_icons:
        icon_label = tk.Label(social_frame, text=icon, bg="#007bff", width=2, height=1) 
        icon_label.pack(side="left", padx=3)
        
    # Các khối liên kết chính
    link_blocks = [
        ("For Students", ["Find courses", "Scholarships", "Events"]),
        ("For Institution", ["List courses", "Advertise"]),
        ("For Professionals", ["Career advice", "MBA rankings"])
    ]
    
    # Đặt các khối liên kết vào hàng 2 và 3
    for i, (header, links) in enumerate(link_blocks):
        # Header
        tk.Label(footer_frame, text=f"{header} ⌵", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=i, sticky="nw", pady=(20, 5))
        # Links
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
    
    # Input field
    tk.Entry(input_frame, width=25, font=("Arial", 9), relief="flat", borderwidth=0, bg="white").pack(side="left", padx=5)
    
    subscribe_btn = tk.Button(input_frame, text="→",width=5, fg="white",bg= "#1F3AB0")
    subscribe_btn.pack(side="left")

    root.mainloop()

# if __name__ == "__main__":
#     create_ui()