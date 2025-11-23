import tkinter as tk
from tkinter import ttk


def reset_filters():
    # Đặt lại các trường nhập liệu text
    region_entry.delete(0, tk.END)
    country_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    
    # Đặt lại Radiobutton về None (bỏ chọn)
    study_level_var.set(None)
    top_ranking_var.set(None)

    
    print("Bộ lọc đã được đặt lại.")

def apply_filters():

    region = region_entry.get()
    country = country_entry.get()
    city = city_entry.get()
    study_level_code = study_level_var.get() 
    top_ranking_code = top_ranking_var.get()        

    print("--- Áp dụng bộ lọc ---")
    print(f"Region: {region}")
    print(f"Country: {country}")
    print(f"City: {city}")
    print(f"Study Level Code (1=Cử nhân, 2=Master): {study_level_code}")
    print(f"Top Ranking Code (1-4): {top_ranking_code}")
    print("------------------------")

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Filter Interface (Cập nhật Entry bằng Code)")
root.geometry("400x700")
root.resizable(False, False)
study_level_var = tk.IntVar(value=1)  # hoặc tk.IntVar() nếu muốn bắt đầu không chọn
top_ranking_var = tk.IntVar(value=1)
# Đặt font và style cơ bản
font_label = ("Arial", 10, "bold")
font_button = ("Arial", 10)
entry_width = 40
radio_font = ("Arial", 10)

# --- Study Level Variables ---
study_level_var = tk.StringVar(value=None)
study_level_var.set(None)

# --- Top Ranking Variables ---
top_ranking_var = tk.StringVar(value=None)
top_ranking_var.set(None)

# --- Khung chứa chính (Main Frame) ---
main_frame = ttk.Frame(root, padding="20 10 20 10")
main_frame.pack(fill='both', expand=True)

# --- 1. Region ---
tk.Label(main_frame, text="Vùng", font=font_label, anchor='w').pack(fill='x', pady=(0, 5))
region_entry = tk.Entry(main_frame, width=entry_width, relief='solid', borderwidth=1)
region_entry.pack(fill='x', ipady=5, pady=(0, 10))

# --- 2. Country ---
tk.Label(main_frame, text="Quốc gia", font=font_label, anchor='w').pack(fill='x', pady=(0, 5))
country_entry = tk.Entry(main_frame, width=entry_width, relief='solid', borderwidth=1)
country_entry.pack(fill='x', ipady=5, pady=(0, 10))

# --- 3. City ---
tk.Label(main_frame, text="Thành phố", font=font_label, anchor='w').pack(fill='x', pady=(0, 5))
city_entry = tk.Entry(main_frame, width=entry_width, relief='solid', borderwidth=1)
city_entry.pack(fill='x', ipady=5, pady=(0, 15))

# --- 4. Study Level (Radiobuttons) ---
tk.Label(main_frame, text="Chương trình đào tạo", font=font_label, anchor='w').pack(fill='x', pady=(0, 5))
study_level_frame = ttk.Frame(main_frame)
study_level_frame.pack(fill='x', pady=(0, 10), anchor='w')

# --- Radio Buttons Cử nhân và Master ---
tk.Radiobutton(study_level_frame, text="Cử nhân ", variable=study_level_var, value=1, font=radio_font 
              ).pack(side='left', padx=5, pady=5)
tk.Radiobutton(study_level_frame, text="Thạc sĩ", variable=study_level_var, value=2, font=radio_font).pack(side='left', padx=5, pady=5)




# --- 5. Top Ranking (Radiobuttons) ---
tk.Label(main_frame, text="Xếp hạng", font=font_label, anchor='w').pack(fill='x', pady=(10, 5))
ranking_frame = ttk.Frame(main_frame)
ranking_frame.pack(fill='x', pady=(0, 10), anchor='w')

ranking_options = [
    ("Top 100", 1),
    ("101 - 300", 2),
    ("301 - 500", 3),
    ("501 - 1,500", 4)
]

# Vòng lặp tạo Radiobutton cho Top Ranking
for i, (text, value) in enumerate(ranking_options):


    
    rb = tk.Radiobutton(ranking_frame, text=text, variable=top_ranking_var, value=ranking_options[i][1], font=radio_font)
    
    # Bố cục 2 cột
    row = i // 2
    col = i % 2
    rb.grid(row=row, column=col, sticky='w', padx=5, pady=3)



# --- 6. Buttons (Reset & Apply) ---
button_frame = ttk.Frame(main_frame, padding="0 10 0 0")
button_frame.pack(fill='x')

style = ttk.Style()
style.configure('Reset.TButton', background='white', foreground='#007BFF', font=font_button, borderwidth=1, relief='flat')
style.map('Reset.TButton', background=[('active', '#e1e1e1')])

# Nút Reset Filters
reset_button = ttk.Button(button_frame, text="Làm mới", command=reset_filters, style='Reset.TButton')
reset_button.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=10)

# Nút Apply Filters (nền xanh, chữ trắng)
apply_button = tk.Button(button_frame, text="Áp dụng", command=apply_filters, bg='#007BFF', fg='white', font=font_button, relief='flat')
apply_button.pack(side='right', fill='x', expand=True, ipady=10)

# Chạy vòng lặp sự kiện chính
root.mainloop()