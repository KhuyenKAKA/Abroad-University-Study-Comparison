import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os


class CombinedProfileUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UniCompare - Hồ sơ tổng hợp")
        self.root.geometry("1000x900")
        self.root.configure(bg="#f8f9fa")

        self.images_reference = []

        self.gender_var = tk.IntVar(value=0)
        self.create_main_layout()

    def create_main_layout(self):
        # 1. HEADER
        self.create_header()

        main_canvas = tk.Canvas(self.root, bg="#f8f9fa", highlightthickness=0)
        main_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # 2. Frame content
        content_frame = tk.Frame(main_canvas, bg="#f8f9fa")
        content_window = main_canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def on_conf(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))

        def on_resize(event):
            main_canvas.itemconfigure(content_window, width=event.width)

        def on_wheel(event):
            main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        content_frame.bind("<Configure>", on_conf)
        main_canvas.bind('<Configure>', on_resize)
        main_canvas.bind_all("<MouseWheel>", on_wheel)

        # 3. Form nhập liệu
        container = tk.Frame(content_frame, bg="#f5f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=120, pady=30)

        tk.Label(container, text="Hồ sơ người dùng", bg="#f5f7fa", fg="#1F3AB0",
                 font=("Segoe UI", 24, "bold")).pack(anchor="center", pady=(0, 30))

        # --- PHẦN I: THÔNG TIN CÁ NHÂN ---
        self.create_section_title(container, "I. THÔNG TIN CÁ NHÂN")

        profile_box = tk.Frame(container, bg="#f5f7fa")
        profile_box.pack(pady=20)

        cv = tk.Canvas(profile_box, width=100, height=100, bg="#f5f7fa", highlightthickness=0)
        cv.pack()
        cv.create_oval(0, 0, 100, 100, fill="#d0d0d0", outline="")
        cv.create_text(50, 45, text="👤", font=("Segoe UI", 40), fill="#999")
        cv.create_oval(70, 70, 100, 100, fill="white", outline="")
        cv.create_text(85, 85, text="📷", font=("Segoe UI", 12))

        p_form = tk.Frame(container, bg="#f5f7fa")
        p_form.pack(fill=tk.X)

        self.create_row_2_cols(p_form, "Họ*", "Tên*")
        self.create_row_2_cols(p_form, "Mã quốc gia*", "Số điện thoại*")

        email_row = tk.Frame(p_form, bg="#f5f7fa")
        email_row.pack(fill=tk.X, pady=10)
        self.create_input_field(email_row, "Email ID*").pack(fill=tk.X)

        g_row = tk.Frame(p_form, bg="#f5f7fa")
        g_row.pack(fill=tk.X, pady=15)
        tk.Label(g_row, text="GIỚI TÍNH", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(anchor="w",
                                                                                                      pady=(0, 5))
        tk.Radiobutton(g_row, text="Nam", variable=self.gender_var, value=0, bg="#f5f7fa").pack(side=tk.LEFT,
                                                                                                padx=(0, 20))
        tk.Radiobutton(g_row, text="Nữ", variable=self.gender_var, value=1, bg="#f5f7fa").pack(side=tk.LEFT)

        self.create_row_2_cols(p_form, "Ngày sinh (dd-mm-yyyy)", "Mã bưu điện")

        tk.Label(p_form, text="DÂN TỘC / NGÔN NGỮ", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(20, 5))
        self.create_row_2_cols(p_form, "Dân tộc", "Ngôn ngữ chính")
        self.create_row_2_cols(p_form, "Ngôn ngữ phụ", "Diện đặc biệt*")

        tk.Frame(container, bg="#ddd", height=2).pack(fill=tk.X, pady=40)

        # --- PHẦN II: LÝ LỊCH HỌC TẬP ---
        self.create_section_title(container, "II. LÝ LỊCH HỌC TẬP")

        a_form = tk.Frame(container, bg="#f5f7fa")
        a_form.pack(fill=tk.X)

        tk.Label(a_form, text="BẰNG CẤP TRƯỚC ĐÂY", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(0, 10))

        self.create_row_2_cols(a_form, "Trình độ cao nhất", "Chuyên ngành")

        row_3 = tk.Frame(a_form, bg="#f5f7fa")
        row_3.pack(fill=tk.X, pady=10)
        for i, txt in enumerate(["Xếp loại", "Điểm số (GPA)", "Năm tốt nghiệp"]):
            f = tk.Frame(row_3, bg="#f5f7fa")
            f.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0 if i == 0 else 15, 0))
            self.create_input_field(f, txt).pack(fill=tk.X)

        tk.Label(a_form, text="ĐIỂM THI HỌC THUẬT", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(20, 10))

        score_row_1 = tk.Frame(a_form, bg="#f5f7fa")
        score_row_1.pack(anchor="w", pady=5)
        for sub in ["ACT", "GMAT", "SAT", "CAT", "GRE", "STAT"]:
            self.create_small_score_box(score_row_1, sub, 8)

        score_row_2 = tk.Frame(a_form, bg="#f5f7fa")
        score_row_2.pack(anchor="w", pady=5)
        self.create_small_score_box(score_row_2, "International Baccalaureat", 25)

        tk.Label(a_form, text="ĐIỂM THI TIẾNG ANH", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(20, 10))
        eng_row = tk.Frame(a_form, bg="#f5f7fa")
        eng_row.pack(anchor="w", pady=5)
        self.create_small_score_box(eng_row, "IELTS", 10)
        self.create_small_score_box(eng_row, "TOEFL", 10)
        self.create_small_score_box(eng_row, "Pearson Test", 15)
        self.create_small_score_box(eng_row, "Cambridge Adv", 25)

        # Save Button
        tk.Frame(container, height=30, bg="#f5f7fa").pack()  # Spacer
        btn = tk.Button(container, text="LƯU HỒ SƠ", bg="#1F3AB0", fg="white",
                        font=("Segoe UI", 12, "bold"), bd=0, padx=50, pady=15, cursor="hand2",
                        command=lambda: messagebox.showinfo("Thông báo", "Lưu thông tin"))
        btn.pack(anchor="e", pady=(0, 20))

        # 4. FOOTER
        self.create_footer(content_frame)

    def create_header(self):
        nav_frame = tk.Frame(self.root, bg="white", height=50)
        nav_frame.pack(fill='x')

        # Logo
        tk.Label(nav_frame, text="UniCompare", font=("Segoe UI", 16, "bold"), fg="#1F3AB0", bg="white").pack(
            side=tk.LEFT, padx=(20, 40), pady=10)

        for item in ["Xếp hạng", "Khám phá", "Sự kiện", "Chuẩn bị", "Học bổng", "Chat với AI"]:
            tk.Button(nav_frame, text=item, font=("Segoe UI", 10), bg="white", relief="flat").pack(side=tk.LEFT,
                                                                                                   padx=10)

        right_nav = tk.Frame(nav_frame, bg="white")
        right_nav.pack(side=tk.RIGHT, padx=20)

        tk.Button(right_nav, text="Tư vấn miễn phí", fg='white', bg="#28a745", font=("Segoe UI", 10)).pack(side=tk.LEFT,
                                                                                                           padx=5)
        tk.Label(right_nav, text="🔍", font=("Segoe UI", 14), bg="white").pack(side=tk.LEFT, padx=10)
        tk.Label(right_nav, text="👤", font=("Segoe UI", 18), bg="white").pack(side=tk.LEFT, padx=10)

    def create_section_title(self, parent, text):
        f = tk.Frame(parent, bg="#E7EFFE", pady=10, padx=15)
        f.pack(fill=tk.X, pady=(10, 20))
        tk.Label(f, text=text, bg="#E7EFFE", fg="#1F3AB0", font=("Segoe UI", 13, "bold")).pack(anchor="w")

    def create_row_2_cols(self, parent, label1, label2):
        row = tk.Frame(parent, bg="#f5f7fa")
        row.pack(fill=tk.X, pady=10)

        c1 = tk.Frame(row, bg="#f5f7fa")
        c1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        self.create_input_field(c1, label1).pack(fill=tk.X)

        c2 = tk.Frame(row, bg="#f5f7fa")
        c2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 0))
        self.create_input_field(c2, label2).pack(fill=tk.X)

    def create_input_field(self, parent, label_text):
        tk.Label(parent, text=label_text, bg="#f5f7fa", fg="#666", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 5))
        entry = tk.Entry(parent, font=("Segoe UI", 10), bd=0, relief=tk.SOLID, highlightthickness=1,
                         highlightcolor="#ddd", highlightbackground="#ddd")
        entry.pack(ipady=8)  # ipady tạo chiều cao cho input
        return entry

    def create_small_score_box(self, parent, label_text, width=10):
        box = tk.Frame(parent, bg="#f5f7fa")
        box.pack(side="left", padx=(0, 15))
        tk.Label(box, text=label_text, bg="#f5f7fa", fg="#555", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 1))
        tk.Entry(box, font=("Segoe UI", 10), width=width, bd=0, relief=tk.SOLID, highlightthickness=1,
                 highlightcolor="#1F3AB0", highlightbackground="#ddd").pack(ipady=6)

    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="white", padx=50, pady=40)
        footer_frame.pack(fill='x', side='bottom', pady=(50, 0))

        for i in range(5):
            footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0)

        tk.Label(footer_frame, text="UniCompare", font=("Segoe UI", 14, "bold"), fg="#1e90ff", bg="white").grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky="nw")

        tk.Label(footer_frame, text="© QS Quacquarelli Symonds Limited 1994 - 2025.\nMọi quyền đã được bảo hộ.",
                 font=("Segoe UI", 8), fg="gray", bg="white", justify="left").grid(row=4, column=0, columnspan=2,
                                                                                   sticky="sw", pady=(50, 0))

        menu_headers = ["Về chúng tôi", "Liên hệ", "Quyền riêng tư", "Người dùng"]
        for col, header in enumerate(menu_headers):
            tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=col + 1,
                                                                                                sticky="w")

        social_frame = tk.Frame(footer_frame, bg="white")
        social_frame.grid(row=0, column=4, sticky="e")

        tk.Label(social_frame, text="Theo dõi chúng tôi", font=("Segoe UI", 10, "bold"), bg="white").pack(side="left",
                                                                                                          padx=(0, 10))

        social_icons = [
            "Abroad-University-Study-Comparison/assets/104498_facebook_icon.png",
            "Abroad-University-Study-Comparison/assets/1161953_instagram_icon.png",
            "Abroad-University-Study-Comparison/assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
            "Abroad-University-Study-Comparison/assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"
        ]

        for icon_path in social_icons:
            try:
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                else:
                    short_path = icon_path.split("/")[-1]
                    alt_path = f"assets/{short_path}"
                    if os.path.exists(alt_path):
                        img = Image.open(alt_path)
                    else:
                        raise FileNotFoundError

                img = img.resize((15, 15), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                icon_label = tk.Label(social_frame, image=photo, bg="#007bff", width=15, height=15)
                icon_label.pack(side="left", padx=3)

                self.images_reference.append(photo)

            except Exception:
                tk.Label(social_frame, text="[Icon]", font=("Segoe UI", 8), bg="#eee").pack(side="left", padx=3)

        link_blocks = [
            ("Dành cho sinh viên", ["Tìm kiếm khóa học", "Học bổng", "Sự kiện"]),
            ("Dành cho tổ chức", ["Danh sách khóa học", "Quảng cáo"]),
            ("Dành cho người đi làm", ["Tư vấn nghề nghiệp", "Xếp hạng MBA"])
        ]

        for i, (header, links) in enumerate(link_blocks):
            tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=i,
                                                                                                sticky="nw",
                                                                                                pady=(20, 5))
            for j, link in enumerate(links):
                tk.Label(footer_frame, text=link, font=("Segoe UI", 9), fg="gray", bg="white").grid(row=3 + j, column=i,
                                                                                                    sticky="nw")

        tk.Label(footer_frame, text="Chính sách", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=3,
                                                                                                  sticky="nw",
                                                                                                  pady=(20, 5))
        tk.Label(footer_frame, text="Bản quyền dữ liệu", font=("Segoe UI", 9), fg="gray", bg="white").grid(row=3,
                                                                                                           column=3,
                                                                                                           sticky="nw")
        tk.Label(footer_frame, text="Điều khoản và điều kiện", font=("Segoe UI", 9), fg="gray", bg="white").grid(row=4,
                                                                                                                 column=3,
                                                                                                                 sticky="nw")

        subscribe_frame = tk.Frame(footer_frame, bg="white")
        subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))

        tk.Label(subscribe_frame, text="Đăng ký nhận bản tin của chúng tôi", font=("Segoe UI", 10, "bold"),
                 bg="white").pack(anchor="e")

        input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1)
        input_frame.pack(anchor="e", pady=5)

        tk.Entry(input_frame, width=25, font=("Segoe UI", 9), relief="flat", borderwidth=0, bg="white").pack(
            side="left", padx=5)
        tk.Button(input_frame, text="→", width=5, fg="white", bg="#1F3AB0", relief="flat").pack(side="left")


if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedProfileUI(root)
    root.mainloop()