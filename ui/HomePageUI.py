import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ui.ChatbotUI import ChatApp



def clickCourseRecommendation(event):
    pass
def create_ui():
    root = tk.Tk()
    root.title("UniCompare - Định hướng tương lai cùng bạn")
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
    
    menu_items = ["Xếp hạng", "Khám phá", "Sự kiện", "Chuẩn bị", "Học bổng", "Chat với AI"]
    btnRankings = tk.Button(nav_frame, text=menu_items[0], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnDiscover = tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnEvents = tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnPrepare = tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnScholarships = tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnChatToStudents = tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat", command=lambda: ChatApp(root))

    btnChatToStudents.grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Tư vấn miễn phí",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    try:
        # img = Image.open("Abroad-University-Study-Comparison/assets/search.png")
        img = Image.open("assets/search.png")
        img = img.resize((24, 24), Image.LANCZOS)
        search_photo = ImageTk.PhotoImage(img)
        tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
    except FileNotFoundError:
        tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    
    tk.Button(right_nav_frame, text="Đăng nhập", foreground='white', background="#1F3AB0").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Đăng ký", foreground='white', background="#1F3AB0").pack(side='left', padx=5)

    # style = ttk.Style() 
    # style.configure('B.TButton', foreground='white', background='#007bff', font=('Arial', 10, 'bold'))
    # style.map('B.TButton', background=[('active', '#0056b3')])
    
    header_frame = tk.Frame(content_frame, bg="#eaf4ff", padx=50, pady=40)
    header_frame.pack(fill='x')
    CourseRecommendationLabel = tk.Label(header_frame, text="Các trường được đề xuất", font=("Arial", 10), fg="#007bff", bg="#eaf4ff")
    CourseRecommendationLabel.pack(anchor='w')
    CourseRecommendationLabel.bind("<Button-1>",clickCourseRecommendation)

    tk.Label(header_frame, text="Kết nối với trường học mơ ước của bạn ngay hôm nay", 
             font=("Arial", 22, "bold"), bg="#eaf4ff").pack(anchor='w', pady=(5, 10))
             
    points_frame = tk.Frame(header_frame, bg="#eaf4ff")
    points_frame.pack(anchor='w')
    
    def add_point(parent, text):
        tk.Label(parent, text="✔ " + text, font=("Arial", 10), bg="#eaf4ff", fg="black").pack(anchor='w')
        
    add_point(points_frame, "Nhận tư vấn tuyển sinh cá nhân hóa cho các trường đại học hàng đầu")
    add_point(points_frame, "Xem thông tin học thuật từ các trường đại học chỉ với vài cú nhấp chuột.")
    
    cards_container = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=30)
    cards_container.pack(fill='x')
    
    cards_container.grid_columnconfigure(0, weight=1)
    cards_container.grid_columnconfigure(1, weight=1)
    cards_container.grid_columnconfigure(2, weight=1)
    card_data = [
        {"title": "Xếp hạng Đại học Thế giới UC năm 2026", "desc": "Khám phá các trường đại học hàng đầu trên toàn thế giới"},
        {"title": "Xếp hạng Đại học Thế giới UC theo Ngành học năm 2025", "desc": "Tìm hiểu xem trường đại học nào xuất sắc trong ngành học bạn đã chọn"},
        {"title": "Xếp hạng Đại học Thế giới UC: Châu Á năm 2026", "desc": "Khám phá các trường đại học hàng đầu tại Châu Á với Bảng xếp hạng Đại học UC Châu Á"}
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
    explore1_btn = tk.Button(card_frame, text="Khám phá →", foreground='white', background='#1F3AB0', font=('Arial', 10, 'bold') )
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
    explore2_btn = tk.Button(card_frame, text="Khám phá →", foreground='white', background='#1F3AB0', font=('Arial', 10, 'bold') )
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
    explore3_btn = tk.Button(card_frame, text="Khám phá →", foreground='white', background='#1F3AB0', font=('Arial', 10, 'bold') )
    explore3_btn.pack(pady=(20, 10))
    
    border_frame.grid(row=0, column=2, padx=15, sticky="nsew")

    # ===============================================
    # 5. Phần Nhận Xét (WHAT STUDENTS SAY )
    # ===============================================

    reviews_frame = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=50)
    reviews_frame.pack(fill='x')
    
    # Tiêu đề
    tk.Label(reviews_frame, text="Nhận xét từ sinh viên", 
             font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=(0, 5))
    tk.Label(reviews_frame, text="Hãy lắng nghe cách chúng tôi đã hỗ trợ những sinh viên như bạn tìm được điểm đến du học lý tưởng", 
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
            "quote": "Sự hỗ trợ từ chuyên viên tư vấn trong mọi bước đi là vô giá, và tôi vô cùng biết ơn vì đã giúp ước mơ của tôi trở thành hiện thực.",
            "name": "Pranay Kasat",
            "info": "Thạc sĩ Khoa học ngành Logistics Toàn cầu, Trường Kinh doanh W.P Carey, Đại học Bang Arizona",
            "bg_color": "#eaf4ff" # Màu xanh nhạt cho khung 1
        },
        {
            "quote": "Trên đời này không có gì tuyệt vời hơn UniCompare khi ai đang tìm thông tin về các trường đại học cho tương lai của mình! Thế thôi!",
            "name": "Hà Thiên Nhất",
            "info": "Master of Science in Global UnderGround, Khu 2, Hoàng Thương, Thanh Ba, Phú Thọ",
            "bg_color": "white" # Màu trắng cho khung giữa
        },
        {
            "quote": "UniCompare đã giúp đỡ tôi rất nhiều ngay từ ban đầu. Khi tôi cảm thấy mệt mỏi, chính chuyên viên tư vấn của tôi đã giúp tôi làm rõ mục tiêu và tìm ra chương trình phù hợp nhất cho tương lai của tôi.",
            "name": "Bibit Jose",
            "info": "Cử nhân Khoa học ngành Kỹ thuật Cơ khí, Đại học Bang Arizona",
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
        
        # if col != 1: 
        #     photo_placeholder = tk.Label(student_info_frame, text="👤", font=("Arial", 12), width=3, height=1, bg="#007bff", fg="white")
        #     photo_placeholder.pack(side="left", padx=(0, 10))

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
    tk.Label(partners_frame, text="Có thể có 650 trường đại học đối tác toàn cầu", 
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
    # logo_texts = [
    #     "assets/American_university.png",
    #     "assets/Auckland-University-Logo.png",
    #     "assets/Boston-University-Logo.png",
    #     "assets/Brown-Unversity-Logo.png",
    #     "assets/Cairo-University-Logo.png",
    #     "assets/Chicago-University-Logo.png",
    #     "assets/Columbia-University-Logo.png",
    #     "assets/Cornell-University-Logo.png",
    #     "assets/Duke-University-Logo.png",
    #     "assets/Georgetown-University-Logo.png",
    #     "assets/Harvard-University-Logo.png",
    #     "assets/Melbourne-University-Logo.png",
    #     "assets/Moscow-State-University-Logo.png",
    #     "assets/National-University-of-Singapore-Logo.png",
    #     "assets/Northeastern-University-Logo.png",
    # ]
    logo_texts = [
        "Abroad-University-Study-Comparison/assets/American_university.png",
        "Abroad-University-Study-Comparison/assets/Auckland-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Boston-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Brown-Unversity-Logo.png",
        "Abroad-University-Study-Comparison/assets/Cairo-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Chicago-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Columbia-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Cornell-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Duke-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Georgetown-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Harvard-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Melbourne-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/Moscow-State-University-Logo.png",
        "Abroad-University-Study-Comparison/assets/National-University-of-Singapore-Logo.png",
        "Abroad-University-Study-Comparison/assets/Northeastern-University-Logo.png",   
    ]
    row_count = 3
    col_count = 5
    images_reference = []
    for i, text in enumerate(logo_texts):
        row = i // col_count
        col = i % col_count
        
        # Mô phỏng ô chứa logo (Thực tế phải là hình ảnh)
        logo_box = tk.Frame(logo_container, bg="white", bd=1, relief="solid", height=80, width=150)
        logo_box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        logo_box.grid_propagate(False) # Ngăn frame thay đổi kích thước theo nội dung
        
        img = Image.open(text)
        img = img.resize((120, 120), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        tk.Label(logo_box, image=photo, font=("Arial", 8, "bold"), bg="white", wraplength=100, justify="center").pack(expand=True, fill='both')
        images_reference.append(photo)

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
    tk.Label(footer_frame, text="© QS Quacquarelli Symonds Limited 1994 - 2025. Mọi quyền đã được bảo hộ.", 
             font=("Arial", 7), fg="gray", bg="white").grid(row=4, column=0, columnspan=2, sticky="sw", pady=(50, 0))
    
    # Cột 1, 2, 3, 4: Menu Links
    menu_headers = ["Về chúng tôi", "Liên hệ", "Quyền riêng tư", "Người dùng"]
    menu_row = 0
    for col, header in enumerate(menu_headers):
        tk.Label(footer_frame, text=header, font=("Arial", 10, "bold"), bg="white").grid(row=menu_row, column=col+1, sticky="w")
        
    # Phần "Follow us" và Social Icons
    social_frame = tk.Frame(footer_frame, bg="white")
    social_frame.grid(row=0, column=4, sticky="e")
    
    tk.Label(social_frame, text="Theo dõi chúng tôi", font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=(0, 10))
    
    # Mô phỏng Social Icons (sử dụng Label với màu nền)
    # social_icons = ["assets/104498_facebook_icon.png", 
    #                 "assets/1161953_instagram_icon.png", 
    #                 "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
    #                 "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    social_icons = ["Abroad-University-Study-Comparison/assets/104498_facebook_icon.png", 
                    "Abroad-University-Study-Comparison/assets/1161953_instagram_icon.png", 
                    "Abroad-University-Study-Comparison/assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
                    "Abroad-University-Study-Comparison/assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    for icon in social_icons:
        img = Image.open(icon)
        img = img.resize((15, 15), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        icon_label = tk.Label(social_frame, image=photo, bg="#007bff", width=15, height=15) 
        icon_label.pack(side="left", padx=3)
        images_reference.append(photo)
        
    # Các khối liên kết chính
    link_blocks = [
        ("Dành cho sinh viên", ["Tìm kiếm khóa học", "Học bổng", "Sự kiện"]),
        ("Dành cho tổ chức", ["Danh sách khóa học", "Quảng cáo"]),
        ("Dành cho người đi làm", ["Tư vấn nghề nghiệp", "Xếp hạng MBA"])
    ]
    
    # Đặt các khối liên kết vào hàng 2 và 3
    for i, (header, links) in enumerate(link_blocks):
        # Header
        tk.Label(footer_frame, text=f"{header}", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=i, sticky="nw", pady=(20, 5))
        # Links
        for j, link in enumerate(links):
            tk.Label(footer_frame, text=link, font=("Arial", 9), fg="gray", bg="white").grid(row=3+j, column=i, sticky="nw")
            
    # Khối T&C, Data Copyright...
    tk.Label(footer_frame, text="Chính sách", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=3, sticky="nw", pady=(20, 5))
    tk.Label(footer_frame, text="Bản quyền dữ liệu", font=("Arial", 9), fg="gray", bg="white").grid(row=3, column=3, sticky="nw")
    tk.Label(footer_frame, text="Điều khoản và điều kiện", font=("Arial", 9), fg="gray", bg="white").grid(row=4, column=3, sticky="nw")
    
    # Khối Subscribe
    subscribe_frame = tk.Frame(footer_frame, bg="white")
    subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))
    
    tk.Label(subscribe_frame, text="Đăng ký nhận bản tin của chúng tôi", font=("Arial", 10, "bold"), bg="white").pack(anchor="e")
    
    input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1)
    input_frame.pack(anchor="e", pady=5)
    
    # Input field
    tk.Entry(input_frame, width=25, font=("Arial", 9), relief="flat", borderwidth=0, bg="white").pack(side="left", padx=5)
    
    subscribe_btn = tk.Button(input_frame, text="→",width=5, fg="white",bg= "#1F3AB0")
    subscribe_btn.pack(side="left")

    root.mainloop()

# if __name__ == "__main__":
#     create_ui()