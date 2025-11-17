import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class PersonalInfoForm:
    def __init__(self, root):
        self.root = root
        self.root.title("UniCompare - Thông tin cá nhân")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f8f9fa")

        # Variables
        self.gender_var = tk.StringVar()
        self.different_nationality = tk.BooleanVar()
        self.images_reference = []  # Giữ tham chiếu đến ảnh

        # Create layout
        self.create_layout()

    def create_layout(self):
        # ===============================================
        # 1. NEW NAVIGATION BAR
        # ===============================================
        nav_frame = tk.Frame(self.root, bg="white", height=50)
        nav_frame.pack(fill='x', padx=0, pady=0)

        nav_frame.grid_columnconfigure(0, weight=0)
        nav_frame.grid_columnconfigure(1, weight=1)
        for i in range(2, 8):
            nav_frame.grid_columnconfigure(i, weight=0)

        tk.Label(nav_frame, text="UniCompare", font=("Segoe UI", 16, "bold"), fg="#1F3AB0", bg="white").grid(
            row=0, column=0, padx=(20, 50), pady=10)

        menu_items = ["Rankings", "Discover", "Events", "Prepare", "Scholarships", "Chat To Students"]
        for i, item in enumerate(menu_items):
            tk.Button(nav_frame, text=item, font=("Segoe UI", 10), bg="white", relief="flat", cursor="hand2").grid(
                row=0, column=i + 1, padx=5, pady=10, sticky="e")

        right_nav_frame = tk.Frame(nav_frame, bg="white")
        right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))


        tk.Button(right_nav_frame, text="Free Counselling", foreground='white', background="#1F3AB0",
                  font=("Segoe UI", 10)).pack(side='left', padx=5)

        try:
            img = Image.open("assets/search.png")
            img = img.resize((24, 24), Image.LANCZOS)
            search_photo = ImageTk.PhotoImage(img)
            tk.Button(right_nav_frame, image=search_photo, bg='white', relief='flat').pack(side='left', padx=5)
            self.images_reference.append(search_photo)
        except:
            tk.Label(right_nav_frame, text="🔍", font=("Segoe UI", 16), bg="white").pack(side='left', padx=5)

        tk.Label(right_nav_frame, text="👤", font=("Segoe UI", 20), bg="white", fg="#444").pack(side='left', padx=10)

        # ===============================================
        # 2. Main Canvas with Scrollbar
        # ===============================================
        main_canvas = tk.Canvas(self.root, bg="#f8f9fa", highlightthickness=0)
        main_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        main_canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = tk.Frame(main_canvas, bg="#f8f9fa")
        content_window = main_canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            main_canvas.itemconfigure(content_window, width=main_canvas.winfo_width())

        def on_canvas_resize(event):
            main_canvas.itemconfigure(content_window, width=event.width)

        def on_mouse_wheel(event):
            main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        content_frame.bind("<Configure>", on_frame_configure)
        main_canvas.bind('<Configure>', on_canvas_resize)

        main_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        main_canvas.bind_all("<Button-4>", on_mouse_wheel)
        main_canvas.bind_all("<Button-5>", on_mouse_wheel)

        # ===============================================
        # 3. Personal Info Content
        # ===============================================
        container = tk.Frame(content_frame, bg="#f5f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        sidebar = tk.Frame(container, bg="#E7EFFE", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="> Tài khoản của tôi", bg="#E7EFFE", fg="#333",
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill=tk.X, padx=20, pady=(30, 20))

        menu_items_sidebar = [
            ("Thông tin cá nhân", True),
            ("Lý lịch học tập", False),
            ("Cài đặt tài khoản", False)
        ]

        for item, selected in menu_items_sidebar:
            bg_color = "#d0d7e5" if selected else "#E7EFFE"
            tk.Label(sidebar, text=item, bg=bg_color, fg="#333",
                     font=("Segoe UI", 10), anchor="w", pady=12).pack(fill=tk.X, padx=20, pady=2)

        submenu_items = ["> Đổi mật khẩu", "> Đăng xuất"]
        for item in submenu_items:
            tk.Label(sidebar, text=item, bg="#E7EFFE", fg="#555",
                     font=("Segoe UI", 9), anchor="w", pady=8).pack(fill=tk.X, padx=40, pady=1)

        main_content = tk.Frame(container, bg="#f5f7fa")
        main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 40), pady=0)

        tk.Label(main_content, text="Thông tin cá nhân", bg="#f5f7fa",
                 fg="#1a1a1a", font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(0, 25))

        profile_container = tk.Frame(main_content, bg="#f5f7fa")
        profile_container.pack(anchor="w", pady=(0, 25))

        avatar_size = 100
        canvas = tk.Canvas(profile_container, width=avatar_size, height=avatar_size,
                           bg="#f5f7fa", highlightthickness=0)
        canvas.pack()

        canvas.create_oval(0, 0, avatar_size, avatar_size, fill="#d0d0d0", outline="")
        canvas.create_text(avatar_size // 2, avatar_size // 2 - 10,
                           text="👤", font=("Segoe UI", 40), fill="#999")

        camera_size = 30
        cam_x = avatar_size - camera_size // 2
        cam_y = avatar_size - camera_size // 2
        canvas.create_oval(cam_x - camera_size // 2, cam_y - camera_size // 2,
                           cam_x + camera_size // 2, cam_y + camera_size // 2,
                           fill="white", outline="")
        canvas.create_text(cam_x, cam_y, text="📷", font=("Segoe UI", 12), fill="black")

        form_frame = tk.Frame(main_content, bg="#f5f7fa")
        form_frame.pack(fill=tk.BOTH, expand=True)

        row1 = tk.Frame(form_frame, bg="#f5f7fa")
        row1.pack(fill=tk.X, pady=(0, 15))
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)
        self.create_labeled_input(row1, "Họ*", 0)
        self.create_labeled_input(row1, "Tên*", 1)

        row2 = tk.Frame(form_frame, bg="#f5f7fa")
        row2.pack(fill=tk.X, pady=(0, 15))
        row2.columnconfigure(0, weight=1)
        row2.columnconfigure(1, weight=1)
        self.create_labeled_input(row2, "Mã quốc gia*", 0)
        self.create_labeled_input(row2, "Số điện thoại*", 1)

        row3 = tk.Frame(form_frame, bg="#f5f7fa")
        row3.pack(fill=tk.X, pady=(0, 15))
        row3.columnconfigure(0, weight=1)
        self.create_labeled_input(row3, "Email ID*", 0)

        gender_frame = tk.Frame(form_frame, bg="#f5f7fa")
        gender_frame.pack(fill=tk.X, pady=(10, 15), anchor="w")
        tk.Label(gender_frame, text="GIỚI TÍNH", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 10))
        gender_buttons = tk.Frame(gender_frame, bg="#f5f7fa")
        gender_buttons.pack(anchor="w")
        tk.Radiobutton(gender_buttons, text="Nam", variable=self.gender_var, value="Male", bg="#f5f7fa",
                       font=("Segoe UI", 10), activebackground="#f5f7fa", selectcolor="#fff").pack(
            side=tk.LEFT, padx=(0, 30))
        tk.Radiobutton(gender_buttons, text="Nữ", variable=self.gender_var, value="Female", bg="#f5f7fa",
                       font=("Segoe UI", 10), activebackground="#f5f7fa", selectcolor="#fff").pack(
            side=tk.LEFT)

        row4 = tk.Frame(form_frame, bg="#f5f7fa")
        row4.pack(fill=tk.X, pady=(0, 15))
        row4.columnconfigure(0, weight=1)
        row4.columnconfigure(1, weight=1)
        self.create_labeled_input(row4, "Ngày sinh", 0)
        self.create_labeled_input(row4, "Mã bưu điện", 1)

        row5 = tk.Frame(form_frame, bg="#f5f7fa")
        row5.pack(fill=tk.X, pady=(0, 15))
        row5.columnconfigure(0, weight=1)
        row5.columnconfigure(1, weight=1)
        self.create_labeled_input(row5, "Tôi sống ở*", 0)

        check_container = tk.Frame(row5, bg="#f5f7fa")
        check_container.grid(row=0, column=1, sticky="w", padx=(15, 0))
        tk.Checkbutton(check_container, text="Đánh dấu nếu bạn có quốc tịch khác",
                       variable=self.different_nationality, bg="#f5f7fa",
                       font=("Segoe UI", 9), activebackground="#f5f7fa").pack(anchor="w", pady=(25, 0))

        tk.Label(form_frame, text="DÂN TỘC/ NGÔN NGỮ", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        row6 = tk.Frame(form_frame, bg="#f5f7fa")
        row6.pack(fill=tk.X, pady=(0, 15))
        row6.columnconfigure(0, weight=1)
        row6.columnconfigure(1, weight=1)
        self.create_labeled_input(row6, "Dân tộc", 0)
        self.create_labeled_input(row6, "Ngôn ngữ chính", 1)

        row7 = tk.Frame(form_frame, bg="#f5f7fa")
        row7.pack(fill=tk.X, pady=(0, 25))
        row7.columnconfigure(0, weight=1)
        row7.columnconfigure(1, weight=1)
        self.create_labeled_input(row7, "Ngôn ngữ phụ", 0)
        self.create_labeled_input(row7, "Diện đặc biệt*", 1)

        tk.Button(form_frame, text="Lưu thay đổi", bg="#1F3AB0", fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=35, pady=12,
                  cursor="hand2", command=self.save_changes).pack(anchor="e", pady=(10, 0))

        self.create_new_footer(content_frame)

    def create_labeled_input(self, parent, label_text, column):
        container = tk.Frame(parent, bg="#f5f7fa")
        container.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 15, 0))
        tk.Label(container, text=label_text, bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9), anchor="w").pack(anchor="w", pady=(0, 5))
        entry = tk.Entry(container, font=("Segoe UI", 10), bd=0, relief=tk.SOLID,
                         highlightthickness=1, highlightcolor="#ddd", highlightbackground="#ddd")
        entry.pack(fill=tk.X, ipady=10)
        return entry

    # =========================================================================
    # FOOTER
    # =========================================================================
    def create_new_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="white", padx=50, pady=40)
        footer_frame.pack(fill='x', side='bottom', pady=(20, 0))

        for i in range(5):
            footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0)

        tk.Label(footer_frame, text="UniCompare", font=("Segoe UI", 14, "bold"), fg="#1F3AB0",
                 bg="white").grid(row=0, column=0, sticky="nw")
        tk.Label(footer_frame,
                 text="© UC Quacquarelli Symonds Limited 1994 - 2025. All rights reserved.",
                 font=("Segoe UI", 7), fg="gray", bg="white").grid(row=4, column=0, columnspan=2, sticky="sw",
                                                               pady=(50, 0))

        menu_headers = ["About", "Contact", "Privacy", "Users"]
        for col, header in enumerate(menu_headers):
            tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"),
                     bg="white").grid(row=0, column=col + 1, sticky="w")

        social_frame = tk.Frame(footer_frame, bg="white")
        social_frame.grid(row=0, column=4, sticky="e")

        tk.Label(social_frame, text="Follow us", font=("Segoe UI", 10, "bold"),
                 bg="white").pack(side="left", padx=(0, 10))

        social_icons = [
            "assets/104498_facebook_icon.png",
            "assets/1161953_instagram_icon.png",
            "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
            "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"
        ]

        for icon_path in social_icons:
            try:
                img = Image.open(icon_path)
                img = img.resize((15, 15), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                icon_label = tk.Label(social_frame, image=photo, bg="#1F3AB0", width=15, height=15)
                icon_label.pack(side="left", padx=3)
                self.images_reference.append(photo)
            except Exception as e:
                print(f"Không thể tải icon {icon_path}: {e}")
                fallback_text = icon_path.split('_')[1][0].upper()
                tk.Label(social_frame, text=f" {fallback_text} ", bg="#1F3AB0", fg="white",
                         font=("Segoe UI", 8, "bold")).pack(side="left", padx=3)

        link_blocks = [
            ("For Students", ["Find courses", "Scholarships", "Events"]),
            ("For Institution", ["List courses", "Advertise"]),
            ("For Professionals", ["Career advice", "MBA rankings"])
        ]

        for i, (header, links) in enumerate(link_blocks):
            tk.Label(footer_frame, text=f"{header}", font=("Segoe UI", 10, "bold"),
                     bg="white").grid(row=2, column=i, sticky="nw", pady=(20, 5))
            for j, link in enumerate(links):
                tk.Label(footer_frame, text=link, font=("Segoe UI", 9), fg="gray",
                         bg="white").grid(row=3 + j, column=i, sticky="nw")

        tk.Label(footer_frame, text="Cookies", font=("Segoe UI", 10, "bold"),
                 bg="white").grid(row=2, column=3, sticky="nw", pady=(20, 5))
        tk.Label(footer_frame, text="Data Copyright", font=("Segoe UI", 9),
                 fg="gray", bg="white").grid(row=3, column=3, sticky="nw")
        tk.Label(footer_frame, text="Terms & Conditions", font=("Segoe UI", 9),
                 fg="gray", bg="white").grid(row=4, column=3, sticky="nw")

        subscribe_frame = tk.Frame(footer_frame, bg="white")
        subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))

        tk.Label(subscribe_frame, text="Subscribe to our newsletter",
                 font=("Arial", 10, "bold"), bg="white").pack(anchor="e")

        input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1)
        input_frame.pack(anchor="e", pady=5)

        tk.Entry(input_frame, width=25, font=("Segoe UIl", 9),
                 relief="flat", borderwidth=0,
                 bg="white").pack(side="left", padx=5)

        subscribe_btn = tk.Button(input_frame, text="→", width=5,
                                  fg="white", bg="#1F3AB0")
        subscribe_btn.pack(side="left")

    def save_changes(self):
        messagebox.showinfo("Thành công", "Đã lưu thay đổi thành công!")


def main():
    root = tk.Tk()
    app = PersonalInfoForm(root)
    root.mainloop()


if __name__ == "__main__":
    main()
