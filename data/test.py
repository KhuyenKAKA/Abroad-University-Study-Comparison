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
from controller.UniversityController import UniversityController

window = tk.Tk()
def update_university_form(university_id):
    mydb = get_connection()
    cursor = mydb.cursor()

    def get_university_data(university_id):
        conn = get_connection()
        cursor = conn.cursor()
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
            
        conn.close()

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
        UniversityController.update_university(data, university_id)
        messagebox.showinfo("Thanh cong","Cap nhat thong tin truong hoc thanh cong!")

    # print(get_university_data(1521))
    tk.Button(frame,bg= "#0013e9", fg='white' ,text="GENERATE DATA", command=generate_data).pack(pady=15)
    root.mainloop()

update_university_form(1521)
window.mainloop()

# def get_university_data(university_id):
#         conn = get_connection()
#         cursor = conn.cursor()
#         # ========= BASIC =========
#         cursor.execute("""
#             SELECT u.name, u.region, c.name, u.city, u.logo, u.overall_score, u.rank_int, u.path
#             FROM universities u
#             JOIN countries c ON u.country_id = c.id
#             WHERE u.id = %s
#         """, (university_id,))
#         basic_fields = ["title", "region", "country", "city", "logo", "overall_score", "rank", "path"]
#         basic_entries = {}
#         basic = cursor.fetchone()
#         for i, data  in enumerate(basic):
#             basic_entries[basic_fields[i]] = data

#         # ========= DETAIL =========
#         cursor.execute("""
#             SELECT * FROM detail_infors
#             WHERE university_id = %s
#         """, (university_id,))
#         detail = cursor.fetchone()
#         detail_keys = [
#                 'id','uid','fee', 'scholarship', 'domestic', 'international',
#                 'english_test', 'academic_test', 'total_stu',
#                 'ug_rate', 'pg_rate', 'inter_total',
#                 'inter_ug_rate', 'inter_pg_rate'
#             ]
#         detail_entries = {}
#         for i, data  in enumerate(detail):
#             detail_entries[detail_keys[i]] = data


#         # ========= SCORES =========
#         cursor.execute("""
#             SELECT 
#                 st.name as category,
#                 i.id as indicator_id,
#                 i.name as indicator_name,
#                 s.rank_int,
#                 s.score
#             FROM scores s
#             JOIN indicators i ON s.indicator_id = i.id
#             JOIN score_types st ON s.score_type_id = st.id
#             WHERE s.university_id = %s
#         """, (university_id,))
#         scores = {}
#         for cat_name, inid, inname, inrank, inscore in cursor.fetchall(): 
#             if cat_name not in scores:
#                 scores[cat_name] = []
#                 scores[cat_name].append(
#                     {
#                     "indicator_id": inid,
#                     "indicator_name": inname,
#                     "rank": inrank,#entry
#                     "score": inscore#entry
#                 })
#             else:
#                 scores[cat_name].append(
#                     {
#                     "indicator_id": inid,
#                     "indicator_name": inname,
#                     "rank": inrank,#entry
#                     "score": inscore#entry
#                 })

#         # ========= ENTRY =========
#         cursor.execute("""
#             SELECT *
#             FROM entry_infor
#             WHERE university_id = %s
#         """, (university_id,))
#         entry = cursor.fetchall()
#         entry_details = {
#             'bachelor':{
#                 "exists": False,#entry -> checkbox
#                 "SAT": None,#entry
#                 "GRE": None,#entry
#                 "GMAT": None,#entry
#                 "ACT": None,#entry
#                 "ATAR" :None,#entry
#                 "GPA":None,#entry
#                 "TOEFL": None,#entry
#                 "IELTS": None#entry
#             },
#             'master':{
#                 "exists": False,#entry -> checkbox
#                 "SAT": None,#entry
#                 "GRE": None,#entry
#                 "GMAT": None,#entry
#                 "ACT": None,#entry
#                 "ATAR" :None,#entry
#                 "GPA":None,#entry
#                 "TOEFL": None,#entry
#                 "IELTS": None#entry
#             }
#         }
#         for id, university_id, degree_type, sat, gre, gmat, act, atar, gpa, toefl, ielts in entry:
#             if int(degree_type) == 1:
#                 entry_details['bachelor'] ={
#                     "exists": True,#entry -> checkbox
#                     "SAT": sat,#entry
#                     "GRE": gre,#entry
#                     "GMAT": gmat,#entry
#                     "ACT": act,#entry
#                     "ATAR" :atar,#entry
#                     "GPA":gpa,#entry
#                     "TOEFL": toefl,#entry
#                     "IELTS": ielts#entry
#                 }
#             if int(degree_type) == 2:
#                 entry_details['master'] ={
#                     "exists": True,#entry -> checkbox
#                     "SAT": sat,#entry
#                     "GRE": gre,#entry
#                     "GMAT": gmat,#entry
#                     "ACT": act,#entry
#                     "ATAR" :atar,#entry
#                     "GPA":gpa,#entry
#                     "TOEFL": toefl,#entry
#                     "IELTS": ielts#entry
#                 }
            
#         conn.close()

#         return {
#             "basic": basic_entries,
#             "detail": detail_entries,
#             "scores": scores,
#             "entry": entry_details
#         }

# print(json.dumps(get_university_data(1), indent=4))

{'basic': (1, 'Massachusetts Institute of Technology (MIT)', 'North America', 1, 'Cambridge', 'https://www.topuniversities.com/sites/default/files/massachusetts-institute-of-technology-mit_410_medium.jpg', 100.0, 1, '/universities/massachusetts-institute-technology-mit', 'United States'), 'detail': (1, 1, None, 0, 67.0, 33.0, 'Generate Result', 'Generate Result', 11720, 39.0, 61.0, 3824, 17.0, 83.0), 'scores': [('Research & Discovery', 'Citations per Faculty', 73, 7, 100.0), ('Research & Discovery', 'Academic Reputation', 76, 4, 100.0), ('Learning Experience', 'Faculty Student Ratio', 36, 16, 100.0), ('Employability', 'Employer Reputation', 77, 2, 100.0), ('Employability', 'Employment Outcomes', 3819456, 7, 100.0), ('Global Engagement', 'International Student Ratio', 14, 153, 91.6), ('Global Engagement', 'International Research Network', 15, 98, 94.1), ('Global Engagement', 'International Faculty Ratio', 18, 63, 100.0), ('Global Engagement', 'International Student Diversity', 3924415, 130, 92.3), ('Sustainability', 'Sustainability Score', 3897497, 33, 93.8)], 'entry': [(1, 1, 1, '1520+', None, None, None, None, None, '100+', None), (2, 1, 2, None, None, '728+', None, None, None, '90+', '7+')]}