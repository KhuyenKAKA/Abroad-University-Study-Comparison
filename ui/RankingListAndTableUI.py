import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests 
from io import BytesIO
from controller.UniversityController import UniversityController
from tkinter import messagebox as mess
def create_ui():
    global current_view_mode
    current_view_mode = 1
    global universities_data
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
    
    menu_items = ["Xếp hạng", "Khám phá", "Sự kiện", "Chuẩn bị", "Học bổng", "Chat với AI"]
    # Để làm nổi bật "Rankings" như trong ảnh
    tk.Button(nav_frame, text=menu_items[0], font=("Arial", 10, "bold"), bg="white", fg="#1e90ff", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame) 
    tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Tư vấn miễn phí",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    try:
        # Giả sử bạn đã có file search.png trong thư mục assets
        # img = Image.open("Abroad-University-Study-Comparison/assets/search.png")
        img = Image.open("assets/search.png")
        img = img.resize((24, 24), Image.LANCZOS)
        search_photo = ImageTk.PhotoImage(img)
        tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
    except FileNotFoundError:
        tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    
    tk.Button(right_nav_frame, text="Đăng nhập", foreground='white', background="#1F3AB0").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Đăng ký", foreground='white', background="#1F3AB0").pack(side='left', padx=5)

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
    
    # ===============================================
    # Phần Nội Dung Chính Bắt Đầu Tại Đây
    # ===============================================
    
    frame_for_infro_frame = tk.Frame(content_frame, bg="#eaf4ff")
    frame_for_infro_frame.pack(fill='x')

    info_frame = tk.Frame(frame_for_infro_frame, bg="#eaf4ff",pady=40,padx=50)
    info_frame.pack(fill="x", expand=True)
    # info_frame.pack(fill="x")
    
    tk.Label(info_frame, text="Bảng xếp hạng Đại học Thế giới UC năm 2025: Các trường đại học hàng đầu toàn cầu", 
             font=("Arial", 20, "bold"), fg="#333", bg="#eaf4ff", justify='left', wraplength=550).pack(anchor="w", pady=(0, 10))
    
    description_text = "Khám phá các trường đại học hàng đầu trên toàn thế giới với Bảng xếp hạng Đại học Thế giới UC 2026. Hơn 1.500 trường đại học hàng đầu thế giới được đưa vào phiên bản 2026 của Bảng xếp hạng Đại học Thế giới UC, với hơn 100 địa điểm được đại diện trên toàn thế giới"
    tk.Label(info_frame, text=description_text, font=("Arial", 10), fg="#555", bg="#eaf4ff", justify='left', wraplength=550).pack(anchor="w", pady=(0, 15))
    
    # Khung Đăng ký
    register_frame = tk.Frame(info_frame, bg="#4879ae")
    register_frame.pack(anchor="w")
    tk.Label(register_frame, text="Đăng ký thành viên trang web miễn phí để truy cập so sánh trực tiếp các trường đại học và nhiều tính năng khác.", 
             font=("Arial", 9), fg="#f8f9fa", bg="#4879ae").pack(side="left", pady=10)
    tk.Button(register_frame, text="Đăng ký ngay!", fg="#1F3AB0", background="#eaf4ff", font=("Arial", 9, "bold"), relief='flat').pack(side="left", padx=10, pady=10)
    
    # 
    main_content_frame = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=10)
    main_content_frame.pack(fill='x')
    
    # # Khung Tiêu Đề và Ảnh Minh Họa
    header_frame = tk.Frame(main_content_frame, bg="#f8f9fa")
    header_frame.pack(fill='x', pady=(0, 10))

    # # Ảnh minh họa (Mô phỏng)
    illustration_frame = tk.Frame(header_frame, bg="#f8f9fa")
    illustration_frame.pack(side="right")
    tk.Label(illustration_frame, text="", fg="gray", bg="#f8f9fa", font=("Arial", 8)).pack(padx=20)
    
    # Thanh công cụ và Tìm kiếm
    toolbar_frame = tk.Frame(main_content_frame, bg="#f8f9fa")
    toolbar_frame.pack(fill='x', pady=(10, 20))

    def render_table_view():
        table_view.config(bg='white')
        quick_view.config(bg='#f0f0f0')
        global current_view_mode 
        current_view_mode = 2
        for widget in unversities_card_frame.winfo_children():
            widget.destroy()

        # Header Row
        header = tk.Frame(unversities_card_frame, bg="#f0f0f0", bd=1, relief="solid")
        header.pack(fill="x")

        # headers = ["Rank", "Logo", "University", "Location", "Overall Score"]
        # widths = [6, 10, 35, 25, 12]
        Re_Dis_frame = tk.Frame(header, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        tk.Label(Re_Dis_frame,text="Xếp hạng\nchung",font=("Arial", 10, "bold"),bg="white", width=10).pack(side="left", padx=5, pady=5)
        tk.Label(header,text="Trường đại học",font=("Arial", 10, "bold"),bg="#f0f0f0", width=33).pack(side="left", padx=5, pady=5)
        
        Re_Dis_frame = tk.Frame(header, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        lower_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        lower_frame.pack(fill='y',padx=5,pady=5)
        tk.Label(upper_frame, text='Nghiên cứu & Khám phá', font=("Arial", 10,), fg="#1e90ff", bg="white").pack()
        tk.Label(lower_frame, text='Số trích dẫn\ntrên mỗi giảng viên', font=("Arial", 8,), bg="white",width=14).pack(side="left")
        tk.Label(lower_frame, text='Danh tiếng\nhọc thuật', font=("Arial", 8), bg="white",width=10).pack(side="left")

        Re_Dis_frame = tk.Frame(header, bg="#f0f0f0")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        lower_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        lower_frame.pack(fill='y',padx=5,pady=5)
        tk.Label(upper_frame, text='Trải nghiệm học tập', font=("Arial", 10,), fg="#1e90ff", bg="#f0f0f0").pack()
        tk.Label(lower_frame, text='Tỷ lệ\ngiảng viên/sinh viên', font=("Arial", 8,), bg="#f0f0f0",width=15).pack(side="left")
        
        Re_Dis_frame = tk.Frame(header, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        lower_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        lower_frame.pack(fill='y',padx=5,pady=5)
        tk.Label(upper_frame, text='Khả năng việc làm', font=("Arial", 10,), fg="#1e90ff", bg="white").pack()
        tk.Label(lower_frame, text='Danh tiếng với\nnhà tuyển dụng', font=("Arial", 8,), bg="white",width=12).pack(side="left")
        tk.Label(lower_frame, text='Kết quả của sinh\nviên tốt nghiệp', font=("Arial", 8,), bg="white",width=14).pack(side="left")
        
        Re_Dis_frame = tk.Frame(header, bg="#f0f0f0")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        lower_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        lower_frame.pack(fill='y',padx=5,pady=5)
        tk.Label(upper_frame, text='Sự tham gia toàn cầu', font=("Arial", 10,), fg="#1e90ff", bg="#f0f0f0").pack()
        tk.Label(lower_frame, text='Tỷ lệ\nsinh viên quốc tế', font=("Arial", 8,), bg="#f0f0f0",width=15).pack(side="left")
        tk.Label(lower_frame, text='Mạng lưới\nnghiên cứu quốc tế', font=("Arial", 8,), bg="#f0f0f0",width=15).pack(side="left")
        tk.Label(lower_frame, text='Tỷ lệ giảng viên\nquốc tế', font=("Arial", 8,), bg="#f0f0f0",width=15).pack(side="left")
        tk.Label(lower_frame, text='Mức độ đa dạng\nsinh viên quốc tế', font=("Arial", 8,), bg="#f0f0f0",width=15).pack(side="left")
        
        Re_Dis_frame = tk.Frame(header, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        lower_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        lower_frame.pack(fill='y',padx=5,pady=5)
        tk.Label(upper_frame, text='Bền vững', font=("Arial", 10,), fg="#1e90ff", bg="white").pack()
        tk.Label(lower_frame, text='Chỉ số\nbền vững', font=("Arial", 8,), bg="white",width=10).pack(side="left")
        
        per_page = results_per_page.get()
        page = current_page.get()

        start = (page - 1) * per_page
        end = start + per_page
        for data in universities_data[start:end]:
            create_university_table_row(unversities_card_frame, data)
        
        render_pagination_bar()

    def render_university_list():
        # Xóa cũ
        quick_view.config(bg='white')
        table_view.config(bg='#f0f0f0')
        global current_view_mode
        current_view_mode = 1
        for widget in unversities_card_frame.winfo_children():
            widget.destroy()

        per_page = results_per_page.get()
        page = current_page.get()

        start = (page - 1) * per_page
        end = start + per_page

        for data in universities_data[start:end]:
            create_university_block(unversities_card_frame, data)

        render_pagination_bar()
    
    def take_compare_universities():
        global compare_list
        checked_list = [v for v in compare_list if compare_list[v].get()]
        if len(checked_list)>1: 
            pass
        else:
            mess.showwarning("Thông báo","Hãy chọn trường đại học để so sánh!")

    # Nút Quick View và Table View
    view_frame = tk.Frame(toolbar_frame, bg="#f8f9fa", bd=1, relief='solid')
    view_frame.pack(side="left", padx=(0, 20))
    # current_view_mode = 1
    quick_view = tk.Button(view_frame, text="📊 Xem nhanh",command=render_university_list, font=("Arial", 9), bg="white", relief='flat')
    quick_view.pack(side="left", padx=(0, 1), pady=0)
    table_view = tk.Button(view_frame, text="▦ Xem dạng bảng",command=render_table_view ,font=("Arial", 9), bg="#e0e0e0", relief='flat')
    table_view.pack(side="left", padx=(1, 0), pady=0)
    
    # Trường tìm kiếm
    search_entry_frame = tk.Frame(toolbar_frame, bg="white", bd=1, relief='solid')
    search_entry_frame.pack(side="left", fill='y', padx=(0, 20))
    tk.Label(search_entry_frame, image=search_photo, font=("Arial", 10), bg="white").pack(side="left", padx=5)
    entry_search = tk.Entry(search_entry_frame, width=30, font=("Arial", 10), relief='flat')
    entry_search.pack(side="left", padx=5)
    
    # Nút Apply Filters & Compare
    tk.Button(toolbar_frame, text="So sánh",command=take_compare_universities, fg="white", background="#0013e9", font=("Arial", 9, "bold"), relief='flat').pack(side="right",padx=(20,0))
    tk.Button(toolbar_frame, text="Áp dụng bộ lọc", fg="white", background="#1e90ff", font=("Arial", 9, "bold"), relief='flat').pack(side="right")
    number_of_Results = tk.Label(toolbar_frame, text="2 Results", font=("Arial", 10), fg="#555", bg="#f8f9fa") # Khoảng cách mô phỏng
    number_of_Results.pack(side="right", padx=(100, 20))

    # Dropdown "University rank (High to Low)"
    rank_dropdown_frame = tk.Frame(toolbar_frame, bg="#f8f9fa")
    rank_dropdown_frame.pack(side="right")
    tk.Label(rank_dropdown_frame, text="Thông tin từ ngày: 19/06/2025", font=("Arial", 8), fg="#555", bg="#f8f9fa").pack(side="left", padx=10)
    
    # tk.Label(rank_dropdown_frame, text="University rank (High to Low) ▼", font=("Arial", 9), fg="#333", bg="white", bd=1, relief='solid', padx=5, pady=2).pack(side="left")
    selected_modes_filter = ["Xếp hạng đại học(Cao xuống thấp)", "Xếp hạng đại học(Thấp lên cao)"]
    selected_mode = tk.StringVar()
    selected_mode.set("Xếp hạng đại học(Cao xuống thấp)")
    selected_modes_filter_dropdown = tk.OptionMenu(rank_dropdown_frame,selected_mode,*selected_modes_filter)
    selected_modes_filter_dropdown.pack(side='left',padx=5,pady=2)

    def on_sort_change(*args):
        mode = selected_mode.get()

        if mode == "Xếp hạng đại học(Cao xuống thấp)":
            universities_data.sort(key=lambda x: x['overall_score'], reverse=True)
        else:
            universities_data.sort(key=lambda x: x['overall_score'])

        # # Cập nhật rank theo thứ tự mới
        # for idx, uni in enumerate(universities_data, start=1):
        #     uni['rank'] = idx
        global current_view_mode
        if current_view_mode == 2:
            render_table_view()
        else:
            render_university_list()
            

    selected_mode.trace("w", on_sort_change)
    # 
    global compare_list
    global short_list
    compare_list = {}
    short_list = {}
    # # Khối thông tin Trường Đại học
    def check_number_of_compare(current_compare):
        global compare_list
        checked = sum(v.get() for v in compare_list.values())
        if checked > 5:
            current_compare.set(0)
            mess.showwarning("Đạt số lượng so sánh tối đa là 5!","Không thêm được các trường nữa")
            
    def link_to_detail(event,id):
        pass
    
    def create_university_block(parent,data):
        uni_block = tk.Frame(parent, bg="white", bd=1, relief='solid', padx=20, pady=15)
        uni_block.pack(fill='x', pady=15)

        # Cột 1: Rank và Score
        rank_score_frame = tk.Frame(uni_block, bg="white")
        rank_score_frame.pack(side="left", padx=(0, 30))
        
        tk.Label(rank_score_frame, text="Rank", font=("Arial", 8), fg="#888", bg="white").pack(anchor="w")
        tk.Label(rank_score_frame, text=data['rank'], font=("Arial", 28, "bold"), fg="#333", bg="white").pack(anchor="w")
        
        tk.Label(rank_score_frame, text="Điểm số:", font=("Arial", 9), fg="#888", bg="white").pack(anchor="w", pady=(10, 0))
        if data['overall_score'] != 0.0:
            tk.Label(rank_score_frame, text=data['overall_score'], font=("Arial", 14, "bold"), fg="#333", bg="white").pack(anchor="w")
        else:
            tk.Label(rank_score_frame, text="Không có dữ liệu", font=("Arial", 14, "bold"), fg="#333", bg="white").pack(anchor="w")

        # Cột 2: Logo và Tên Trường
        details_frame = tk.Frame(uni_block, bg="white")
        details_frame.pack(side="left", fill='x', expand=True)

        header_details_frame = tk.Frame(details_frame, bg="white")
        header_details_frame.pack(fill='x', pady=(0, 10))

        # Logo (Mô phỏng)
        try:
            # Sửa lỗi: Chuyển sang đường dẫn tương đối đơn giản hơn
            response = requests.get(data['logo'])
            image_data = BytesIO(response.content)
            pil_image = Image.open(image_data)
            pil_image = pil_image.resize((70, 70), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            logo_label = tk.Label(header_details_frame, image=tk_image, bg="white")
            logo_label.pack(side="left", padx=(0, 10))
            images_reference.append(tk_image) # Lưu reference
        except FileNotFoundError:
            tk.Label(header_details_frame, text="[Logo]", font=("Arial", 8), bg="white", fg="gray", width=5).pack(side="left", padx=(0, 10))
        
        name_loc_frame = tk.Frame(header_details_frame, bg="white")
        name_loc_frame.pack(side="left", fill='y')
        
        university_name = tk.Label(name_loc_frame, text=data['name'], font=("Arial", 14, "bold"), fg="#1e90ff", bg="white")
        university_name.pack(anchor="w")
        university_name.bind("<Button-1>",lambda event: link_to_detail(event,data['id']))
        tk.Label(name_loc_frame, text=f'{data['city']}, {data['country']}', font=("Arial", 10), fg="#555", bg="white").pack(anchor="w")

        # Nút Shortlist và Compare
        action_frame = tk.Frame(header_details_frame, bg="white")
        action_frame.pack(side="right")
        # tk.Button(action_frame, text="Shortlist", font=("Arial", 9), bg="white", relief='flat').pack(side="left", padx=5)

        
        tk.Checkbutton(action_frame,variable=short_list[data['id']], text='Ưa thích',font=("Arial", 9), bg="white", relief='flat').pack(side="left", padx=5)
        tk.Checkbutton(action_frame,variable=compare_list[data['id']], command=lambda v=compare_list[data['id']]: check_number_of_compare(v), text='So sánh',font=("Arial", 9), bg="white", relief='flat').pack(side="left", padx=5)
        # tk.Button(action_frame, text="Compare", font=("Arial", 9), bg="white", relief='flat').pack(side="left", padx=5)

        # Thanh tiêu chí - Tab Menu (Mới)
        criteria_frame = tk.Frame(details_frame, bg="white")
        criteria_frame.pack(fill='x', pady=(5, 15))

        criteria_list = ["Nghiên cứu & khám phá", "Trải nghiệm học tập", "Khả năng việc làm", "Sự tham gia toàn cầu", "Bền vững"]

        criteria_tabs = {}  # lưu cả button và underline

        # Khung chứa thanh điểm
        score_bar_container = tk.Frame(details_frame, bg="white")
        score_bar_container.pack(fill='x', pady=(5, 0))

        # Hàm click tab
        def on_tab_click(selected):
            # Reset tất cả tab
            for key, (btn, underline) in criteria_tabs.items():
                btn.config(bg="white", fg="#333")
                underline.config(bg="white")

            # Active tab được chọn
            btn, underline = criteria_tabs[selected]
            btn.config(bg="white", fg="#1e90ff")
            underline.config(bg="#1e90ff")

            # Reset score bar
            for widget in score_bar_container.winfo_children():
                widget.destroy()

            # Hàm vẽ score bar
            def create_score_item(parent, label, score, max_width=150):
                item_frame = tk.Frame(parent, bg="white")
                item_frame.pack(side="left", padx=20)

                tk.Label(item_frame, text=label, font=("Arial", 8, "bold"), bg="white").pack(anchor="w")

                bar = tk.Canvas(item_frame, width=max_width, height=6, bg="#e0e0e0", highlightthickness=0)
                bar.pack(side="left")

                w = int(score / 100 * max_width)
                bar.create_rectangle(0, 0, w, 6, fill="#1e90ff", outline="")

                tk.Label(item_frame, text=str(score), font=("Arial", 8), bg="white").pack(side="left", padx=5)

            # Hiện nội dung theo tab
            if selected == "Nghiên cứu & khám phá":
                for score_type,score_current in data['score']['Research & Discovery'].items():
                    create_score_item(score_bar_container, score_type, score_current)
            elif selected == "Trải nghiệm học tập":
                for score_type,score_current in data['score']['Learning Experience'].items():
                    create_score_item(score_bar_container, score_type, score_current)
            elif selected == "Khả năng việc làm":
                for score_type,score_current in data['score']['Employability'].items():
                    create_score_item(score_bar_container, score_type, score_current)
            elif selected == "Sự tham gia toàn cầu":
                for score_type,score_current in data['score']['Global Engagement'].items():
                    create_score_item(score_bar_container, score_type, score_current)
            else:
                for score_type,score_current in data['score']['Sustainability'].items():
                    create_score_item(score_bar_container, score_type, score_current)

        # Tạo button + underline tách biệt
        for name in criteria_list:
            tab = tk.Frame(criteria_frame, bg="white")
            tab.pack(side="left", padx=8)

            btn = tk.Button(tab, text=name, font=("Arial", 9),
                            bg="white", fg="#333", relief="flat",
                            command=lambda c=name: on_tab_click(c))
            btn.pack()

            underline = tk.Frame(tab, height=2, bg="white")
            underline.pack(fill='x')

            criteria_tabs[name] = (btn, underline)

        # Auto-select tab đầu tiên
        on_tab_click(criteria_list[0])

    def create_university_table_row(parent, data):
        row = tk.Frame(parent, bg="white", bd=1, relief="solid", pady=5)
        row.pack(fill="x")

        # Rank
        tk.Label(row, text=data["rank"], font=("Arial", 11, "bold"), bg="white", width=10).pack(side="left")

        Re_Dis_frame = tk.Frame(row, bg="#f0f0f0")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        lower_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        lower_frame.pack(fill='y',padx=5,pady=5)
        tk.Label(upper_frame, text=data["name"], font=("Arial", 10,), fg="#1e90ff", bg="#f0f0f0",width=33).pack(side="left")
        tk.Label(lower_frame, text=f"{data['city']}, {data['country']}", font=("Arial", 8,), bg="#f0f0f0",width=33).pack(side="left")

        Re_Dis_frame = tk.Frame(row, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        for score_type,score_current in data['score']['Research & Discovery'].items():
            tk.Label(upper_frame, text=f'{score_current}', font=("Arial", 8),
                    bg="white", fg="#1e90ff", width=12)\
                .pack(side="left")
            
        Re_Dis_frame = tk.Frame(row, bg="#f0f0f0")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=(3,2),pady=5)
        for score_type,score_current in data['score']['Learning Experience'].items():
            tk.Label(upper_frame, text=f'{score_current}', font=("Arial", 8),
                    bg="#f0f0f0", fg="#1e90ff", width=20)\
                .pack(side="left")
            
        Re_Dis_frame = tk.Frame(row, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        for score_type,score_current in data['score']['Employability'].items():
            tk.Label(upper_frame, text=f'{score_current}', font=("Arial", 8),
                    bg="white", fg="#1e90ff", width=13)\
                .pack(side="left")
            
        Re_Dis_frame = tk.Frame(row, bg="#f0f0f0")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        for score_type,score_current in data['score']['Global Engagement'].items():
            tk.Label(upper_frame, text=f'{score_current}', font=("Arial", 8),
                    bg="#f0f0f0", fg="#1e90ff", width=15)\
                .pack(side="left")
            
        Re_Dis_frame = tk.Frame(row, bg="white")
        Re_Dis_frame.pack(side="left", fill='y')
        upper_frame = tk.Frame(Re_Dis_frame,bg= 'white')
        upper_frame.pack(fill='y',padx=5,pady=5)
        for score_type,score_current in data['score']['Sustainability'].items():
            tk.Label(upper_frame, text=f'{score_current}', font=("Arial", 8),
                    bg="white", fg="#1e90ff", width=10)\
                .pack(side="left")

    
    def crawl_data():
        # from models.UniversityModel import UniversityModel
        universities_data = UniversityController.get_all_university()
        global short_list
        global compare_list
        short_list = {}
        compare_list = {}
        for data in universities_data:
            shortList_var = tk.IntVar()
            compare_var = tk.IntVar()
            short_list[data['id']] = shortList_var
            compare_list[data['id']] = compare_var
        return universities_data

    def crawl_data_with_name(event):
        name = entry_search.get()
        uni_data = UniversityController.search_by_name(name)
        global universities_data
        universities_data = uni_data
        number_of_Results.config(text=f"{len(universities_data)} kết quả")
        global short_list
        global compare_list
        short_list = {}
        compare_list = {}
        for data in universities_data:
            shortList_var = tk.IntVar()
            compare_var = tk.IntVar()
            short_list[data['id']] = shortList_var
            compare_list[data['id']] = compare_var
        render_university_list()

    entry_search.bind("<Return>", crawl_data_with_name)
    universities_data = crawl_data()
    number_of_Results.config(text=f"{len(universities_data)} kết quả")
    for data in universities_data:
        shortList_var = tk.IntVar()
        compare_var = tk.IntVar()
        short_list[data['id']] = shortList_var
        compare_list[data['id']] = compare_var
    # Giả sử bạn có ảnh logo trong thư mục assets
    unversities_card_frame = tk.Frame(content_frame, bg="#f8f9fa", padx=50, pady=10)
    unversities_card_frame.pack(fill='x')

    
        # create_university_block(main_content_frame,data)    

    # ===================== Phân trang =================
    pagination_frame = tk.Frame(content_frame, bg="#f8f9fa")
    pagination_frame.pack()

    

    def change_page(delta):
        global current_view_mode
        new_page = current_page.get() + delta
        if 1 <= new_page <= get_total_pages():
            current_page.set(new_page)
            if current_view_mode == 2:
                render_table_view()
            else: 
                render_university_list()

    def go_to_page(page):
        current_page.set(page)
        global current_view_mode
        if current_view_mode == 2:
            render_table_view()
        else: 
            render_university_list()

    def render_pagination_bar():
        for widget in pagination_frame.winfo_children():
            widget.destroy()

        tk.Label(pagination_frame,text="Results per page:",bg="#f8f9fa",font=("Arial", 10, "bold")).pack(side="left", padx=10)
        results_dropdown = tk.OptionMenu(
            pagination_frame,
            results_per_page,
            *results_per_page_options,
            command=lambda _: update_pagination()
        )
        results_dropdown.pack(side="left", padx=10)

        total_pages = get_total_pages()
        page = current_page.get()

        # Prev button
        tk.Button(
            pagination_frame, text="← Prev",
            state="normal" if page > 1 else "disabled",
            command=lambda: change_page(-1)
        ).pack(side="left", padx=5)

        # Page numbers
        for p in range(1, total_pages + 1):
            btn = tk.Button(
                pagination_frame, text=str(p),
                width=3,
                fg="white" if p == page else "black",
                bg="#1e90ff" if p == page else "white",
                command=lambda x=p: go_to_page(x)
            )
            btn.pack(side="left", padx=2)

        # Next button
        tk.Button(
            pagination_frame, text="Next →",
            state="normal" if page < total_pages else "disabled",
            command=lambda: change_page(1)
        ).pack(side="left", padx=5)


    # Pagination states
    results_per_page_options = [5, 10, 20, 50]
    results_per_page = tk.IntVar(value=10) 
    current_page = tk.IntVar(value=1)

    def get_total_pages():
        total = len(universities_data)
        per_page = results_per_page.get()
        return max(1, (total + per_page - 1) // per_page)

    def update_pagination():
        current_page.set(1)  # reset về page 1 mỗi khi đổi số lượng
        global current_view_mode
        if current_view_mode == 2:
            render_table_view()
        else: 
            render_university_list()
    render_pagination_bar()

    per_page = results_per_page.get()
    page = current_page.get()

    start = (page - 1) * per_page
    end = start + per_page

    for data in universities_data[start:end]:
        create_university_block(unversities_card_frame,data)
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

if __name__ == "__main__":
    create_ui()