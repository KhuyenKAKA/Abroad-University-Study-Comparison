import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from controller import UserController

def create_ui():
    """Tạo giao diện đăng nhập người dùng"""
    # Khởi tạo cơ sở dữ liệu và controller
    # controller = UserController()
    
    # Khởi tạo cửa sổ chính
    root = tk.Tk()
    root.title("Đăng nhập - UC")
    # Thiết lập kích thước cửa sổ để trông giống giao diện web hơn
    root.geometry("800x600")
    # Tắt khả năng thay đổi kích thước cửa sổ
    root.resizable(False, False)

    # --- Phần 1: Khung chứa chính (chia thành 2 cột) ---
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill='both', expand=True)
    
    # Thiết lập trọng số cột cho main_frame để chia không gian
    main_frame.grid_columnconfigure(0, weight=1) # Cột 0 (Trái) mở rộng
    main_frame.grid_columnconfigure(1, weight=1) # Cột 1 (Phải) mở rộng

    # --- Phần 2: Cột bên trái (Thông tin khuyến khích) ---
    left_frame = ttk.Frame(main_frame, padding="30", style='Left.TFrame')
    left_frame.grid(row=0, column=0, sticky="nsew")

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
    right_frame = ttk.Frame(main_frame, padding="30")
    right_frame.grid(row=0, column=1, sticky="nsew")
    
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
    #     email = entries[0].get()
    #     password = entries[1].get()
        
    #     # Gọi controller để kiểm tra đăng nhập
    #     success, message = controller.login_user(email, password)
        
    #     if success:
    #         messagebox.showinfo("Thành công", message)
    #         entries[0].delete(0, tk.END)
    #         entries[1].delete(0, tk.END)
    #     else:
    #         messagebox.showerror("Lỗi", message)
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
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
