import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import ui.session as session_data
from controller.UserController import UserController
from controller.CountryController import CountryController
from controller.AuthController import AuthController
user_now = UserController.get_current_user()
from datetime import datetime, date
class PersonalInfoForm:
    def __init__(self, root):
        self.root = root
        self.user = UserController.get_current_user()
        print("Current user data:", self.user)

        self.root.title("UniCompare - Định hướng tương lai cùng bạn")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("1000x800")
        self.root.configure(bg="#f8f9fa")

        # Variables
        self.gender_var =  tk.IntVar()
        self.gender_var.set(0)  #
        self.different_nationality = tk.BooleanVar()
        self.images_reference = []
        self.is_submenu_visible = False

        #data
        self.first_name_entry = None
        self.last_name_entry = None
        self.email_entry = None
        self.phone_entry = None
        self.country_entry = None
        self.dob_entry = None
        self.postal_entry = None
        self.ethnic_entry = None
        self.main_lang_entry = None
        self.add_lang_entry = None
        self.special_entry =   None
        self.create_layout()

        self.fill_user_data()

    def create_layout(self):
        nav_frame = tk.Frame(self.root, bg="white", height=50)
        nav_frame.pack(fill='x', padx=0, pady=0)
        nav_frame.grid_columnconfigure(1, weight=1)

        tk.Label(nav_frame, text="UniCompare", font=("Segoe UI", 16, "bold"), fg="#1F3AB0", bg="white").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=(20,
                                                                                                                   50),
                                                                                                             pady=10)

        menu_items = ["Xếp hạng", "Khám phá", "Sự kiện", "Chuẩn bị", "Học bổng", "Chat với AI"]
        for i, item in enumerate(menu_items):
            tk.Button(nav_frame, text=item, font=("Segoe UI", 10), bg="white", relief="flat", cursor="hand2").grid(
                row=0, column=i + 1, padx=5, pady=10, sticky="e")

        right_nav = tk.Frame(nav_frame, bg="white")
        right_nav.grid(row=0, column=7, sticky="e", padx=(0, 20))
        tk.Button(right_nav, text="Tư vấn miễn phí", fg='white', bg="#28a745", font=("Segoe UI", 10)).pack(side='left',
                                                                                                            padx=5)

        try:
            img = Image.open("assets/search.png")
            img = img.resize((24, 24), Image.LANCZOS)
            search_photo = ImageTk.PhotoImage(img)
            tk.Button(right_nav, image=search_photo, bg='white', relief='flat').pack(side='left', padx=5)
            self.images_reference.append(search_photo)
        except:
            tk.Label(right_nav, text="🔍", font=("Segoe UI", 16), bg="white").pack(side='left', padx=5)
        tk.Label(right_nav, text="👤", font=("Segoe UI", 20), bg="white", fg="#444").pack(side='left', padx=10)

        # ===============================================
        # 2. SCROLL AREA
        # ===============================================
        main_canvas = tk.Canvas(self.root, bg="#f8f9fa", highlightthickness=0)
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        main_canvas.configure(yscrollcommand=scrollbar.set)

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

        container = tk.Frame(content_frame, bg="#f5f7fa")
        container.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        # ===============================================
        # 3. SIDEBAR
        # ===============================================
        sidebar = tk.Frame(container, bg="#E7EFFE", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="> Tài khoản của tôi", bg="#E7EFFE", fg="#333", font=("Segoe UI", 11, "bold"),
                 anchor="w").pack(fill=tk.X, padx=20, pady=(30, 20))

        menu_items_sidebar = [
            ("Thông tin cá nhân", True),
            ("Lý lịch học tập", False),
            ("Cài đặt tài khoản", False)
        ]

        for item_text, is_selected in menu_items_sidebar:
            bg_color = "#d0d7e5" if is_selected else "#E7EFFE"
            cmd = None

            if item_text == "Cài đặt tài khoản":
                cmd = self.toggle_submenu
            elif item_text == "Lý lịch học tập":
                cmd = self.open_academic_view

            tk.Button(sidebar, text=item_text, bg=bg_color, fg="#333",
                      font=("Segoe UI", 10), anchor="w", relief="flat",
                      padx=10, pady=12, cursor="hand2", command=cmd).pack(fill=tk.X, padx=20, pady=2)

        # Sub-menu Frame
        self.submenu_frame = tk.Frame(sidebar, bg="#E7EFFE")
        tk.Button(self.submenu_frame, text="> Đổi mật khẩu", bg="#E7EFFE", fg="#555", font=("Segoe UI", 9), anchor="w",
                  relief="flat", padx=10, pady=8, cursor="hand2", command=self.show_change_password).pack(fill=tk.X,
                                                                                                          padx=40,
                                                                                                          pady=1)
        tk.Button(self.submenu_frame, text="> Đăng xuất", bg="#E7EFFE", fg="#555", font=("Segoe UI", 9), anchor="w",
                  relief="flat", padx=10, pady=8, cursor="hand2", command=self.logout_action).pack(fill=tk.X, padx=40,
                                                                                                   pady=1)

        # ===============================================
        # 4. MAIN CONTENT
        # ===============================================
        # Lưu vào biến self.main_content để có thể xóa khi đổi mật khẩu
        self.main_content = tk.Frame(container, bg="#f5f7fa")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 40), pady=0)

        tk.Label(self.main_content, text="Thông tin cá nhân", bg="#f5f7fa", fg="#1a1a1a",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(0, 25))

        profile_container = tk.Frame(self.main_content, bg="#f5f7fa")
        profile_container.pack(anchor="w", pady=(0, 25))

        avatar_size = 100
        canvas = tk.Canvas(profile_container, width=avatar_size, height=avatar_size, bg="#f5f7fa", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(0, 0, avatar_size, avatar_size, fill="#d0d0d0", outline="")
        canvas.create_text(avatar_size // 2, avatar_size // 2 - 10, text="👤", font=("Segoe UI", 40), fill="#999")

        camera_size = 30
        cam_x = avatar_size - camera_size // 2
        cam_y = avatar_size - camera_size // 2
        canvas.create_oval(cam_x - camera_size // 2, cam_y - camera_size // 2, cam_x + camera_size // 2,
                           cam_y + camera_size // 2, fill="white", outline="")
        canvas.create_text(cam_x, cam_y, text="📷", font=("Segoe UI", 12), fill="black")

        form_frame = tk.Frame(self.main_content, bg="#f5f7fa")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # --- Enter ---
        row1 = tk.Frame(form_frame, bg="#f5f7fa")
        row1.pack(fill=tk.X, pady=(0, 15))
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)
        self.first_name_entry = self.create_labeled_input(row1, "Họ*", 0)
        self.last_name_entry = self.create_labeled_input(row1, "Tên*", 1)

        row2 = tk.Frame(form_frame, bg="#f5f7fa")
        row2.pack(fill=tk.X, pady=(0, 15))
        row2.columnconfigure(0, weight=1)
        row2.columnconfigure(1, weight=1)
        self.country_entry = self.create_labeled_input(row2, "Mã quốc gia*", 0)
        self.phone_entry = self.create_labeled_input(row2, "Số điện thoại*", 1)

        row3 = tk.Frame(form_frame, bg="#f5f7fa")
        row3.pack(fill=tk.X, pady=(0, 15))
        row3.columnconfigure(0, weight=1)
        self.email_entry = self.create_labeled_input(row3, "Email ID*", 0)

        gender_frame = tk.Frame(form_frame, bg="#f5f7fa")
        gender_frame.pack(fill=tk.X, pady=(10, 15), anchor="w")
        tk.Label(gender_frame, text="GIỚI TÍNH", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(anchor="w",
                                                                                                             pady=(0,
                                                                                                                   10))
        gender_buttons = tk.Frame(gender_frame, bg="#f5f7fa")
        gender_buttons.pack(anchor="w")
        tk.Radiobutton(gender_buttons, text="Nam", variable=self.gender_var, value=0, bg="#f5f7fa",
                       font=("Segoe UI", 10), activebackground="#f5f7fa", selectcolor="#fff").pack(side=tk.LEFT,
                                                                                                   padx=(0, 30))
        tk.Radiobutton(gender_buttons, text="Nữ", variable=self.gender_var, value=1, bg="#f5f7fa",
                       font=("Segoe UI", 10), activebackground="#f5f7fa", selectcolor="#fff").pack(side=tk.LEFT)

        row4 = tk.Frame(form_frame, bg="#f5f7fa")
        row4.pack(fill=tk.X, pady=(0, 15))
        row4.columnconfigure(0, weight=1)
        row4.columnconfigure(1, weight=1)
        self.dob_entry = self.create_labeled_input(row4, "Ngày sinh (dd-mm-yyyy)", 0)
        self.postal_entry = self.create_labeled_input(row4, "Mã bưu điện", 1)

        row5 = tk.Frame(form_frame, bg="#f5f7fa")
        row5.pack(fill=tk.X, pady=(0, 15))
        row5.columnconfigure(0, weight=1)
        row5.columnconfigure(1, weight=1)
 

        tk.Label(form_frame, text="DÂN TỘC/ NGÔN NGỮ", bg="#f5f7fa", fg="#666", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(10, 10))

        row6 = tk.Frame(form_frame, bg="#f5f7fa")
        row6.pack(fill=tk.X, pady=(0, 15))
        row6.columnconfigure(0, weight=1)
        row6.columnconfigure(1, weight=1)
        self.ethnic_entry = self.create_labeled_input(row6, "Dân tộc", 0)
        self.main_lang_entry = self.create_labeled_input(row6, "Ngôn ngữ chính", 1)

        row7 = tk.Frame(form_frame, bg="#f5f7fa")
        row7.pack(fill=tk.X, pady=(0, 25))
        row7.columnconfigure(0, weight=1)
        row7.columnconfigure(1, weight=1)
        self.add_lang_entry = self.create_labeled_input(row7, "Ngôn ngữ phụ", 0)
        self.special_entry = self.create_labeled_input(row7, "Diện đặc biệt*", 1)

        tk.Button(form_frame, text="Lưu thay đổi", bg="#1F3AB0", fg="white", font=("Segoe UI", 10, "bold"), bd=0,
                  padx=35, pady=12, cursor="hand2", command=self.save_changes).pack(anchor="e", pady=(10, 0))

        # FOOTER
        self.create_new_footer(content_frame)


    def create_labeled_input(self, parent, label_text, column):
        container = tk.Frame(parent, bg="#f5f7fa")
        container.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 15, 0))
        tk.Label(container, text=label_text, bg="#f5f7fa", fg="#666", font=("Segoe UI", 9), anchor="w").pack(anchor="w",
                                                                                                             pady=(0,
                                                                                                                   5))
        entry = tk.Entry(container, font=("Segoe UI", 10), bd=0, relief=tk.SOLID, highlightthickness=1,
                         highlightcolor="#ddd", highlightbackground="#ddd")
        entry.pack(fill=tk.X, ipady=10)
        return entry

    # def create_labeled_input(self, parent, label_text, column, variable): # Thêm tham số variable
    #     container = tk.Frame(parent, bg="#f5f7fa")
    #     container.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 15, 0))
    #     tk.Label(container, text=label_text, bg="#f5f7fa", fg="#666", font=("Segoe UI", 9), anchor="w").pack(
    #         anchor="w",
    #         pady=(0, 5)
    #     )
    #     entry = tk.Entry(container, 
    #                     font=("Segoe UI", 10), 
    #                     bd=0, 
    #                     relief=tk.SOLID, 
    #                     highlightthickness=1,
    #                     highlightcolor="#ddd", 
    #                     highlightbackground="#ddd",
    #                     textvariable=variable) # ⬅️ Gán StringVar vào đây
    #     entry.pack(fill=tk.X, ipady=10)
    #     return entry

    def create_new_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="white", padx=50, pady=40)
        footer_frame.pack(fill='x', side='bottom', pady=(20, 0))
        for i in range(5): footer_frame.grid_columnconfigure(i, weight=1 if i > 0 else 0)

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
        for txt in social_texts: tk.Label(social_frame, text=txt, bg="#1F3AB0", fg="white", width=3).pack(side="left",
                                                                                                          padx=2)

        link_blocks = [("For Students", ["Find courses", "Scholarships", "Events"]),
                       ("For Institution", ["List courses", "Advertise"]),
                       ("For Professionals", ["Career advice", "MBA rankings"])]
        for i, (header, links) in enumerate(link_blocks):
            tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=i,
                                                                                                sticky="nw",
                                                                                                pady=(20, 5))
            for j, link in enumerate(links): tk.Label(footer_frame, text=link, font=("Segoe UI", 9), fg="gray",
                                                      bg="white").grid(row=3 + j, column=i, sticky="nw")

        tk.Label(footer_frame, text="Cookies", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=3,
                                                                                               sticky="nw",
                                                                                               pady=(20, 5))
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


    def toggle_submenu(self):
        if self.is_submenu_visible:
            self.submenu_frame.pack_forget()
            self.is_submenu_visible = False
        else:
            self.submenu_frame.pack(fill='x', anchor='n')
            self.is_submenu_visible = True

    def logout_action(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?"):
            AuthController.logout()
            from ui.HomePageUI import create_ui as create_ui
            self.root.destroy()
            create_ui()
            print(session_data.session)

    # 
    def show_change_password(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        tk.Label(self.main_content, text="Đổi mật khẩu",
                bg="#f5f7fa", font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(0, 25))

        pass_form = tk.Frame(self.main_content, bg="#f5f7fa")
        pass_form.pack(fill='both', expand=True)

        labels = ["Mật khẩu hiện tại*", "Mật khẩu mới*", "Xác nhận mật khẩu mới*"]
        self.password_entries = []  # LƯU ENTRY LẠI

        for label in labels:
            container = tk.Frame(pass_form, bg="#f5f7fa")
            container.pack(fill=tk.X, pady=(0, 15))

            tk.Label(container, text=label, bg="#f5f7fa", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 5))

            entry = tk.Entry(container, show="*", font=("Segoe UI", 10),
                            relief="solid", bd=0, highlightthickness=1)
            entry.pack(fill="x", ipady=10)

            self.password_entries.append(entry)

        tk.Button(
            pass_form,
            text="Cập nhật",
            bg="#1F3AB0",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=35,
            pady=12,
            command=self.update_password
        ).pack(anchor="w", pady=20)

    def update_password(self):
        current_pw = self.password_entries[0].get().strip()
        new_pw = self.password_entries[1].get().strip()
        confirm_pw = self.password_entries[2].get().strip()

        # 1. Kiểm tra nhập đủ
        if not current_pw or not new_pw or not confirm_pw:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        # 2. Kiểm tra xác nhận mật khẩu
        if new_pw != confirm_pw:
            messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận không khớp.")
            return

        # 3. Lấy hash mật khẩu hiện tại từ DB
        user_id = session_data.session.get("user_id")
        user_pass = UserController.get_pass_by_id(user_id)
        if not user_pass:
            messagebox.showerror("Lỗi", "Không tìm thấy tài khoản.")
            return

        stored_hashed_pw = user_pass['password']  # mật khẩu hash trong DB

        # 4. Xác thực mật khẩu hiện tại
        if not UserController.verify_password(current_pw, stored_hashed_pw):
            messagebox.showerror("Lỗi", "Mật khẩu hiện tại không chính xác.")
            return

        # 5. Hash mật khẩu mới
        new_hashed_pw = UserController.hash_password(new_pw)

        # 6. Update mật khẩu trong DB
        success, msg = UserController.update_password(user_id, new_hashed_pw)
        if not success:
            messagebox.showerror("Lỗi", f"Cập nhật mật khẩu thất bại: {msg}")
            return
        else:
            messagebox.showinfo("Thành công",msg)

    def open_academic_view(self):
        try:
            from PersonalBgUI import AcademicInfoForm
            AcademicInfoForm(self.root)
        except ImportError:
            messagebox.showerror("Lỗi", "Không tìm thấy file education.py")

    def fill_user_data(self):
        """Populate entries from self.user (dict) if available"""
        if not self.user:
            return
        u = self.user
        # user dict keys are expected to match DB columns
        try:
            if u.get('first_name') is not None:
                self.first_name_entry.delete(0, tk.END)
                self.first_name_entry.insert(0, u.get('first_name') or "")


            if u.get('last_name') is not None:
                self.last_name_entry.delete(0, tk.END)
                self.last_name_entry.insert(0, u.get('last_name') or "")


            if u.get('email') is not None:
                self.email_entry.delete(0, tk.END)
                self.email_entry.insert(0, u.get('email') or "")


            if u.get('phone_number') is not None:
                self.phone_entry.delete(0, tk.END)
                self.phone_entry.insert(0, u.get('phone_number') or "")


            if u.get('country_id') is not None:
                self.country_entry.delete(0, tk.END)
                c_id = u.get('country_id')
                country_name = CountryController.get_name_by_id(c_id)
                print("country_name:", country_name)
                self.country_entry.insert(0, str(country_name['name'] or ""))


            if u.get('gender'):
                self.gender_var.set(u.get('gender'))


            if u.get('dob') is not None:
                self.dob_entry.delete(0, tk.END)
                date_str = convert_date_ymd_to_dmy(u.get('dob'))
                print("Converted date:", date_str)
                self.dob_entry.insert(0, str(convert_date_ymd_to_dmy(u.get('dob'))or ""))


            if u.get('postal_code') is not None:
                self.postal_entry.delete(0, tk.END)
                self.postal_entry.insert(0, u.get('postal_code') or "")


            if u.get('ethnic_group') is not None:
                self.ethnic_entry.delete(0, tk.END)
                self.ethnic_entry.insert(0, u.get('ethnic_group') or "")


            if u.get('main_lang') is not None:
                self.main_lang_entry.delete(0, tk.END)
                self.main_lang_entry.insert(0, u.get('main_lang') or "")


            if u.get('add_lang') is not None:
                self.add_lang_entry.delete(0, tk.END)
                self.add_lang_entry.insert(0, u.get('add_lang') or "")


            if u.get('special') is not None:
                self.special_entry.delete(0, tk.END)
                self.special_entry.insert(0, u.get('special') or "")
        except Exception as e:
            print("Lỗi khi fill dữ liệu user:", e)
    
    def save_changes(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()

        if email:
            existing_user = UserController.get_user_by_email(email)
            if existing_user and (not self.user or existing_user != self.user.get('id')):
                messagebox.showerror("Lỗi", "Email đã được sử dụng bởi người dùng khác.")
                return
        if not first_name or not last_name or not email:
            messagebox.showerror("Lỗi", "Họ, tên và email là bắt buộc.")
            return
        country_name = self.country_entry.get().strip()
        country_id = None
        if country_name:
            country_id = CountryController.get_id_by_name(country_name)
            if isinstance(country_id, dict):
                 country_id = country_id.get("id")
        dob = None 
        if self.dob_entry.get().strip():
            try:
                dob = self.dob_entry.get().strip()
                day, month, year = map(int, dob.split('-'))
                dob = datetime(year, month, day).date()
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày sinh không đúng định dạng dd-mm-yyyy.")
                return
        payload = {
        'id': self.user.get('id') if self.user else None,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number': self.phone_entry.get().strip(),
        'country_id': country_id,
        'gender': int(self.gender_var.get()),
        'dob': dob,
        'postal_code': self.postal_entry.get().strip(),
        'ethnic_group': self.ethnic_entry.get().strip(),
        'main_lang': self.main_lang_entry.get().strip(),
        'add_lang': self.add_lang_entry.get().strip(),
        'special': self.special_entry.get().strip()
        }
        print("Payload to update:", payload)
         # Call controller to update
        success, msg = UserController.update_user(payload)

        if success:
            messagebox.showinfo("Thành công", msg)
            self.user = UserController.get_current_user()
            self.fill_user_data()
        else:
            messagebox.showerror("Lỗi", msg)

    # ví dụ thêm:

def convert_date_ymd_to_dmy(dob):
    """Chuyển YYYY-MM-DD -> DD/MM/YYYY, hỗ trợ cả datetime.date và datetime"""
    if dob is None:
        return ""

    # Nếu là kiểu datetime.date hoặc datetime
    if isinstance(dob, (datetime, date)):
        return dob.strftime("%d-%m-%Y")

    # Nếu là chuỗi
    if isinstance(dob, str):
        try:
            parsed = datetime.strptime(dob, "%Y-%m-%d")
            return parsed.strftime("%d-%m-%Y")
        except ValueError:
            return ""  # sai format chuỗi
    return ""

def main():
    root = tk.Tk()
    app = PersonalInfoForm(root)
    root.mainloop()


if __name__ == "__main__":
    main()