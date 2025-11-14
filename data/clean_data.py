import re
import mysql.connector
from enum import Enum

# ===================== ENUM LOẠI BẰNG =====================
class TypeDegree(Enum):
    Bachelor = 1
    Master = 2

# ===================== KẾT NỐI DATABASE =====================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="Tung@09092004",  
        database="universities_db"  
    )

def create_entry_infor_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS entry_infor")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entry_infor (
        id INT AUTO_INCREMENT PRIMARY KEY,
        university_id INT,
        degree_type INT,
        SAT VARCHAR(20),
        GRE VARCHAR(20),
        GMAT VARCHAR(20),
        ACT VARCHAR(20),
        ATAR VARCHAR(20),
        GPA VARCHAR(20),
        TOEFL VARCHAR(20),
        IELTS VARCHAR(20),
        FOREIGN KEY (university_id) REFERENCES universities(id)
    );
    """)
def clean_data(value:str):
    requirement = ["SAT","GRE","GMAT","ACT","ATAR","GPA","TOEFL","IELTS"]
    haveMaster = False
    haveBachelor = False
    Bachelor_requirement = {
        "SAT": None,
        "GRE": None,
        "GMAT": None,
        "ACT": None,
        "ATAR" :None,
        "GPA":None,
        "TOEFL": None,
        "IELTS": None
    }
    Master_requirement = {
        "SAT": None,
        "GRE": None,
        "GMAT": None,
        "ACT": None,
        "ATAR" :None,
        "GPA":None,
        "TOEFL": None,
        "IELTS": None
    }

    Master_infor = [x.strip() for x in value.split("Master") if "+" in x]
    if len(Master_infor)>1:
        
        Master_infor = Master_infor[1].strip().split()
        for data_index in range(len(Master_infor)-1):
            if Master_infor[data_index] in requirement and any(c.isdigit() for c in Master_infor[data_index+1]):
                haveMaster = True
                Master_requirement[Master_infor[data_index]] = Master_infor[data_index+1] 
    
    Bachelor_infor = value.split("Master")[0].strip()
    Bachelor_infor = [x.strip() for first_split in Bachelor_infor.split("Bachelor") for x in first_split.split("General") if "+" in x and "email" not in x]
    if Bachelor_infor:
        Bachelor_infor = Bachelor_infor[0]
        
        Bachelor_infor = Bachelor_infor.split()
        for data_index in range(len(Bachelor_infor)-1):
            if Bachelor_infor[data_index] in requirement and  any(c.isdigit() for c in Bachelor_infor[data_index+1]):
                haveBachelor = True
                Bachelor_requirement[Bachelor_infor[data_index]] = Bachelor_infor[data_index+1] 
    return haveBachelor, Bachelor_requirement, haveMaster, Master_requirement

# ===================== GHI DỮ LIỆU =====================
def process_entry_infor():
    conn = connect_db()
    cursor = conn.cursor()

    create_entry_infor_table(cursor)
    conn.commit()

    cursor.execute("SELECT id, university_information FROM university_texts")
    rows = cursor.fetchall()

    for uni_id, info_text in rows:
        if not info_text:
            continue

        haveBachelor, Bachelor_requirement, haveMaster, Master_requirement = clean_data(info_text)
        if haveBachelor:
            cursor.execute("""
            INSERT INTO entry_infor (
                university_id, degree_type, SAT, GRE, GMAT, ACT, ATAR, GPA, TOEFL, IELTS
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            uni_id,
            TypeDegree.Bachelor.value,
            Bachelor_requirement["SAT"],
            Bachelor_requirement["GRE"],
            Bachelor_requirement["GMAT"],
            Bachelor_requirement["ACT"],
            Bachelor_requirement["ATAR"],
            Bachelor_requirement["GPA"],
            Bachelor_requirement["TOEFL"],
            Bachelor_requirement["IELTS"]
        ))
            
        if haveMaster:
            cursor.execute("""
            INSERT INTO entry_infor (
                university_id, degree_type, SAT, GRE, GMAT, ACT, ATAR, GPA, TOEFL, IELTS
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            uni_id,
            TypeDegree.Master.value,
            Master_requirement["SAT"],
            Master_requirement["GRE"],
            Master_requirement["GMAT"],
            Master_requirement["ACT"],
            Master_requirement["ATAR"],
            Master_requirement["GPA"],
            Master_requirement["TOEFL"],
            Master_requirement["IELTS"]
        ))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Đã xử lý và lưu dữ liệu vào bảng entry_infor.")

# ===================== MAIN =====================
if __name__ == "__main__":
    process_entry_infor()
