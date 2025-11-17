import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class PersonalInfoForm:
    def __init__(self, root):
        self.root = root
        self.root.title("UniCompare - Lý lịch học tập")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f8f9fa")

        # Variables
        self.gender_var = tk.StringVar()
        self.different_nationality = tk.BooleanVar()
        self.images_reference = []

        # Create layout
        self.create_layout()

    def create_layout(self):
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

    
        # 2. Main layout
      
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

        container = tk.Frame(content_frame, bg="#f5f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        # Sidebar
        sidebar = tk.Frame(container, bg="#E7EFFE", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="> Tài khoản của tôi", bg="#E7EFFE", fg="#333",
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill=tk.X, padx=20, pady=(30, 20))

        menu_items_sidebar = [("Thông tin cá nhân", False), ("Lý lịch học tập", True), ("Cài đặt tài khoản", False)]
        for item, selected in menu_items_sidebar:
            bg_color = "#d0d7e5" if selected else "#E7EFFE"
            tk.Label(sidebar, text=item, bg=bg_color, fg="#333",
                     font=("Segoe UI", 10), anchor="w", pady=12).pack(fill=tk.X, padx=20, pady=2)

        submenu_items = ["> Đổi mật khẩu", "> Đăng xuất"]
        for item in submenu_items:
            tk.Label(sidebar, text=item, bg="#E7EFFE", fg="#555",
                     font=("Segoe UI", 9), anchor="w", pady=8).pack(fill=tk.X, padx=40, pady=1)

        # Main Content
        main_content = tk.Frame(container, bg="#f5f7fa")
        main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 40), pady=0)

        tk.Label(main_content, text="Lý lịch học tập", bg="#f5f7fa",
                 fg="#1a1a1a", font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(0, 25))

        # --- Bằng cấp ---
        tk.Label(main_content, text="BẰNG CẤP TRƯỚC ĐÂY", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        qual_frame = tk.Frame(main_content, bg="#f5f7fa")
        qual_frame.pack(fill=tk.X, pady=(0, 15))
        qual_frame.columnconfigure(0, weight=1)
        qual_frame.columnconfigure(1, weight=1)
        self.create_labeled_input(qual_frame, "Trình độ cao nhất", 0)
        self.create_labeled_input(qual_frame, "Chuyên ngành", 1)

        score_frame = tk.Frame(main_content, bg="#f5f7fa")
        score_frame.pack(fill=tk.X, pady=(0, 15))
        score_frame.columnconfigure(0, weight=1)
        score_frame.columnconfigure(1, weight=1)
        score_frame.columnconfigure(2, weight=1)
        self.create_labeled_input(score_frame, "Xếp loại", 0)
        self.create_labeled_input(score_frame, "Điểm số", 1)
        self.create_labeled_input(score_frame, "Năm tốt nghiệp", 2)

        # --- Điểm thi học thuật ---
        tk.Label(main_content, text="ĐIỂM THI HỌC THUẬT", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        test_frame1 = tk.Frame(main_content, bg="#f5f7fa")
        test_frame1.pack(anchor="w", pady=(0, 15))
        self.create_score_box(test_frame1, "ACT", width=8)
        self.create_score_box(test_frame1, "GMAT", width=8)
        self.create_score_box(test_frame1, "SAT", width=8)
        self.create_score_box(test_frame1, "CAT", width=8)
        self.create_score_box(test_frame1, "GRE", width=8)
        self.create_score_box(test_frame1, "STAT", width=8)

        test_frame2 = tk.Frame(main_content, bg="#f5f7fa")
        test_frame2.pack(anchor="w", pady=(0, 15))
        self.create_score_box(test_frame2, "International Baccalaureat", width=25)

        # --- Điểm thi tiếng Anh ---
        tk.Label(main_content, text="ĐIỂM THI TIẾNG ANH", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        english_frame = tk.Frame(main_content, bg="#f5f7fa")
        english_frame.pack(anchor="w", pady=(0, 15))
        self.create_score_box(english_frame, "IELTS", width=10)
        self.create_score_box(english_frame, "TOEFL", width=10)
        self.create_score_box(english_frame, "Pearson Test", width=15)
        self.create_score_box(english_frame, "Cambridge Advanced Test", width=25)

        tk.Button(main_content, text="Lưu thay đổi", bg="#1F3AB0", fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=35, pady=12,
                  cursor="hand2", command=self.save_changes).pack(anchor="e", pady=(20, 0))

        # Footer
        self.create_new_footer(content_frame)

    
    def create_score_box(self, parent, label_text, width=10):
        container = tk.Frame(parent, bg="#f5f7fa")
        container.pack(side="left", padx=(0, 15))

        tk.Label(container, text=label_text, bg="#f5f7fa", fg="#555",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 1))

        entry = tk.Entry(container, font=("Segoe UI", 10), width=width, bd=0,
                         relief=tk.SOLID, highlightthickness=1,
                         highlightcolor="#1F3AB0", highlightbackground="#ddd")
        entry.pack(fill=tk.X, ipady=6)
        return entry

    def create_labeled_input(self, parent, label_text, column):
        container = tk.Frame(parent, bg="#f5f7fa")
        col_padx = (0, 0) if column == 0 else (15, 0)
        container.grid(row=0, column=column, sticky="ew", padx=col_padx)

     
        tk.Label(container, text=label_text, bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9), anchor="w").pack(anchor="w", pady=(0, 1))

        entry = tk.Entry(container, font=("Segoe UI", 10), bd=0, relief=tk.SOLID,
                         highlightthickness=1, highlightcolor="#ddd", highlightbackground="#ddd")
        entry.pack(fill=tk.X, ipady=10)
        return entry

    def create_new_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="white", padx=50, pady=40)
        footer_frame.pack(fill='x', side='bottom', pady=(20, 0))

        for i in range(5):
            footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0)

        tk.Label(footer_frame, text="UniCompare", font=("Segoe UI", 14, "bold"), fg="#1F3AB0", bg="white").grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky="nw")
        tk.Label(footer_frame, text="© UC Quacquarelli Symonds Limited 1994 - 2025. All rights reserved.",
                 font=("Segoe UI", 7), fg="gray", bg="white").grid(row=4, column=0, columnspan=2, sticky="sw",
                                                                   pady=(50, 0))

        menu_headers = ["About", "Contact", "Privacy", "Users"]
        for col, header in enumerate(menu_headers):
            tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=col + 1,
                                                                                                sticky="w")

        social_frame = tk.Frame(footer_frame, bg="white")
        social_frame.grid(row=0, column=4, sticky="e")
        tk.Label(social_frame, text="Follow us", font=("Segoe UI", 10, "bold"), bg="white").pack(side="left",
                                                                                                 padx=(0, 10))

        social_texts = ["FB", "IG", "IN", "X"]
        for txt in social_texts:
            tk.Label(social_frame, text=txt, bg="#1F3AB0", fg="white", width=3).pack(side="left", padx=2)

        link_blocks = [("For Students", ["Find courses", "Scholarships", "Events"]),
                       ("For Institution", ["List courses", "Advertise"]),
                       ("For Professionals", ["Career advice", "MBA rankings"])]
        for i, (header, links) in enumerate(link_blocks):
            tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=i,
                                                                                                sticky="nw",
                                                                                                pady=(20, 5))
            for j, link in enumerate(links):
                tk.Label(footer_frame, text=link, font=("Segoe UI", 9), fg="gray", bg="white").grid(row=3 + j, column=i,
                                                                                                    sticky="nw")

        tk.Label(footer_frame, text="Cookies", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=3,
                                                                                               sticky="nw",
                                                                                               pady=(20, 5))
        tk.Label(footer_frame, text="Data Copyright", font=("Segoe UI", 9), fg="gray", bg="white").grid(row=3, column=3,
                                                                                                        sticky="nw")
        tk.Label(footer_frame, text="Terms & Conditions", font=("Segoe UI", 9), fg="gray", bg="white").grid(row=4,
                                                                                                            column=3,
                                                                                                            sticky="nw")

        subscribe_frame = tk.Frame(footer_frame, bg="white")
        subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))
        tk.Label(subscribe_frame, text="Subscribe to our newsletter", font=("Segoe UI", 10, "bold"), bg="white").pack(
            anchor="e")
        input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1)
        input_frame.pack(anchor="e", pady=5)
        tk.Entry(input_frame, width=25, font=("Segoe UI", 9), relief="flat", borderwidth=0, bg="white").pack(
            side="left", padx=5)
        tk.Button(input_frame, text="→", width=5, fg="white", bg="#1F3AB0").pack(side="left")

    def save_changes(self):
        messagebox.showinfo("Thành công", "Đã lưu thay đổi thành công!")


def main():
    root = tk.Tk()
    app = PersonalInfoForm(root)
    root.mainloop()


if __name__ == "__main__":
    main()