import tkinter as tk

# ================== DỮ LIỆU BẢNG (5 TRƯỜNG) =====================
table_data = [
    {
        "name": "MIT",
        "fee": 100, "scholarship": 100, "domestic": 100, "international": 100,
        "total_stu": 11500, "ug_rate": 60, "pg_rate": 40,
        "inter_total": 30, "inter_ug_rate": 20, "inter_pg_rate": 10
    },
    {
        "name": "Imperial College London",
        "fee": 95, "scholarship": 99.6, "domestic": 99.3, "international": 100,
        "total_stu": 19000, "ug_rate": 55, "pg_rate": 45,
        "inter_total": 35, "inter_ug_rate": 25, "inter_pg_rate": 10
    },
    {
        "name": "Stanford University",
        "fee": 98, "scholarship": 98.5, "domestic": 99.5, "international": 95,
        "total_stu": 17000, "ug_rate": 50, "pg_rate": 50,
        "inter_total": 25, "inter_ug_rate": 15, "inter_pg_rate": 10
    },
    {
        "name": "ETH Zurich",
        "fee": 90, "scholarship": 95, "domestic": 100, "international": 90,
        "total_stu": 24000, "ug_rate": 65, "pg_rate": 35,
        "inter_total": 40, "inter_ug_rate": 30, "inter_pg_rate": 10
    },
    {
        "name": "National University of SGP",
        "fee": 92, "scholarship": 97, "domestic": 95, "international": 98,
        "total_stu": 35000, "ug_rate": 70, "pg_rate": 30,
        "inter_total": 20, "inter_ug_rate": 10, "inter_pg_rate": 10
    }
]

# --- Cấu hình Độ rộng Cột ---
COLUMN_WIDTHS = [20, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9] 

# Định nghĩa các list độ rộng cho từng nhóm cột
COL_1_WIDTHS = [COLUMN_WIDTHS[0]] # Trường
COL_2_WIDTHS = [COLUMN_WIDTHS[1], COLUMN_WIDTHS[2]] # Học phí & Học bổng
COL_3_WIDTHS = [COLUMN_WIDTHS[3], COLUMN_WIDTHS[4]] # Tỷ lệ Sinh viên
COL_4_WIDTHS = [COLUMN_WIDTHS[5], COLUMN_WIDTHS[6], COLUMN_WIDTHS[7]] # Cấu trúc SV
COL_5_WIDTHS = [COLUMN_WIDTHS[8], COLUMN_WIDTHS[9], COLUMN_WIDTHS[10]] # SV Quốc tế


def create_header_label(parent_frame, title_text, sub_labels, sub_label_widths, bg_color, header_height=2, column_padx=1):
    """
    Tạo một cột tiêu đề (Frame) với tiêu đề chính và các tiêu đề phụ.
    """
    column_frame = tk.Frame(parent_frame, bg=bg_color, bd=1, relief="solid")
    column_frame.pack(side="left", fill='y', padx=(0, column_padx)) 

    # --- Xử lý Tiêu đề Phức hợp (2 tầng) ---
    if sub_labels and title_text:
        total_sub_width = sum(sub_label_widths) 
        
        # Khung chứa Tiêu đề chính
        upper_frame = tk.Frame(column_frame, bg=bg_color)
        upper_frame.pack(fill='x', padx=0, pady=2) 

        # Tiêu đề chính: Đặt width bằng tổng độ rộng các Label con và dùng pack căn giữa
        tk.Label(
            upper_frame, 
            text=title_text, 
            font=("Arial", 10, "bold"), 
            fg="#1e90ff", 
            bg=bg_color,
            width=total_sub_width,
            justify="center" # <--- Căn giữa text
        ).pack(pady=(0, 2))

        # Khung chứa Tiêu đề phụ (Cột dữ liệu)
        lower_frame = tk.Frame(column_frame, bg=bg_color)
        # Sử dụng anchor='center' khi pack để khung con căn giữa trong khung cha
        # Tuy nhiên, ta vẫn dùng side="left" cho các label con để chúng nằm ngang.
        lower_frame.pack(fill='x', padx=0, pady=2) 
        
        # Các tiêu đề phụ
        for i, label_text in enumerate(sub_labels):
            width = sub_label_widths[i]
            tk.Label(
                lower_frame, 
                text=label_text, 
                font=("Arial", 8), 
                bg=bg_color, 
                width=width,
                justify="center",
                anchor="center" # <--- Căn giữa text
            ).pack(side="left", padx=0) 
            
    # --- Xử lý Tiêu đề Đơn (1 tầng) ---
    elif title_text and not sub_labels:
        # Cột chỉ có 1 tiêu đề: Căn giữa
        tk.Label(
            column_frame, 
            text=title_text, 
            font=("Arial", 10, "bold"), 
            bg=bg_color, 
            width=COLUMN_WIDTHS[0], 
            height=header_height, 
            bd=1, relief="solid",
            justify="center" # <--- Căn giữa text
        ).pack(side="left", padx=0, pady=5) 


