import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from db import get_connection
def create_university_form(window):
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

    root = tk.Toplevel(window)
    root.title("Create University Data")
    root.geometry("700x700")
    def only_int(P):
        return P.isdigit() or P == ""
    vcmd = root.register(only_int)

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
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
            messagebox.showerror("Thiếu tên trường","Xin hãy nhập tên trường!")
            return
        if not basic_entries['region'].get():
            messagebox.showerror("Thiếu tên khu vực","Xin hãy chọn khu vực!")
            return
        if not basic_entries['country'].get():
            messagebox.showerror("Thiếu tên quốc gia","Xin hãy chọn quốc gia!")
            return
        if not basic_entries['rank'].get():
            messagebox.showerror("Thiếu thứ hạng","Xin hãy nhập thứ hạng!")
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

        print("\n✅ GENERATED DATA:\n")
        print(data)

    tk.Button(frame,bg= "#0013e9", fg='white' ,text="GENERATE DATA", command=generate_data).pack(pady=15)

    root.mainloop()

window = tk.Tk()
create_university_form(window)

window.mainloop()