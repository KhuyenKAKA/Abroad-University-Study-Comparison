
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PIL import Image, ImageTk
import ui.session as session_data
from ui.HomePageUI import create_ui as home_page_ui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controller.AuthController import AuthController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
line_data = [
    {"name": "Trường 1", "SAT": 1200, "GRE": 320, "GMAT": 600, "ACT": 29, "ATAR": 85, "GPA": 3.5, "TOEFL": 95, "IELTS": 6.5},
    {"name": "Trường 2", "SAT": 1250, "GRE": 315, "GMAT": 650, "ACT": 28, "ATAR": 80, "GPA": 3.2, "TOEFL": 100, "IELTS": 7.0},
    {"name": "Trường 3", "SAT": 1100, "GRE": 300, "GMAT": 580, "ACT": 26, "ATAR": 75, "GPA": 3.0, "TOEFL": 90, "IELTS": 6.0},
]

criteria = ["SAT", "GRE", "GMAT", "ACT", "ATAR", "GPA", "TOEFL", "IELTS"]
def create_ui():

    root = tk.Tk()
    root.title("UniCompare - Định hướng tương lai cùng bạn")
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
    btnRankings = tk.Button(nav_frame, text=menu_items[0], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=1, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnDiscover = tk.Button(nav_frame, text=menu_items[1], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=2, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnEvents = tk.Button(nav_frame, text=menu_items[2], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=3, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnPrepare = tk.Button(nav_frame, text=menu_items[3], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=4, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnScholarships = tk.Button(nav_frame, text=menu_items[4], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=5, padx=5, pady=10, sticky="e", in_=nav_frame)
    btnChatToStudents = tk.Button(nav_frame, text=menu_items[5], font=("Arial", 10), bg="white", relief="flat").grid(row=0, column=6, padx=5, pady=10, sticky="e", in_=nav_frame)
    
    right_nav_frame = tk.Frame(nav_frame, bg="white")
    right_nav_frame.grid(row=0, column=7, sticky="e", padx=(0, 20))

    tk.Button(right_nav_frame, text="Tư vấn miễn phí",foreground='white', background='#28a745', ).pack(side='left', padx=5)
    
    try:
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

    # content_frame đã được cấu hình mở rộng hàng 0 và hàng 1
    content_frame.grid_rowconfigure(0, weight=1)# Hàng 0: Table
    content_frame.grid_rowconfigure(1, weight=1) # Hàng 1: Chart
    content_frame.grid_rowconfigure(2, weight=0) # Hàng 2: Footer (Weight 0 so it doesn't grow)
    content_frame.grid_columnconfigure(0, weight=1)


    frame_table = tk.Frame(content_frame, bg="#e8f0fe") 

    frame_table.grid(row=0, column=0, sticky="nsew") 

    frame_chart = tk.Frame(content_frame, bg="#dfe7fd")

    frame_chart.grid(row=1, column=0, sticky="nsew") 

    draw_chart_in_frame(frame_chart, criteria, line_data)

    # ===============================================
    # Phần Footer
    # ===============================================

    footer_frame = tk.Frame(content_frame, bg="white", padx=50, pady=40)

    footer_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
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
    # social_icons = ["Abroad-University-Study-Comparison/assets/104498_facebook_icon.png", 
    #                 "Abroad-University-Study-Comparison/assets/1161953_instagram_icon.png", 
    #                 "Abroad-University-Study-Comparison/assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
    #                 "Abroad-University-Study-Comparison/assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    social_icons = ["assets/104498_facebook_icon.png", 
                    "assets/1161953_instagram_icon.png", 
                    "assets/5279114_linkedin_network_social network_linkedin logo_icon.png",
                    "assets/11244080_x_twitter_elon musk_twitter new logo_icon.png"] 
    
    for icon in social_icons:
        img = Image.open(icon)
        img = img.resize((15, 15), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        icon_label = tk.Label(social_frame, image=photo, bg="#007bff", width=15, height=15) 
        icon_label.pack(side="left", padx=3)
        images_reference.append(photo)
        
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
def draw_chart_in_frame(master_frame, criteria, line_data):

    for widget in master_frame.winfo_children():
        widget.destroy()

    ttk.Label(master_frame, text="Chỉ số Tiêu chí Tuyển sinh", 
              font=("Arial", 14, "bold"), background=master_frame['bg']).pack(pady=(5, 5))

    fig_chart = plt.Figure(figsize=(10, 5), dpi=100)
    ax_chart = fig_chart.add_subplot(111)

    x_pos = list(range(len(criteria)))

    plots = []
    
    data_points = []
    
    for i, school in enumerate(line_data):
        values = [school[c] for c in criteria]
        line, = ax_chart.plot(x_pos, values, marker="o", label=school["name"])
        plots.append(line)

        for j, val in enumerate(values):
            data_points.append({
                'x': x_pos[j],
                'y': val,
                'school': school['name'],
                'criterion': criteria[j]
            })

    ax_chart.set_xticks(x_pos) 
    ax_chart.set_xticklabels(criteria, rotation=15, ha="right")
    ax_chart.legend()

    canvas = FigureCanvasTkAgg(fig_chart, master=master_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    annot = ax_chart.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                              bbox=dict(boxstyle="round", fc="w", alpha=0.7),
                              arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    
    def update_annot(point):
        annot_text = f"Trường: {point['school']}\n{point['criterion']}: {point['y']}"
        annot.xy = (point['x'], point['y'])
        annot.set_text(annot_text)
        annot.get_bbox_patch().set_facecolor('#ffffcc')
        annot.get_bbox_patch().set_alpha(0.7)

    def hover(event):
        if event.inaxes == ax_chart:
            closest_point = None
            min_dist = float('inf')
            
            tolerance_px = 5 
            
            display_x, display_y = ax_chart.transData.transform((event.xdata, event.ydata))

            for point in data_points:
                point_display_x, point_display_y = ax_chart.transData.transform((point['x'], point['y']))
                
                dist_sq = (display_x - point_display_x)**2 + (display_y - point_display_y)**2
                
                if dist_sq < min_dist and dist_sq <= tolerance_px**2:
                    min_dist = dist_sq
                    closest_point = point

            if closest_point:
                update_annot(closest_point)
                annot.set_visible(True)
                fig_chart.canvas.draw_idle()
            else:
                if annot.get_visible():
                    annot.set_visible(False)
                    fig_chart.canvas.draw_idle()

    canvas.mpl_connect("motion_notify_event", hover)

if __name__ == "__main__":
    create_ui()