def add_table_row(parent_frame, data, row_index):
    """
    Tạo một hàng dữ liệu. Căn chỉnh tất cả các cột dữ liệu vào giữa.
    """
    bg_color = "#ffffff" if row_index % 2 == 0 else "#f0f0f0"
    
    row_frame = tk.Frame(parent_frame, bg=bg_color, bd=1, relief="solid")
    row_frame.pack(fill="x", pady=(0, 1))

    # Định nghĩa các trường dữ liệu theo thứ tự cột
    fields = [
        data["name"], data["fee"], data["scholarship"], 
        data["domestic"], data["international"], 
        data["total_stu"], data["ug_rate"], data["pg_rate"], 
        data["inter_total"], data["inter_ug_rate"], data["inter_pg_rate"]
    ]
    
    for i, value in enumerate(fields):
        width = COLUMN_WIDTHS[i]
        
        # Căn chỉnh nội dung: Cột tên trường VẪN căn lề trái để dễ đọc, các cột số liệu căn giữa
        anchor_style = 'center' # <--- Đã thay đổi thành 'center' cho TẤT CẢ
        
        # Định dạng giá trị
        if i == 0: 
             text_value = str(value)
             anchor_style = 'w' # Giữ nguyên cột tên trường căn trái
        elif i == 5: 
             text_value = f'{value:,}' 
        else: 
             text_value = f'{value:.1f}' if isinstance(value, float) else str(value)
        
        # Màu nền xen kẽ cho cột dữ liệu
        label_bg_color = bg_color
        if i > 0 and i % 2 == 0:
            label_bg_color = "#E6F2FF" if bg_color == "#ffffff" else "#DDDDDD"

        tk.Label(
            row_frame, 
            text=text_value, 
            font=("Arial", 10), 
            bg=label_bg_color, 
            width=width, 
            anchor=anchor_style, # <--- Áp dụng anchor
            relief="flat", bd=0
        ).pack(side="left", padx=0, pady=8)


def render_table_view_matplotlib_data(frame_to_render):
    """Hàm chính để render bảng dữ liệu bằng Tkinter Frames"""
    
    # 1. Xóa nội dung cũ
    for widget in frame_to_render.winfo_children():
        widget.destroy()

    # 2. Khung Tiêu đề
    header = tk.Frame(frame_to_render, bg="white", bd=1, relief="solid")
    header.pack(fill="x", pady=(0, 1))

    # --- Cột 1: Trường (Tiêu đề đơn) ---
    create_header_label(
        header, 
        "Trường", 
        [], 
        COL_1_WIDTHS, 
        "#CCCCCC",
        header_height=4,
    )
    
    # --- Cột 2: Học phí & Học bổng (2 sub-labels) ---
    create_header_label(
        header, 
        "Học phí & Học bổng", 
        ['Fee', 'Scholarship'], 
        COL_2_WIDTHS, 
        "#BBDDFF",
    )
    
    # --- Cột 3: Tỷ lệ Sinh viên (2 sub-labels) ---
    create_header_label(
        header, 
        "Tỷ lệ Sinh viên", 
        ['Domestic', 'International'], 
        COL_3_WIDTHS, 
        "#BBDDFF",
    )

    # --- Cột 4: Cấu trúc SV (3 sub-labels) ---
    create_header_label(
        header, 
        "Cấu trúc SV", 
        ['Total Stu', 'UG Rate', 'PG Rate'], 
        COL_4_WIDTHS, 
        "#BBDDFF",
    )
    
    # --- Cột 5: SV Quốc tế (3 sub-labels) ---
    create_header_label(
        header, 
        "SV Quốc tế", 
        ['Inter Total', 'Inter UG', 'Inter PG'],
        COL_5_WIDTHS, 
        "#BBDDFF",
    )
    
    # 3. Thêm các hàng dữ liệu
    for index, data in enumerate(table_data):
        add_table_row(frame_to_render, data, index)


# =================================================================
# --- Khởi tạo Demo Tkinter ---
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tkinter Table View - Content Center Aligned")
    root.geometry("1000x500") 

    unversities_card_frame = tk.Frame(root, bg="#DDDDDD")
    unversities_card_frame.pack(fill='x', padx=10, pady=10) 
    
    render_table_view_matplotlib_data(unversities_card_frame)
    
    root.mainloop()