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
    global user_data
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
    # Để làm nổi bật "Rankings" như trong ảnh
    tk.Button(nav_frame, text=menu_items[0], font=("Arial", 10, "bold"), bg="white", fg="#1e90ff", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame) 
    tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Free Counselling",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    try:
        # Giả sử bạn đã có file search.png trong thư mục assets
        img = Image.open("Abroad-University-Study-Comparison/assets/search.png")
        # img = Image.open("assets/search.png")
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
    
    # ===============================================
    # Phần Nội Dung Chính Bắt Đầu Tại Đây
    # ===============================================
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

    def on_click_detail(id):
        pass

    def on_click_update(id):
        pass 

    def on_click_delete_university(id):
        pass
    
    def on_click_delete_user(id):
        pass

    def render_table_view():
        btn_add.config(text="Thêm tài khoản người dùng")
        quick_view.config(bg='white')
        table_view.config(bg='#f0f0f0')
        global current_view_mode
        current_view_mode = 2
        for widget in unversities_card_frame.winfo_children():
            widget.destroy()
        
        per_page = results_per_page.get()
        page = current_page.get()

        start = (page - 1) * per_page
        end = start + per_page
        for stt, data in enumerate(user_data[start:end], start=1):
            create_university_table_row(unversities_card_frame, data, stt)
        
        render_pagination_bar()

    def render_university_list():
        btn_add.config(text="Thêm trường đại học")
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
    quick_view = tk.Button(view_frame, text="Danh sách trường",width=30,command=render_university_list, font=("Arial", 9), bg="white", relief='flat')
    quick_view.pack(side="left", padx=(0, 1), pady=0)
    table_view = tk.Button(view_frame, text="Danh sách tài khoản",width=30,command=render_table_view ,font=("Arial", 9), bg="#e0e0e0", relief='flat')
    table_view.pack(side="left", padx=(1, 0), pady=0)
    
    # Trường tìm kiếm
    search_entry_frame = tk.Frame(toolbar_frame, bg="white", bd=1, relief='solid')
    search_entry_frame.pack(side="left", fill='y', padx=(0, 20))
    tk.Label(search_entry_frame, image=search_photo, font=("Arial", 10), bg="white").pack(side="left", padx=5)
    entry_search = tk.Entry(search_entry_frame, width=30, font=("Arial", 10), relief='flat')
    entry_search.pack(side="left", padx=5)
    
    # Nút Apply Filters & Compare
    # tk.Button(toolbar_frame, text="So sánh",command=take_compare_universities, fg="white", background="#0013e9", font=("Arial", 9, "bold"), relief='flat').pack(side="right",padx=(20,0))
    btn_add = tk.Button(toolbar_frame, text="Thêm trường đại học", fg="white", background="#1e90ff", font=("Arial", 9, "bold"), relief='flat')
    btn_add.pack(side="right")
    number_of_Results = tk.Label(toolbar_frame, text="2 Results", font=("Arial", 15, "bold"), fg="#555", bg="#f8f9fa") # Khoảng cách mô phỏng
    number_of_Results.pack(side="right", padx=(100, 20))

    # Dropdown "University rank (High to Low)"
    rank_dropdown_frame = tk.Frame(toolbar_frame, bg="#f8f9fa")
    rank_dropdown_frame.pack(side="right")
    tk.Label(rank_dropdown_frame, text="Published on: 19 June 2025", font=("Arial", 8), fg="#555", bg="#f8f9fa").pack(side="left", padx=10)
    
    # tk.Label(rank_dropdown_frame, text="University rank (High to Low) ▼", font=("Arial", 9), fg="#333", bg="white", bd=1, relief='solid', padx=5, pady=2).pack(side="left")
    # selected_modes_filter = ["University rank(High to Low)", "University rank(Low to High)"]
    # selected_mode = tk.StringVar()
    # selected_mode.set("University rank(High to Low)")
    # selected_modes_filter_dropdown = tk.OptionMenu(rank_dropdown_frame,selected_mode,*selected_modes_filter)
    # selected_modes_filter_dropdown.pack(side='left',padx=5,pady=2)

    # def on_sort_change(*args):
    #     mode = selected_mode.get()

    #     if mode == "University rank(High to Low)":
    #         universities_data.sort(key=lambda x: x['overall_score'], reverse=True)
    #     else:
    #         universities_data.sort(key=lambda x: x['overall_score'])

    #     # # Cập nhật rank theo thứ tự mới
    #     # for idx, uni in enumerate(universities_data, start=1):
    #     #     uni['rank'] = idx
    #     global current_view_mode
    #     if current_view_mode == 2:
    #         render_table_view()
    #     else:
    #         render_university_list()
            

    # selected_mode.trace("w", on_sort_change)
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
        rank_score_frame.pack(side="left", padx=(150, 150))
        
        # tk.Label(rank_score_frame, text="Rank", font=("Arial", 8), fg="#888", bg="white").pack(anchor="w")
        tk.Label(rank_score_frame, text=data['rank'], font=("Arial", 28, "bold"), fg="#333", bg="white").pack(anchor="w")
        
        # tk.Label(rank_score_frame, text="Overall Score:", font=("Arial", 9), fg="#888", bg="white").pack(anchor="w", pady=(10, 0))
        # if data['overall_score'] != 0.0:
        #     tk.Label(rank_score_frame, text=data['overall_score'], font=("Arial", 14, "bold"), fg="#333", bg="white").pack(anchor="w")
        # else:
        #     tk.Label(rank_score_frame, text="Không có dữ liệu", font=("Arial", 14, "bold"), fg="#333", bg="white").pack(anchor="w")

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
            # logo_label.pack(padx=(0, 10))
            images_reference.append(tk_image) # Lưu reference
        except FileNotFoundError:
            tk.Label(header_details_frame, text="[Logo]", font=("Arial", 8), bg="white", fg="gray", width=5).pack(side="left", padx=(0, 10))
        
        name_loc_frame = tk.Frame(header_details_frame, bg="white")
        name_loc_frame.pack(side="left", fill='y')
        # name_loc_frame.pack(fill='y')

        university_name = tk.Label(name_loc_frame, text=data['name'], font=("Arial", 14, "bold"), fg="#1e90ff", bg="white")
        university_name.pack(anchor="w")
        university_name.bind("<Button-1>",lambda event: link_to_detail(event,data['id']))
        tk.Label(name_loc_frame, text=f'{data['city']}, {data['country']}', font=("Arial", 10), fg="#555", bg="white").pack(anchor="w")

        # Nút Shortlist và Compare
        action_frame = tk.Frame(header_details_frame, bg="white")
        action_frame.pack(side="right")
        # tk.Button(action_frame, text="Shortlist", font=("Arial", 9), bg="white", relief='flat').pack(side="left", padx=5)

        img = Image.open("Abroad-University-Study-Comparison/assets/detail_icon.png")
        # img = Image.open("assets/detail_icon.png")
        img = img.resize((24, 24), Image.LANCZOS)
        detail_photo = ImageTk.PhotoImage(img)
        # tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        tk.Button(action_frame, command=lambda name=data['id']: on_click_detail(name), image=detail_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        images_reference.append(detail_photo)

        img = Image.open("Abroad-University-Study-Comparison/assets/updates_icon.png")
        # img = Image.open("assets/updates_icon.png")
        img = img.resize((24, 24), Image.LANCZOS)
        update_photo = ImageTk.PhotoImage(img)
        # tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        tk.Button(action_frame, command= lambda name=data['id']: on_click_update(name), image=update_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        images_reference.append(update_photo)

        img = Image.open("Abroad-University-Study-Comparison/assets/delete_icon.png")
        # img = Image.open("assets/delete_icon.png")
        img = img.resize((24, 24), Image.LANCZOS)
        delete_photo = ImageTk.PhotoImage(img)
        # tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        tk.Button(action_frame, command= lambda name=data['id']: on_click_delete_university(name), image=delete_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        images_reference.append(delete_photo)    


    def create_university_table_row(parent, data, stt):
        uni_block = tk.Frame(parent, bg="white", bd=1, relief='solid', padx=20, pady=15)
        uni_block.pack(fill='x', pady=15)

        # Cột 1: Rank và Score
        rank_score_frame = tk.Frame(uni_block, bg="white")
        rank_score_frame.pack(side="left", padx=(150, 150))
        
        # tk.Label(rank_score_frame, text="Rank", font=("Arial", 8), fg="#888", bg="white").pack(anchor="w")
        tk.Label(rank_score_frame, text=stt, font=("Arial", 28, "bold"), fg="#333", bg="white").pack(anchor="w")

        # Cột 2: Logo và Tên Trường
        details_frame = tk.Frame(uni_block, bg="white")
        details_frame.pack(side="left", fill='x', expand=True)

        header_details_frame = tk.Frame(details_frame, bg="white")
        header_details_frame.pack(fill='x', pady=(0, 10))

        name_loc_frame = tk.Frame(header_details_frame, bg="white")
        name_loc_frame.pack(side="left", fill='y')
        # name_loc_frame.pack(fill='y')

        user_name = tk.Label(name_loc_frame, text=data['name']+"_"+data['id'], font=("Arial", 14, "bold"), fg="#1e90ff", bg="white")
        user_name.pack(anchor="w")
        tk.Label(name_loc_frame, text=f'Ngày tạo: {data['datetime']}', font=("Arial", 10), fg="#555", bg="white").pack(anchor="w")

        # Nút Shortlist và Compare
        action_frame = tk.Frame(header_details_frame, bg="white")
        action_frame.pack(side="right")
        # tk.Button(action_frame, text="Shortlist", font=("Arial", 9), bg="white", relief='flat').pack(side="left", padx=5)

        # img = Image.open("Abroad-University-Study-Comparison/assets/detail_icon.png")
        # # img = Image.open("assets/detail_icon.png")
        # img = img.resize((24, 24), Image.LANCZOS)
        # detail_photo = ImageTk.PhotoImage(img)
        # # tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        # tk.Button(action_frame, command=lambda name=data['id']: on_click_detail(name), image=detail_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        # images_reference.append(detail_photo)

        # img = Image.open("Abroad-University-Study-Comparison/assets/updates_icon.png")
        # # img = Image.open("assets/updates_icon.png")
        # img = img.resize((24, 24), Image.LANCZOS)
        # update_photo = ImageTk.PhotoImage(img)
        # # tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        # tk.Button(action_frame, command= lambda name=data['id']: on_click_update(name), image=update_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        # images_reference.append(update_photo)

        img = Image.open("Abroad-University-Study-Comparison/assets/delete_icon.png")
        # img = Image.open("assets/delete_icon.png")
        img = img.resize((24, 24), Image.LANCZOS)
        delete_photo = ImageTk.PhotoImage(img)
        # tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        tk.Button(action_frame, command= lambda name=data['id']: on_click_delete_user(name), image=delete_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
        images_reference.append(delete_photo)   

    
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

    def crawl_data_university_with_name(event):
        if current_view_mode==1:
            name = entry_search.get()
            uni_data = UniversityController.search_by_name(name)
            global universities_data
            universities_data = uni_data
            number_of_Results.config(text=f"{len(universities_data)} Results")
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
        else:
            render_table_view()

    entry_search.bind("<Return>", crawl_data_university_with_name)
    
    universities_data = crawl_data()
    user_data = [
        {
            'id': '1',
            'name': 'Corn Thị Tú Khuyên',
            'datetime': '22/11/2025 10:11:12'
        },
        {
            'id': '2',
            'name': 'Nguyễn Mountain River',
            'datetime': '23/11/2025 11:12:13'
        },
        {
            'id': '3',
            'name': 'Cloud Sound Forest',
            'datetime': '24/11/2025 12:13:14'
        }
    ]
    if current_view_mode==1:
        number_of_Results.config(text=f"{len(universities_data)} Results")
    else:
        number_of_Results.config(text=f"{len(user_data)} Results")
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
        if current_view_mode==1:
            total = len(universities_data)
        else:
            total = len(user_data)
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
    # social_icons = ["assets/104498_facebook_icon.png", 
    #                 "assets/1161953_instagram_icon.png", 
    #                 "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
    #                 "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    social_icons = ["Abroad-University-Study-Comparison/assets/104498_facebook_icon.png", 
                    "Abroad-University-Study-Comparison/assets/1161953_instagram_icon.png", 
                    "Abroad-University-Study-Comparison/assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
                    "Abroad-University-Study-Comparison/assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    for icon in social_icons:
        try:
            img = Image.open(icon)
            img = img.resize((15, 15), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            # Dùng label thay vì nút để mô phỏng icon
            icon_label = tk.Label(social_frame, image=photo, bg="#007bff") 
            icon_label.pack(side="left", padx=3)
            images_reference.append(photo)
        except FileNotFoundError:
             tk.Label(social_frame, text="[Icon]", font=("Arial", 7), bg="#007bff", fg="gray").pack(side="left", padx=3)
        
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