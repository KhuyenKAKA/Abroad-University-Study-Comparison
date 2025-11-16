import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from controller import UserController

def create_ui():
    """Tạo giao diện đăng ký người dùng"""
    # Khởi tạo cơ sở dữ liệu và controller
    # controller = UserController()
    
    # Khởi tạo cửa sổ chính
    root = tk.Tk()
    root.title("Biểu mẫu Đăng ký QS")
    # Thiết lập kích thước cửa sổ để trông giống giao diện web hơn
    root.geometry("900x800")
    # Tắt khả năng thay đổi kích thước cửa sổ
    root.resizable(False, False)

    # --- Phần 1: Khung chứa chính (chia thành 2 cột) ---
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill='both', expand=True)
    
    # Thiết lập trọng số cột cho main_frame để chia không gian
    main_frame.grid_columnconfigure(0, weight=1) # Cột 0 (Trái) mở rộng
    main_frame.grid_columnconfigure(1, weight=1) # Cột 1 (Phải) mở rộng

    # --- Phần 2: Cột bên trái (Thông tin khuyến khích) ---
    # Trong bản gốc là nền màu xanh nhạt với chữ trắng, 
    # ở đây tôi dùng nền màu xám nhạt để dễ phân biệt
    left_frame = ttk.Frame(main_frame, padding="30", style='Left.TFrame')
    left_frame.grid(row=0, column=0, sticky="nsew")

    # Định nghĩa style cho khung bên trái (optional)
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
        
    #     # Thêm một khoảng trống để mô phỏng vị trí hình ảnh
    ttk.Label(left_frame, background='#7EA6F2').pack(pady=40, fill='x')


    # --- Phần 3: Cột bên phải (Form Đăng ký) ---
    right_frame = ttk.Frame(main_frame, padding="30")
    right_frame.grid(row=0, column=1, sticky="nsew")
    
    # Sử dụng grid bên trong right_frame để dễ dàng căn chỉnh form

    # Hàng 0: Tiêu đề "Đăng ký"
    signup_title = ttk.Label(right_frame, text="Đăng ký", font=("Arial", 14, "bold"))
    signup_title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky='w')

    # --- Các trường nhập liệu (Hàng 1 đến Hàng 5) ---
    labels = ["Họ*", "Tên*", "Email*", "Mật khẩu*", "Xác nhận mật khẩu*"]
    entries = []
    for i, label_text in enumerate(labels):
        label = ttk.Label(right_frame, text=label_text, font=("Arial", 9))
        label.grid(row=1 + i*2, column=0, columnspan=2, pady=(10, 2), sticky='w')
        
        # Nếu là trường mật khẩu, hiển thị dấu sao
        if i >= 3:  # Cột 3 (Mật khẩu) và 4 (Xác nhận mật khẩu)
            entry = ttk.Entry(right_frame, width=40, show="*")
        else:
            entry = ttk.Entry(right_frame, width=40)
        
        entry.grid(row=2 + i*2, column=0, columnspan=2, pady=(0, 10), sticky='ew', ipady=3)
        entries.append(entry)
        
    # Hàng 11 & 12: Checkboxes
    cb_var1 = tk.BooleanVar()
    cb1 = tk.Checkbutton(right_frame, text="Tôi rất vui khi nhận được các thông tin liên lạc và tài nguyên hữu ích từ QS liên quan đến sở thích học tập và hứa hẹn sự kiện của tôi.", variable=cb_var1, wraplength=350, justify='left')
    cb1.grid(row=11, column=0, columnspan=2, pady=5, sticky='w')
    
    cb_var2 = tk.BooleanVar()
    cb2 = tk.Checkbutton(right_frame, text="Tôi rất vui khi nhận được tin nhắn từ các bên thứ ba bao gồm các tổ chức phù hợp với sở thích học tập của tôi.", variable=cb_var2, wraplength=350, justify='left')
    cb2.grid(row=12, column=0, columnspan=2, pady=5, sticky='w')

    # Hàng 13: Nút "Đăng ký"
    def on_signup_click():
        # Lấy dữ liệu từ các trường nhập liệu
        first_name = entries[0].get()
        last_name = entries[1].get()
        email = entries[2].get()
        password = entries[3].get()
        confirm_password = entries[4].get()
        agree_communication = cb_var1.get()
        agree_third_party = cb_var2.get()
        
        # Kiểm tra checkbox
        if not agree_communication or not agree_third_party:
            messagebox.showerror("Lỗi", "Vui lòng đánh dấu cả hai hộp kiểm để tiếp tục")
            return
        
        # Gọi controller để đăng ký
        # success, message = controller.register_user(
        #     first_name, last_name, email, password, confirm_password,
        #     agree_communication, agree_third_party
        # )
        
        # if success:
        #     messagebox.showinfo("Thành công", message)
        #     # Xóa các trường nhập liệu
        #     for entry in entries:
        #         entry.delete(0, tk.END)
        #     cb_var1.set(False)
        #     cb_var2.set(False)
        # else:
        #     messagebox.showerror("Lỗi", message)
    
    signup_button = tk.Button(right_frame, text="Đăng ký", bg="#1F3AB0", fg="white", font=("Arial", 10, "bold"), bd=0, padx=10, pady=8, command=on_signup_click)
    signup_button.grid(row=13, column=0, columnspan=2, pady=(20, 10), sticky='ew')

    signin_frame = ttk.Frame(right_frame)
    signin_frame.grid(row=14, column=0, columnspan=2, pady=(10, 0), sticky='w')
    
    dont_have_label = ttk.Label(signin_frame, text="Bạn đã có tài khoản?", font=("Arial", 9))
    dont_have_label.pack(side=tk.LEFT)
    def go_to_signin():
        from ui.SignInUI import create_ui as create_signin_ui
        root.destroy()  # Đóng cửa sổ đăng nhập
        create_signin_ui()  # Mở cửa sổ đăng ký
    
    signin_button = tk.Button(signin_frame, text="Đăng nhập", fg="#1F3AB0", bg="white", 
                             bd=0, font=("Arial", 9), cursor="hand2",
                             command=go_to_signin)
    signin_button.pack(side=tk.LEFT, padx=(5, 0))
    root.mainloop()

if __name__ == "__main__":
    create_ui()
