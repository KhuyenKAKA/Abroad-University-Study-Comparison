import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from controller.UniversityController import UniversityController
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests 
from db import get_connection

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
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    
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
    # tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    # tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    # tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    # tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    # tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)
    tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    # tk.Button(right_nav_frame, text="Free Counselling",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    try:
        # Giả sử bạn đã có file search.png trong thư mục assets
        img = Image.open("Abroad-University-Study-Comparison/assets/search.png")
        # img = Image.open("assets/search.png")
        img = img.resize((24, 24), Image.LANCZOS)
        search_photo = ImageTk.PhotoImage(img)
        tk.Button(right_nav_frame, image=search_photo,bg= 'white',relief='flat').pack(side='left', padx=5)
    except FileNotFoundError:
        tk.Label(right_nav_frame, text="🔍", font=("Arial", 16), bg="white").pack(side='left', padx=5)
    
    def logout_action():
        if mess.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?"):
            from controller.AuthController import AuthController
            AuthController.logout()
            from ui.HomePageUI import create_ui as create_homepage_ui
            root.destroy()
            create_homepage_ui()
    # tk.Button(right_nav_frame, text="👤", foreground='white',command= link_to_personal_infor, background="#1F3AB0").pack(side='left', padx=5)
    tk.Button(right_nav_frame, text="Đăng xuất", foreground='white', background="#1F3AB0", command= logout_action).pack(side='left', padx=5)
    # tk.Button(right_nav_frame, text="Đăng ký", foreground='white', background="#1F3AB0").pack(side='left', padx=5)

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

    def on_click_update(university_id):
        def update_university_form(university_id):
            mydb = get_connection()
            cursor = mydb.cursor()
            def get_university_data(university_id):
                # ========= BASIC =========
                cursor.execute("""
                    SELECT u.name, u.region, c.name, u.city, u.logo, u.overall_score, u.rank_int, u.path
                    FROM universities u
                    JOIN countries c ON u.country_id = c.id
                    WHERE u.id = %s
                """, (university_id,))
                basic_fields = ["title", "region", "country", "city", "logo", "overall_score", "rank", "path"]
                basic_entries = {}
                basic = cursor.fetchone()
                for i, data  in enumerate(basic):
                    basic_entries[basic_fields[i]] = data

                # ========= DETAIL =========
                cursor.execute("""
                    SELECT * FROM detail_infors
                    WHERE university_id = %s
                """, (university_id,))
                detail = cursor.fetchone()
                detail_keys = [
                        'id','uid','fee', 'scholarship', 'domestic', 'international',
                        'english_test', 'academic_test', 'total_stu',
                        'ug_rate', 'pg_rate', 'inter_total',
                        'inter_ug_rate', 'inter_pg_rate'
                    ]
                detail_entries = {}
                for i, data  in enumerate(detail):
                    detail_entries[detail_keys[i]] = data


                # ========= SCORES =========
                cursor.execute("""
                    SELECT 
                        st.name as category,
                        i.id as indicator_id,
                        i.name as indicator_name,
                        s.rank_int,
                        s.score
                    FROM scores s
                    JOIN indicators i ON s.indicator_id = i.id
                    JOIN score_types st ON s.score_type_id = st.id
                    WHERE s.university_id = %s
                """, (university_id,))
                scores = {}
                for cat_name, inid, inname, inrank, inscore in cursor.fetchall(): 
                    if cat_name not in scores:
                        scores[cat_name] = []
                        scores[cat_name].append(
                            {
                            "indicator_id": inid,
                            "indicator_name": inname,
                            "rank": inrank,#entry
                            "score": inscore#entry
                        })
                    else:
                        scores[cat_name].append(
                            {
                            "indicator_id": inid,
                            "indicator_name": inname,
                            "rank": inrank,#entry
                            "score": inscore#entry
                        })

                # ========= ENTRY =========
                cursor.execute("""
                    SELECT *
                    FROM entry_infor
                    WHERE university_id = %s
                """, (university_id,))
                entry = cursor.fetchall()
                entry_details = {
                    'bachelor':{
                        "exists": False,#entry -> checkbox
                        "SAT": None,#entry
                        "GRE": None,#entry
                        "GMAT": None,#entry
                        "ACT": None,#entry
                        "ATAR" :None,#entry
                        "GPA":None,#entry
                        "TOEFL": None,#entry
                        "IELTS": None#entry
                    },
                    'master':{
                        "exists": False,#entry -> checkbox
                        "SAT": None,#entry
                        "GRE": None,#entry
                        "GMAT": None,#entry
                        "ACT": None,#entry
                        "ATAR" :None,#entry
                        "GPA":None,#entry
                        "TOEFL": None,#entry
                        "IELTS": None#entry
                    }
                }
                for id, university_id, degree_type, sat, gre, gmat, act, atar, gpa, toefl, ielts in entry:
                    if int(degree_type) == 1:
                        entry_details['bachelor'] ={
                            "exists": True,#entry -> checkbox
                            "SAT": sat,#entry
                            "GRE": gre,#entry
                            "GMAT": gmat,#entry
                            "ACT": act,#entry
                            "ATAR" :atar,#entry
                            "GPA":gpa,#entry
                            "TOEFL": toefl,#entry
                            "IELTS": ielts#entry
                        }
                    if int(degree_type) == 2:
                        entry_details['master'] ={
                            "exists": True,#entry -> checkbox
                            "SAT": sat,#entry
                            "GRE": gre,#entry
                            "GMAT": gmat,#entry
                            "ACT": act,#entry
                            "ATAR" :atar,#entry
                            "GPA":gpa,#entry
                            "TOEFL": toefl,#entry
                            "IELTS": ielts#entry
                        }
                return {
                    "basic": basic_entries,
                    "detail": detail_entries,
                    "scores": scores,
                    "entry": entry_details
                }

            cursor.execute("SELECT region FROM universities")
            region_data = [x[0] for x in cursor.fetchall() if x[0] is not None]
            region_data = list(dict.fromkeys(region_data))
            region_data.sort()

            cursor.execute("""
                SELECT c.name 
                FROM universities u 
                JOIN countries c ON u.country_id = c.id
            """)
            country_data = [x[0] for x in cursor.fetchall() if x[0] is not None]
            country_data = list(dict.fromkeys(country_data))
            country_data.sort()

            window = tk.Toplevel(root)
            window.title("Create University Data")
            window.geometry("700x700")
            def only_int(P):
                return P.isdigit() or P == ""
            vcmd = window.register(only_int)

            canvas = tk.Canvas(window)
            scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
            frame = ttk.Frame(canvas)

            frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            def on_mouse_wheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind_all("<MouseWheel>", on_mouse_wheel)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # ========== BASIC INFO ==========
            ttk.Label(frame, text="BASIC UNIVERSITY INFORMATION", font=("Segoe UI", 14, "bold")).pack(pady=5)
            # basic_fields = ["title", "region", "country", "city", "logo", "overall_score", "rank", "path"]
            basic_fields = ["title", "region", "country", "city", "logo", "overall_score", "rank",  "path"]
            basic_entries = {}

            box = ttk.LabelFrame(frame, text="Basic Info")
            box.pack(padx=10, pady=5, fill="x")

            for i, field in enumerate(basic_fields):
                if field == "region":
                    ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    e = ttk.Combobox(box, values=region_data,
                                        width=47, height=6, state="readonly")
                    e.grid(row=i, column=1, padx=5, pady=3)
                    basic_entries[field] = e
                elif field == "country":
                    ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    e = ttk.Combobox(box, values=country_data,
                                        width=47, height=6, state="readonly")
                    e.grid(row=i, column=1, padx=5, pady=3)
                    basic_entries[field] = e
                else:   
                    ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    e = ttk.Entry(box, width=50)
                    e.grid(row=i, column=1, padx=5, pady=3)
                    basic_entries[field] = e

            # ========== SCORES ==========
            ttk.Label(frame, text="SCORES - <RANK - SCORE>", font=("Segoe UI", 14, "bold")).pack(pady=5)

            categories = {
                "Research & Discovery": [("Citations per Faculty", '73'), ("Academic Reputation", '76')],
                "Learning Experience": [("Faculty Student Ratio", '36')],
                "Employability": [("Employer Reputation", '77'), ("Employment Outcomes",'3819456' )],
                "Global Engagement": [
                    ("International Student Ratio", '14'),
                    ("International Research Network", '15'),
                    ("International Faculty Ratio", '18'),
                    ("International Student Diversity", '3924415')
                ],
                "Sustainability": [("Sustainability Score", '3897497')]
            }

            score_entries = {}

            for cat, indicators in categories.items():
                cf = ttk.LabelFrame(frame, text=cat)
                cf.pack(padx=10, pady=4, fill="x")

                score_entries[cat] = []

                for i, (name, id) in enumerate(indicators):
                    ttk.Label(cf, text=name).grid(row=i, column=0, sticky="w")

                    r = ttk.Entry(cf, validate="key", validatecommand=(vcmd, "%P"),width=8)
                    r.grid(row=i, column=1, padx=2)
                    r.insert(0, "")

                    s = ttk.Entry(cf, width=8)
                    s.grid(row=i, column=2, padx=2)
                    s.insert(0, "")
                    score_entries[cat].append((id, name, r, s))

            # ========== DETAIL INFOS ==========
            ttk.Label(frame, text="DETAIL INFORS", font=("Segoe UI", 14, "bold")).pack(pady=5)

            detail_keys = [
                'fee', 'scholarship', 'domestic', 'international',
                'english_test', 'academic_test', 'total_stu',
                'ug_rate', 'pg_rate', 'inter_total',
                'inter_ug_rate', 'inter_pg_rate'
            ]

            detail_entries = {}
            df = ttk.LabelFrame(frame, text="Detail Infos")
            df.pack(padx=10, pady=5, fill="x")

            for i, key in enumerate(detail_keys):
                ttk.Label(df, text=key).grid(row=i, column=0, sticky="w", padx=4)
                e = ttk.Entry(df, width=40)
                e.grid(row=i, column=1, padx=4)
                detail_entries[key] = e

            # ========== ENTRY INFORS ==========
            ttk.Label(frame, text="ENTRY REQUIREMENTS", font=("Segoe UI", 14, "bold")).pack(pady=5)

            entry_data = {}
            entry_frame = ttk.LabelFrame(frame, text="Entry Info")
            entry_frame.pack(padx=10, pady=5, fill="x")

            for col, level in enumerate(["bachelor", "master"]):
                lf = ttk.LabelFrame(entry_frame, text=level.upper())
                lf.grid(row=0, column=col, padx=20, pady=5)

                exists = tk.BooleanVar()
                ttk.Checkbutton(lf, text="Exists", variable=exists).grid(row=0, column=0, sticky="w")

                fields = ["SAT", "GRE", "GMAT", "ACT", "ATAR", "GPA", "TOEFL", "IELTS"]

                entry_data[level] = {"exists": exists, "entries": {}}

                for i, f in enumerate(fields, 1):
                    ttk.Label(lf, text=f).grid(row=i, column=0, sticky="w")
                    e = ttk.Entry(lf,  width=25)
                    e.grid(row=i, column=1)
                    entry_data[level]["entries"][f] = e
            
            def load_to_form(university_id):

                data = get_university_data(university_id)

                # ========== BASIC ==========
                for i, field in enumerate(basic_fields):
                    if field == "region":
                        basic_entries[field].set(data['basic']['region'])
                    elif field == "country":
                        basic_entries[field].set(data['basic']['country'])
                    else:   
                        basic_entries[field].delete('0',tk.END)
                        basic_entries[field].insert(tk.END, data['basic'][field])

                # ========== SCORES ==========

                categories = {
                    "Research & Discovery": [("Citations per Faculty", '73'), ("Academic Reputation", '76')],
                    "Learning Experience": [("Faculty Student Ratio", '36')],
                    "Employability": [("Employer Reputation", '77'), ("Employment Outcomes",'3819456' )],
                    "Global Engagement": [
                        ("International Student Ratio", '14'),
                        ("International Research Network", '15'),
                        ("International Faculty Ratio", '18'),
                        ("International Student Diversity", '3924415')
                    ],
                    "Sustainability": [("Sustainability Score", '3897497')]
                }


                for cat, indicators in categories.items():
                    for (id, name, r, s) in score_entries[cat]:
                        old_r, old_s = "", ""
                        for x in data['scores'][cat]:
                            if  x['indicator_name'] == name:
                                old_r = x["rank"]
                                old_s = x['score']
                        
                        r.delete('0',tk.END)
                        s.delete('0',tk.END)
                        if old_r == None:
                            r.insert(tk.END,"")
                        else: 
                            r.insert(tk.END, str(old_r))
                        if old_s == None:
                            s.insert(tk.END,"")
                        else: 
                            s.insert(tk.END, str(old_s))

                # ========== DETAIL INFOS ==========
                detail_keys = [
                    'fee', 'scholarship', 'domestic', 'international',
                    'english_test', 'academic_test', 'total_stu',
                    'ug_rate', 'pg_rate', 'inter_total',
                    'inter_ug_rate', 'inter_pg_rate'
                ]

                for i, key in enumerate(detail_keys):
                    detail_entries[key].delete('0',tk.END)
                    if data['detail'][key] == None:
                        detail_entries[key].insert(tk.END, '')
                    else:
                        detail_entries[key].insert(tk.END, str(data['detail'][key]))
                    # print(data['detail'][key])

                # # ========== ENTRY INFORS ==========
                
                for col, level in enumerate(["bachelor", "master"]):
                    fields = ["SAT", "GRE", "GMAT", "ACT", "ATAR", "GPA", "TOEFL", "IELTS"]
                    if data['entry'][level]['exists'] == True:
                        entry_data[level]['exists'].set(1) 
                        for i, f in enumerate(fields, 1):
                            entry_data[level]["entries"][f].delete('0',tk.END)
                            entry_data[level]["entries"][f].insert('0',str(data['entry'][level][f]))
                        

            load_to_form(university_id)
            # ========== GENERATE DATA ==========
            def generate_data():

                data = {}
                if not basic_entries['title'].get():
                    mess.showerror("Thiếu tên trường","Xin hãy nhập tên trường!")
                    return
                if not basic_entries['region'].get():
                    mess.showerror("Thiếu tên khu vực","Xin hãy chọn khu vực!")
                    return
                if not basic_entries['country'].get():
                    mess.showerror("Thiếu tên quốc gia","Xin hãy chọn quốc gia!")
                    return
                if not basic_entries['rank'].get():
                    mess.showerror("Thiếu thứ hạng","Xin hãy nhập thứ hạng!")
                    return
                for k, e in basic_entries.items():
                    data[k] = e.get()
                    if k == 'overall_score' and not e.get():
                        data[k] = "0"

                # scores
                data["scores"] = {}
                for cat, indicators in score_entries.items():
                    data["scores"][cat] = []
                    for id, name, r, s in indicators:
                        data["scores"][cat].append({
                            "indicator_id": f"{id}",
                            "indicator_name": name,
                            "rank": r.get(),
                            "score": s.get()
                        })

                # detail_infors
                data["detail_infors"] = {}
                for k, e in detail_entries.items():
                    val = e.get()
                    data["detail_infors"][k] = val if val != "" else None

                # entry_infor
                data["entry_infor"] = {}

                for level in entry_data:
                    data["entry_infor"][level] = {}
                    data["entry_infor"][level]["exists"] = entry_data[level]["exists"].get()
                    for k, e in entry_data[level]["entries"].items():
                        v = e.get()
                        data["entry_infor"][level][k] = v if v != "" else None
                result = mess.askyesno("Xác nhận", "Bạn có muốn cập nhật thông tin của trường này không?")
                if result:
                    UniversityController.update_university(data, university_id)
                    mess.showinfo("Thanh cong","Cap nhat thong tin truong hoc thanh cong!")

            # print(get_university_data(1521))
            tk.Button(frame,bg= "#0013e9", fg='white' ,text="Cập nhật thông tin trường", command=generate_data).pack(pady=15)
            window.mainloop()
        
        if current_view_mode == 1:
            update_university_form(university_id)
        else:
            from ui.AddAccountUI import create_update_ui as create_update
            root.destroy()
            create_update(university_id)

    def on_click_delete_university(id):
        result = mess.askyesno("Xác nhận xóa","Bạn có chắc chắn muốn xóa chứ?")
        if result:
            UniversityController.delete_university(id)
            mess.showinfo("Da xoa", "Ban da xoa thanh cong")
            global universities_data
            universities_data = crawl_data()
            render_university_list()
        
    
    def on_click_delete_user(id):
        conn = get_connection()
        cursor = conn.cursor()
        # cursor.execute("use universities_db")
        # xóa study_bg
        result = mess.askyesno("Xác nhận","Bạn muốn xóa người dùng này chứ?")
        if result:
            cursor.execute("DELETE FROM study_bg WHERE user_id=%s", (id,))
            # xóa users
            cursor.execute("DELETE FROM users WHERE id=%s", (id,))
            conn.commit()
            global user_data 
            user_data = crawl_user()
            render_table_view()

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

        number_of_Results.config(text=f'{len(user_data)} kết quả')
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

        render_pagination_bar()
        for data in universities_data[start:end]:
            create_university_block(unversities_card_frame, data)

        
    

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
    
    def create_university_form():
        if current_view_mode == 1:
            mydb = get_connection()
            cursor = mydb.cursor()
            cursor.execute("SELECT region FROM universities")
            region_data = [x[0] for x in cursor.fetchall() if x[0] is not None]
            region_data = list(dict.fromkeys(region_data))
            region_data.sort()

            cursor.execute("""
                SELECT c.name 
                FROM universities u 
                JOIN countries c ON u.country_id = c.id
            """)
            country_data = [x[0] for x in cursor.fetchall() if x[0] is not None]
            country_data = list(dict.fromkeys(country_data))
            country_data.sort()

            window = tk.Toplevel(root)
            window.title("Create University Data")
            window.geometry("700x700")
            def only_int(P):
                return P.isdigit() or P == ""
            vcmd = window.register(only_int)

            canvas = tk.Canvas(window)
            scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
            frame = ttk.Frame(canvas)

            frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            def on_mouse_wheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind_all("<MouseWheel>", on_mouse_wheel)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # ========== BASIC INFO ==========
            ttk.Label(frame, text="BASIC UNIVERSITY INFORMATION", font=("Segoe UI", 14, "bold")).pack(pady=5)

            basic_fields = ["title", "path", "region", "country", "city", "logo", "overall_score", "rank"]
            basic_entries = {}

            box = ttk.LabelFrame(frame, text="Basic Info")
            box.pack(padx=10, pady=5, fill="x")

            for i, field in enumerate(basic_fields):
                if field == "region":
                    ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    e = ttk.Combobox(box, values=region_data,
                                        width=47, height=6, state="readonly")
                    e.grid(row=i, column=1, padx=5, pady=3)
                    basic_entries[field] = e
                elif field == "country":
                    ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    e = ttk.Combobox(box, values=country_data,
                                        width=47, height=6, state="readonly")
                    e.grid(row=i, column=1, padx=5, pady=3)
                    basic_entries[field] = e
                else:   
                    ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    e = ttk.Entry(box, width=50)
                    e.grid(row=i, column=1, padx=5, pady=3)
                    basic_entries[field] = e

            # ========== SCORES ==========
            ttk.Label(frame, text="SCORES - <RANK - SCORE>", font=("Segoe UI", 14, "bold")).pack(pady=5)

            categories = {
                "Research & Discovery": [("Citations per Faculty", '73'), ("Academic Reputation", '76')],
                "Learning Experience": [("Faculty Student Ratio", '36')],
                "Employability": [("Employer Reputation", '77'), ("Employment Outcomes",'3819456' )],
                "Global Engagement": [
                    ("International Student Ratio", '14'),
                    ("International Research Network", '15'),
                    ("International Faculty Ratio", '18'),
                    ("International Student Diversity", '3924415')
                ],
                "Sustainability": [("Sustainability Score", '3897497')]
            }

            score_entries = {}

            for cat, indicators in categories.items():
                cf = ttk.LabelFrame(frame, text=cat)
                cf.pack(padx=10, pady=4, fill="x")

                score_entries[cat] = []

                for i, (name, id) in enumerate(indicators):
                    ttk.Label(cf, text=name).grid(row=i, column=0, sticky="w")

                    r = ttk.Entry(cf, validate="key", validatecommand=(vcmd, "%P"),width=8)
                    r.grid(row=i, column=1, padx=2)
                    r.insert(0, "")

                    s = ttk.Entry(cf, width=8)
                    s.grid(row=i, column=2, padx=2)
                    s.insert(0, "")

                    score_entries[cat].append((id, name, r, s))

            # ========== DETAIL INFOS ==========
            ttk.Label(frame, text="DETAIL INFORS", font=("Segoe UI", 14, "bold")).pack(pady=5)

            detail_keys = [
                'fee', 'scholarship', 'domestic', 'international',
                'english_test', 'academic_test', 'total_stu',
                'ug_rate', 'pg_rate', 'inter_total',
                'inter_ug_rate', 'inter_pg_rate'
            ]

            detail_entries = {}
            df = ttk.LabelFrame(frame, text="Detail Infos")
            df.pack(padx=10, pady=5, fill="x")

            for i, key in enumerate(detail_keys):
                ttk.Label(df, text=key).grid(row=i, column=0, sticky="w", padx=4)
                e = ttk.Entry(df, validate="key", validatecommand=(vcmd, "%P"), width=40)
                e.grid(row=i, column=1, padx=4)
                detail_entries[key] = e

            # ========== ENTRY INFORS ==========
            ttk.Label(frame, text="ENTRY REQUIREMENTS", font=("Segoe UI", 14, "bold")).pack(pady=5)

            entry_data = {}
            entry_frame = ttk.LabelFrame(frame, text="Entry Info")
            entry_frame.pack(padx=10, pady=5, fill="x")

            for col, level in enumerate(["bachelor", "master"]):
                lf = ttk.LabelFrame(entry_frame, text=level.upper())
                lf.grid(row=0, column=col, padx=20, pady=5)

                exists = tk.BooleanVar()
                ttk.Checkbutton(lf, text="Exists", variable=exists).grid(row=0, column=0, sticky="w")

                fields = ["SAT", "GRE", "GMAT", "ACT", "ATAR", "GPA", "TOEFL", "IELTS"]

                entry_data[level] = {"exists": exists, "entries": {}}

                for i, f in enumerate(fields, 1):
                    ttk.Label(lf, text=f).grid(row=i, column=0, sticky="w")
                    e = ttk.Entry(lf, validate="key", validatecommand=(vcmd, "%P"), width=25)
                    e.grid(row=i, column=1)
                    entry_data[level]["entries"][f] = e

            # ========== GENERATE DATA ==========
            def generate_data():
                data = {}
                if not basic_entries['title'].get():
                    mess.showerror("Thiếu tên trường","Xin hãy nhập tên trường!")
                    return
                if not basic_entries['region'].get():
                    mess.showerror("Thiếu tên khu vực","Xin hãy chọn khu vực!")
                    return
                if not basic_entries['country'].get():
                    mess.showerror("Thiếu tên quốc gia","Xin hãy chọn quốc gia!")
                    return
                if not basic_entries['rank'].get():
                    mess.showerror("Thiếu thứ hạng","Xin hãy nhập thứ hạng!")
                    return
                for k, e in basic_entries.items():
                    data[k] = e.get()
                    if k == 'overall_score' and not e.get():
                        data[k] = "0"

                # scores
                data["scores"] = {}
                for cat, indicators in score_entries.items():
                    data["scores"][cat] = []
                    for id, name, r, s in indicators:
                        data["scores"][cat].append({
                            "indicator_id": f"{id}",
                            "indicator_name": name,
                            "rank": r.get(),
                            "score": s.get()
                        })

                # detail_infors
                data["detail_infors"] = {}
                for k, e in detail_entries.items():
                    val = e.get()
                    data["detail_infors"][k] = val if val != "" else None

                # entry_infor
                data["entry_infor"] = {}

                for level in entry_data:
                    data["entry_infor"][level] = {}
                    data["entry_infor"][level]["exists"] = entry_data[level]["exists"].get()

                    for k, e in entry_data[level]["entries"].items():
                        v = e.get()
                        data["entry_infor"][level][k] = v if v != "" else None
                UniversityController.add_university(data)
                mess.showinfo("Thành công", "Bạn đã thêm thành công!")
                window.destroy()
            tk.Button(frame,bg= "#0013e9", fg='white' ,text="Thêm trường đại học", command=generate_data).pack(pady=15)
            window.mainloop()
        else:
            from ui.AddAccountUI import create_ui as create_ui_add_user 
            root.destroy()
            create_ui_add_user()



    # tk.Button(toolbar_frame, text="So sánh",command=take_compare_universities, fg="white", background="#0013e9", font=("Arial", 9, "bold"), relief='flat').pack(side="right",padx=(20,0))
    btn_add = tk.Button(toolbar_frame, text="Thêm trường đại học",command= create_university_form, fg="white", background="#1e90ff", font=("Arial", 9, "bold"), relief='flat')
    btn_add.pack(side="right")
    number_of_Results = tk.Label(toolbar_frame, text="2 Results", font=("Arial", 15, "bold"), fg="#555", bg="#f8f9fa") # Khoảng cách mô phỏng
    number_of_Results.pack(side="right", padx=(100, 20))

    # Dropdown "University rank (High to Low)"
    rank_dropdown_frame = tk.Frame(toolbar_frame, bg="#f8f9fa")
    rank_dropdown_frame.pack(side="right")
    tk.Label(rank_dropdown_frame, text="Thông tin từ ngày: 19/06/2025", font=("Arial", 8), fg="#555", bg="#f8f9fa").pack(side="left", padx=10)
    
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
            if data['logo']:
                response = requests.get(data['logo'])
                image_data = BytesIO(response.content)
                pil_image = Image.open(image_data)
                pil_image = pil_image.resize((70, 70), Image.Resampling.LANCZOS)
                tk_image = ImageTk.PhotoImage(pil_image)
                logo_label = tk.Label(header_details_frame, image=tk_image, bg="white")
                logo_label.pack(side="left", padx=(0, 10))
                # logo_label.pack(padx=(0, 10))
                images_reference.append(tk_image) # Lưu reference
            else:
                tk.Label(header_details_frame, text="[Logo]", font=("Arial", 8), bg="white", fg="gray", width=5).pack(side="left", padx=(0, 10))    
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
    def crawl_user():
        querry = '''
        select id, first_name, last_name, insert_date from users  
        '''
        from db import get_connection
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute(querry)
        result = []
        for id, first, last, date in cursor.fetchall():
            result.append(
                {
                    'id': str(id),
                    'name': last+ first,
                    'datetime': date
                }
            )
        return result
    def crawl_data_university_with_name(event):
        if current_view_mode==1:
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
        else:
            render_table_view()

    entry_search.bind("<Return>", crawl_data_university_with_name)
    
    universities_data = crawl_data()
    user_data = crawl_user()
    if current_view_mode==1:
        number_of_Results.config(text=f"{len(universities_data)} kết quả")
    else:
        number_of_Results.config(text=f"{len(user_data)} kết quả")
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

        tk.Label(pagination_frame,text="Kết quả trên mỗi trang:",bg="#f8f9fa",font=("Arial", 10, "bold")).pack(side="left", padx=10)
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
            pagination_frame, text="← Trước",
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
            pagination_frame, text="Sau →",
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