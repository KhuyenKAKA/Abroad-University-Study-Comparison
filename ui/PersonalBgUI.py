import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import ui.session as session_data
from controller.StudyBGController import StudyBGController
from controller.UserController import UserController 
from controller.AuthController import AuthController
class AcademicInfoForm:
    def __init__(self, root):
        self.root = root
        self.root.title("UniCompare - Lý lịch học tập")
        self.study_bg = StudyBGController.get_current_user_bg()
        print("Loaded study background:", self.study_bg)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.configure(bg="#f8f9fa")
        self.is_submenu_visible = False
        self.images_reference = []
        self.level_entry = None
        self.major_entry = None
        self.academic_rate_entry = None
        self.gpa_entry = None       
        self.graduate_year_entry = None
        self.act_entry = None
        self.gmat_entry = None
        self.sat_entry = None
        self.cat_entry = None
        self.gre_entry = None
        self.stat_entry = None
        self.inter_bac_entry = None
        self.ielts_entry = None
        self.toefl_entry = None
        self.pearson_entry = None
        self.cam_entry = None
        self.create_layout()
        self.fill_data()

    def create_layout(self):
        nav_frame = tk.Frame(self.root, bg="white", height=50)
        nav_frame.pack(fill='x', padx=0, pady=0)
        nav_frame.grid_columnconfigure(1, weight=1)
        def link_to_homepage(event):
            from ui.HomePageUI import create_ui as create_homepage_ui
            self.root.destroy()
            create_homepage_ui()
        
        lb_homepage_tittle = tk.Label(nav_frame, text="UniCompare", font=("Arial", 16, "bold"), fg="#1e90ff", bg="white")
        lb_homepage_tittle.grid(row=0, column=0, padx=(20, 50), pady=10)
        lb_homepage_tittle.bind('<Button-1>', link_to_homepage)

        def link_to_ranking():
            self.root.destroy()
            from ui.RankingListAndTableUI import create_ui as create_ranking_ui
            create_ranking_ui()
        
        def chat_to_ai():
            from ui.session import session as session_data
            if session_data['is_logged_in'] == True:
                from ui.ChatbotUI import ChatApp
                self.root.destroy()
                ChatApp()
            else:
                messagebox.showerror("Lỗi", "Vui lòng đăng nhập để dùng chức năng này!")
        menu_items = ["Xếp hạng", "Khám phá", "Sự kiện", "Chuẩn bị", "Học bổng", "Chat với AI"]
        btnRankings = tk.Button(nav_frame, text=menu_items[0], command=link_to_ranking, font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame)
        btnDiscover = tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
        btnEvents = tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
        btnPrepare = tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
        btnScholarships = tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
        btnChatToStudents = tk.Button(nav_frame, command= chat_to_ai, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)

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
            ("Thông tin cá nhân", False),
            ("Lý lịch học tập", True),
            ("Cài đặt tài khoản", False)
        ]

        for item_text, is_selected in menu_items_sidebar:
            bg_color = "#d0d7e5" if is_selected else "#E7EFFE"
            cmd = None
            if item_text == "Cài đặt tài khoản":
                cmd = self.toggle_submenu
            elif item_text == "Thông tin cá nhân":
                cmd = self.go_back_to_personal

            tk.Button(sidebar, text=item_text, bg=bg_color, fg="#333",
                      font=("Segoe UI", 10), anchor="w", relief="flat",
                      padx=10, pady=12, cursor="hand2", command=cmd).pack(fill=tk.X, padx=20, pady=2)

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
        self.main_content = tk.Frame(container, bg="#f5f7fa")
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 40), pady=0)

        tk.Label(self.main_content, text="Lý lịch học tập", bg="#f5f7fa", fg="#1a1a1a",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(0, 25))

        # --- Bằng cấp ---
        tk.Label(self.main_content, text="BẰNG CẤP TRƯỚC ĐÂY", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        qual_frame = tk.Frame(self.main_content, bg="#f5f7fa")
        qual_frame.pack(fill=tk.X, pady=(0, 15))
        qual_frame.columnconfigure(0, weight=1)
        qual_frame.columnconfigure(1, weight=1)
        self.level_entry = self.create_labeled_input(qual_frame, "Trình độ cao nhất", 0)
        self.major_entry = self.create_labeled_input(qual_frame, "Chuyên ngành", 1)

        score_frame = tk.Frame(self.main_content, bg="#f5f7fa")
        score_frame.pack(fill=tk.X, pady=(0, 15))
        score_frame.columnconfigure(0, weight=1)
        score_frame.columnconfigure(1, weight=1)
        score_frame.columnconfigure(2, weight=1)
        self.academic_rate_entry = self.create_labeled_input(score_frame, "Xếp loại", 0)
        self.gpa_entry = self.create_labeled_input(score_frame, "Điểm số", 1)
        self.graduate_year_entry = self.create_labeled_input(score_frame, "Năm tốt nghiệp", 2)

        # --- Điểm thi học thuật ---
        tk.Label(self.main_content, text="ĐIỂM THI HỌC THUẬT", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        test_frame1 = tk.Frame(self.main_content, bg="#f5f7fa")
        test_frame1.pack(anchor="w", pady=(0, 15))
        self.act_entry = self.create_score_box(test_frame1, "ACT", width=8)
        self.gmat_entry = self.create_score_box(test_frame1, "GMAT", width=8)
        self.sat_entry = self.create_score_box(test_frame1, "SAT", width=8)
        self.cat_entry = self.create_score_box(test_frame1, "CAT", width=8)
        self.gre_entry = self.create_score_box(test_frame1, "GRE", width=8)
        self.stat_entry = self.create_score_box(test_frame1, "STAT", width=8)

        test_frame2 = tk.Frame(self.main_content, bg="#f5f7fa")
        test_frame2.pack(anchor="w", pady=(0, 15))
        self.inter_bac_entry = self.create_score_box(test_frame2, "International Baccalaureat", width=25)

        # --- Điểm thi tiếng Anh ---
        tk.Label(self.main_content, text="ĐIỂM THI TIẾNG ANH", bg="#f5f7fa", fg="#666",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 10))

        english_frame = tk.Frame(self.main_content, bg="#f5f7fa")
        english_frame.pack(anchor="w", pady=(0, 15))
        self.ielts_entry = self.create_score_box(english_frame, "IELTS", width=10)
        self.toefl_entry = self.create_score_box(english_frame, "TOEFL", width=10)
        self.pearson_entry = self.create_score_box(english_frame, "Pearson Test", width=15)
        self.cam_entry = self.create_score_box(english_frame, "Cambridge Advanced Test", width=25)

        tk.Button(self.main_content, text="Lưu thay đổi", bg="#1F3AB0", fg="white", font=("Segoe UI", 10, "bold"), bd=0,
                  padx=35, pady=12, cursor="hand2",command=self.save_changes).pack(anchor="e", pady=(20, 0))

        self.create_new_footer(content_frame)

    def create_score_box(self, parent, label_text, width=10):
        container = tk.Frame(parent, bg="#f5f7fa")
        container.pack(side="left", padx=(0, 15))
        tk.Label(container, text=label_text, bg="#f5f7fa", fg="#555", font=("Segoe UI", 9)).pack(anchor="w",
                                                                                                 pady=(0, 1))
        entry = tk.Entry(container, font=("Segoe UI", 10), width=width, bd=0, relief=tk.SOLID, highlightthickness=1,
                         highlightcolor="#1F3AB0", highlightbackground="#ddd")
        entry.pack(fill=tk.X, ipady=6)
        return entry

    def create_labeled_input(self, parent, label_text, column):
        container = tk.Frame(parent, bg="#f5f7fa")
        col_padx = (0, 0) if column == 0 else (15, 0)
        container.grid(row=0, column=column, sticky="ew", padx=col_padx)
        tk.Label(container, text=label_text, bg="#f5f7fa", fg="#666", font=("Segoe UI", 9), anchor="w").pack(anchor="w",
                                                                                                             pady=(0,
                                                                                                                   1))
        entry = tk.Entry(container, font=("Segoe UI", 10), bd=0, relief=tk.SOLID, highlightthickness=1,
                         highlightcolor="#ddd", highlightbackground="#ddd")
        entry.pack(fill=tk.X, ipady=10)
        return entry

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

        # (Rút gọn code footer giống file main để tiết kiệm dòng, nhưng vẫn đầy đủ hiển thị)
        menu_headers = ["About", "Contact", "Privacy", "Users"]
        for col, header in enumerate(menu_headers): tk.Label(footer_frame, text=header, font=("Segoe UI", 10, "bold"),
                                                             bg="white").grid(row=0, column=col + 1, sticky="w")
        social_frame = tk.Frame(footer_frame, bg="white");
        social_frame.grid(row=0, column=4, sticky="e")
        tk.Label(social_frame, text="Follow us", font=("Segoe UI", 10, "bold"), bg="white").pack(side="left",
                                                                                                 padx=(0, 10))
        for txt in ["FB", "IG", "IN", "X"]: tk.Label(social_frame, text=txt, bg="#1F3AB0", fg="white", width=3).pack(
            side="left", padx=2)
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
        subscribe_frame = tk.Frame(footer_frame, bg="white");
        subscribe_frame.grid(row=2, column=4, sticky="ne", pady=(20, 5))
        tk.Label(subscribe_frame, text="Subscribe to our newsletter", font=("Segoe UI", 10, "bold"), bg="white").pack(
            anchor="e")
        input_frame = tk.Frame(subscribe_frame, bg="white", relief="solid", bd=1);
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
            


    # def show_change_password(self):
    #     for widget in self.main_content.winfo_children():
    #         widget.destroy()

    #     tk.Label(self.main_content, text="Đổi mật khẩu", bg="#f5f7fa", font=("Segoe UI", 22, "bold")).pack(anchor="w",
    #                                                                                                        pady=(0, 25))
    #     pass_form = tk.Frame(self.main_content, bg="#f5f7fa")
    #     pass_form.pack(fill='both', expand=True)

    #     for label in ["Mật khẩu hiện tại*", "Mật khẩu mới*", "Xác nhận mật khẩu mới*"]:
    #         container = tk.Frame(pass_form, bg="#f5f7fa")
    #         container.pack(fill=tk.X, pady=(0, 15))
    #         tk.Label(container, text=label, bg="#f5f7fa", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 5))
    #         tk.Entry(container, show="*", font=("Segoe UI", 10), relief="solid", bd=0, highlightthickness=1).pack(
    #             fill="x", ipady=10)

    #     tk.Button(pass_form, text="Cập nhật", bg="#1F3AB0", fg="white", font=("Segoe UI", 10, "bold"), padx=35, pady=12,
    #               command=lambda: messagebox.showinfo("Success", "Đổi mật khẩu thành công")).pack(anchor="w", pady=20)
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


    def go_back_to_personal(self):
        try:
            from ui.PersonalInfoUI import PersonalInfoForm
            PersonalInfoForm(self.root)
        except ImportError:
            messagebox.showerror("Lỗi", "Không tìm thấy file main.py")

    def fill_data(self):
        """Populate entries from self.user (dict) if available"""
        if not self.study_bg:
            return
        u = self.study_bg
        # user dict keys are expected to match DB columns
        try:
            if u.get('level') is not None:
                self.level_entry.delete(0, tk.END)
                self.level_entry.insert(0, u.get('level') or "")


            if u.get('major') is not None:
                self.major_entry.delete(0, tk.END)
                self.major_entry.insert(0, u.get('major') or "")


            if u.get('academic_rate') is not None:
                self.academic_rate_entry.delete(0, tk.END)
                self.academic_rate_entry.insert(0, u.get('academic_rate') or "")


            if u.get('gpa') is not None:
                self.gpa_entry.delete(0, tk.END)
                self.gpa_entry.insert(0, u.get('gpa') or "")


            if u.get('graduate_year') is not None:
                self.graduate_year_entry.delete(0, tk.END)
                self.graduate_year_entry.insert(0, u.get('graduate_year') or "")

            if u.get('act'):
                self.act_entry.delete(0, tk.END)
                self.act_entry.insert(0, u.get('act') or "")


            if u.get('gmat') is not None:
                self.gmat_entry.delete(0, tk.END)
                self.gmat_entry.insert(0, u.get('gmat') or "")


            if u.get('sat') is not None:
                self.sat_entry.delete(0, tk.END)
                self.sat_entry.insert(0, u.get('sat') or "")


            if u.get('cat') is not None:
                self.cat_entry.delete(0, tk.END)
                self.cat_entry.insert(0, u.get('cat') or "")


            if u.get('gre') is not None:
                self.gre_entry.delete(0, tk.END)
                self.gre_entry.insert(0, u.get('gre') or "")


            if u.get('stat') is not None:
                self.stat_entry.delete(0, tk.END)
                self.stat_entry.insert(0, u.get('stat') or "")


            if u.get('ielts') is not None:
                self.ielts_entry.delete(0, tk.END)
                self.ielts_entry.insert(0, u.get('ielts') or "")
            if u.get('toefl') is not None:
                self.toefl_entry.delete(0, tk.END)
                self.toefl_entry.insert(0, u.get('toefl') or "")    
            if u.get('pearson_test') is not None:
                self.pearson_entry.delete(0, tk.END)
                self.pearson_entry.insert(0, u.get('pearson_test') or "")
            if u.get('cam_adv_test') is not None:
                self.cam_entry.delete(0, tk.END)
                self.cam_entry.insert(0, u.get('cam_adv_test') or "")
            if u.get('inter_bac') is not None:
                self.inter_bac_entry.delete(0, tk.END)
                self.inter_bac_entry.insert(0, u.get('inter_bac') or "")
        except Exception as e:
            print("Lỗi khi fill dữ liệu study bg:", e)
    def save_changes(self):
        """Save study background changes to database"""
        try:
            payload = {
                'level': self.level_entry.get().strip() or None,
                'major': self.major_entry.get().strip() or None,
                'academic_rate': self.academic_rate_entry.get().strip() or None,

                'gpa': to_float(self.gpa_entry.get().strip()),
                'graduate_year': to_int(self.graduate_year_entry.get().strip()),

                'act': to_float(self.act_entry.get().strip()),
                'gmat': to_float(self.gmat_entry.get().strip()),
                'sat': to_float(self.sat_entry.get().strip()),
                'cat': to_float(self.cat_entry.get().strip()),
                'gre': to_float(self.gre_entry.get().strip()),
                'stat': to_float(self.stat_entry.get().strip()),

                'ielts': to_float(self.ielts_entry.get().strip()),
                'toefl': to_float(self.toefl_entry.get().strip()),
                'pearson_test': to_float(self.pearson_entry.get().strip()),
                'cam_adv_test': to_float(self.cam_entry.get().strip()),
                'inter_bac': to_float(self.inter_bac_entry.get().strip()),

                'user_id': session_data.session.get("user_id")
            }


            print("\nPayload study_bg:", payload)

            # Gọi controller cập nhật
            success, msg = StudyBGController.update_bg(payload)

            if success:
                messagebox.showinfo("Thành công", msg)

                # load lại study background mới
                self.study_bg = StudyBGController.get_current_user_bg()
                self.fill_data()
            else:
                messagebox.showerror("Lỗi", msg)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu thay đổi!\n{e}")
            print("Lỗi save_changes study bg:", e)
def to_float(value):
    return float(value) if value not in ("", None) else None

def to_int(value):
    return int(value) if value not in ("", None) else None
if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicInfoForm(root)
    root.mainloop()