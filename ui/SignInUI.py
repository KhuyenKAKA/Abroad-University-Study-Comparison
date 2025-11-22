
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PIL import Image, ImageTk
from ui.session import session
from ui.HomePageUI import create_ui as home_page_ui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controller.AuthController import AuthController
def open_main_menu():
    if session["role_type"] == 2:
        #adminui()
        return
    else:
        home_page_ui()

def create_ui():
    root = tk.Tk()
    root.title("UniCompare - Course Recommendation")
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
        # img = Image.open("Abroad-University-Study-Comparison/assets/search.png")
        img = Image.open("assets/search.png")
        img = img.resize((24, 24), Image.LANCZOS)
        search_photo = ImageTk.PhotoImage(img)
        tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
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
    images_reference = []
    
    
    # Thiết lập trọng số cột cho main_frame để chia không gian
    content_frame.grid_columnconfigure(0, weight=1) # Cột 0 (Trái) mở rộng
    content_frame.grid_columnconfigure(1, weight=1) # Cột 1 (Phải) mở rộng

    body_frame = tk.Frame(content_frame)
    body_frame.pack(fill='x')
    left_padding = tk.Frame(body_frame)
    left_padding.grid(row=0,column=0,padx=200)
    # --- Phần 2: Cột bên trái (Thông tin khuyến khích) ---
    left_frame = ttk.Frame(body_frame, padding="30", style='Left.TFrame')
    # left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid(row=0,column=1)
    # Định nghĩa style cho khung bên trái
    style = ttk.Style()
    style.configure('Left.TFrame', background='#7EA6F2') # Màu nền xanh nhạt
    
    # Tiêu đề
    title_label = ttk.Label(left_frame, text="Đến lúc nắm quyền\nkiểm soát tương lai\ncủa bạn", 
                            font=("Arial", 16, "bold"), 
                            background='#7EA6F2', 
                            foreground="#333")
    title_label.pack(pady=(50, 20), anchor='w')

    # Các điểm bullet
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
        
    # Thêm một khoảng trống để mô phỏng vị trí hình ảnh
    ttk.Label(left_frame, background='#7EA6F2').pack(pady=40, fill='x')


    # --- Phần 3: Cột bên phải (Form Đăng nhập) ---
    right_frame = ttk.Frame(body_frame, padding="30")
    # right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid(row=0,column=2)
    
    # Hàng 0: Tiêu đề "Đăng nhập"
    signin_title = ttk.Label(right_frame, text="Đăng nhập", font=("Arial", 18, "bold"))
    signin_title.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky='w')
    
    # Hàng 1: Mô tả
    desc_label = ttk.Label(right_frame, text="Nhập email đã đăng ký để đăng nhập hoặc\nĐăng ký để bắt đầu", 
                          font=("Arial", 9), foreground="#666", wraplength=350)
    desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky='w')

    # --- Các trường nhập liệu ---
    labels = ["Email*", "Mật khẩu*"]
    entries = []
    
    for i, label_text in enumerate(labels):
        label = ttk.Label(right_frame, text=label_text, font=("Arial", 9))
        label.grid(row=2 + i*2, column=0, columnspan=2, pady=(10, 2), sticky='w')
        
        # Nếu là trường mật khẩu, hiển thị dấu sao
        if i == 1:  # Password field
            entry = ttk.Entry(right_frame, width=40, show="*")
        else:
            entry = ttk.Entry(right_frame, width=40)
        
        entry.grid(row=3 + i*2, column=0, columnspan=2, pady=(0, 5), sticky='ew', ipady=5)
        entries.append(entry)
    
    # Hàng 7: Link "Quên mật khẩu?"
    forgot_button = tk.Button(right_frame, text="Quên mật khẩu?", fg="#1F3AB0", bg="white", 
                             bd=0, font=("Arial", 8), cursor="hand2",
                             command=lambda: messagebox.showinfo("Thông tin", "Tính năng quên mật khẩu"))
    forgot_button.grid(row=6, column=0, columnspan=2, pady=(5, 15), sticky='e')

    # Hàng 8: Nút "Đăng nhập"
    def on_signin_click():
        email = entries[0].get()
        password = entries[1].get()
        
        # Gọi controller để kiểm tra đăng nhập
        success, message = AuthController.login(email, password)
        
        if success:
            messagebox.showinfo("Thành công", message)
            root.destroy()
            open_main_menu()
            entries[0].delete(0, tk.END)
            entries[1].delete(0, tk.END)
        else:
            messagebox.showerror("Lỗi", message)
        return
    
    signin_button = tk.Button(right_frame, text="Đăng nhập", bg="#1F3AB0", fg="white", 
                             font=("Arial", 11, "bold"), bd=0, padx=10, pady=8, 
                             command=on_signin_click)
    signin_button.grid(row=7, column=0, columnspan=2, pady=(10, 15), sticky='ew', padx=5)
    
    # Hàng 9: Dòng OR
    ttk.Separator(right_frame, orient='horizontal').grid(row=8, column=0, columnspan=2, sticky='ew', pady=(10, 10))
    ttk.Label(right_frame, text="OR", anchor='center', font=("Arial", 8)).grid(row=8, column=0, columnspan=2)
    ttk.Separator(right_frame, orient='horizontal').grid(row=9, column=0, columnspan=2, sticky='ew', pady=(10, 15))

    # Hàng 10: Link "Đăng ký"
    signup_frame = ttk.Frame(right_frame)
    signup_frame.grid(row=10, column=0, columnspan=2, pady=(10, 0), sticky='w')
    
    dont_have_label = ttk.Label(signup_frame, text="Bạn chưa có tài khoản?", font=("Arial", 9))
    dont_have_label.pack(side=tk.LEFT)
    
    def go_to_signup():
        from ui.SignUpUI import create_ui as create_signup_ui
        root.destroy()  # Đóng cửa sổ đăng nhập
        create_signup_ui()  # Mở cửa sổ đăng ký
    
    signup_button = tk.Button(signup_frame, text="Đăng ký", fg="#1F3AB0", bg="white", 
                             bd=0, font=("Arial", 9), cursor="hand2",
                             command=go_to_signup)
    signup_button.pack(side=tk.LEFT, padx=(5, 0))
    


    # ===============================================
    # Phần Footer
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
    # social_icons = ["Abroad-University-Study-Comparison/assets/104498_facebook_icon.png", 
    #                 "Abroad-University-Study-Comparison/assets/1161953_instagram_icon.png", 
    #                 "Abroad-University-Study-Comparison/assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
    #                 "Abroad-University-Study-Comparison/assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    social_icons = ["assets/104498_facebook_icon.png", 
                    "assets/1161953_instagram_icon.png", 
                    "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
                    "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    
    for icon in social_icons:
        img = Image.open(icon)
        img = img.resize((15, 15), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        icon_label = tk.Label(social_frame, image=photo, bg="#007bff", width=15, height=15) 
        icon_label.pack(side="left", padx=3)
        images_reference.append(photo)
        
    # Các khối liên kết chính
    link_blocks = [
        ("For Students", ["Find courses", "Scholarships", "Events"]),
        ("For Institution", ["List courses", "Advertise"]),
        ("For Professionals", ["Career advice", "MBA rankings"])
    ]
    
    # Đặt các khối liên kết vào hàng 2 và 3
    for i, (header, links) in enumerate(link_blocks):
        # Header
        tk.Label(footer_frame, text=f"{header}", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=i, sticky="nw", pady=(20, 5))
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

if __name__ == "__main__":
    create_ui()
