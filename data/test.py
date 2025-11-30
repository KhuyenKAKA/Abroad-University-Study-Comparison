import tkinter as tk
from tkinter import ttk
import json

def create_university_form():

    root = tk.Tk()
    root.title("Create University Data")
    root.geometry("900x700")

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
    ttk.Label(frame, text="BASIC INFORMATION", font=("Segoe UI", 14, "bold")).pack(pady=5)

    basic_fields = ["title", "path", "region", "country", "city", "logo", "overall_score", "rank"]
    basic_entries = {}

    box = ttk.LabelFrame(frame, text="Basic Info")
    box.pack(padx=10, pady=5, fill="x")

    for i, field in enumerate(basic_fields):
        ttk.Label(box, text=field).grid(row=i, column=0, sticky="w", padx=5, pady=3)
        e = ttk.Entry(box, width=50)
        e.grid(row=i, column=1, padx=5, pady=3)
        basic_entries[field] = e

    # ========== MORE INFO ==========
    ttk.Label(frame, text="MORE INFO", font=("Segoe UI", 14, "bold")).pack(pady=5)

    more_info_labels = [
        "International Fees",
        "Scholarship",
        "Student Mix",
        "English Tests",
        "Academic Tests"
    ]

    more_entries = {}
    more_frame = ttk.LabelFrame(frame, text="More Info")
    more_frame.pack(padx=10, pady=5, fill="x")

    for i, label in enumerate(more_info_labels):
        ttk.Label(more_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        e = ttk.Entry(more_frame, width=60)
        e.grid(row=i, column=1, padx=5)
        more_entries[label] = e

    # ========== SCORES ==========
    ttk.Label(frame, text="SCORES", font=("Segoe UI", 14, "bold")).pack(pady=5)

    categories = {
        "Research & Discovery": ["Citations per Faculty", "Academic Reputation"],
        "Learning Experience": ["Faculty Student Ratio"],
        "Employability": ["Employer Reputation", "Employment Outcomes"],
        "Global Engagement": [
            "International Student Ratio",
            "International Research Network",
            "International Faculty Ratio",
            "International Student Diversity"
        ],
        "Sustainability": ["Sustainability Score"]
    }

    score_entries = {}

    for cat, indicators in categories.items():
        cf = ttk.LabelFrame(frame, text=cat)
        cf.pack(padx=10, pady=4, fill="x")

        score_entries[cat] = []

        for i, name in enumerate(indicators):
            ttk.Label(cf, text=name).grid(row=i, column=0, sticky="w")

            r = ttk.Entry(cf, width=8)
            r.grid(row=i, column=1, padx=2)
            r.insert(0, "")

            s = ttk.Entry(cf, width=8)
            s.grid(row=i, column=2, padx=2)
            s.insert(0, "")

            score_entries[cat].append((name, r, s))

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
            e = ttk.Entry(lf, width=25)
            e.grid(row=i, column=1)
            entry_data[level]["entries"][f] = e

    # ========== GENERATE DATA ==========
    def generate_data():

        data = {}

        for k, e in basic_entries.items():
            data[k] = e.get()

        # rank_display tự tạo
        data["rank_display"] = data.get("rank", "")

        # more_info
        data["more_info"] = []
        for key, entry in more_entries.items():
            data["more_info"].append({
                "label": key,
                "value": entry.get()
            })

        # scores
        data["scores"] = {}
        for cat, indicators in score_entries.items():
            data["scores"][cat] = []
            for name, r, s in indicators:
                data["scores"][cat].append({
                    "indicator_id": "",
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
        print(json.dumps(data, indent=4))

    ttk.Button(frame, text="GENERATE DATA", command=generate_data).pack(pady=15)

    root.mainloop()


create_university_form()
