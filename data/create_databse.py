import mysql.connector
import json

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="user",       
    password="Tung@09092004"  
)
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS universities_db;")
cursor.execute("CREATE DATABASE IF NOT EXISTS universities_db")
cursor.execute("USE universities_db;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS universities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    region ENUM('Asia','Europe','North America','Latin America','Oceania','Africa'),
    country_id INT,
    city VARCHAR(255),
    logo VARCHAR(500),
    overall_score FLOAT,
    rank_int INT,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS detail_infors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT,
    fee DOUBLE,
    scholarship BOOLEAN,
    domestic FLOAT,
    international FLOAT,
    english_test VARCHAR(255),
    academic_test VARCHAR(255),
    FOREIGN KEY (university_id) REFERENCES universities(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS indicators (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS score_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indicator_id INT,
    score_type_id INT,
    rank_int INT,
    score FLOAT,
    university_id INT,
    FOREIGN KEY (indicator_id) REFERENCES indicators(id),
    FOREIGN KEY (score_type_id) REFERENCES score_types(id),
    FOREIGN KEY (university_id) REFERENCES universities(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    password VARCHAR(255),
    image VARCHAR(255),
    phone_number VARCHAR(50),
    gender BOOLEAN,
    dob DATE,
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
""")

conn.commit()

with open("E:\\Tunz\\Python\\BTL\\raw_data_visualize.json",'r') as f:
    data = json.load(f)

country_map = {}
indicator_map = {}
score_type_map = {}

for uni in data:
    country_name = uni.get("country", "").strip()
    if country_name and country_name not in country_map:
        cursor.execute("INSERT IGNORE INTO countries (name) VALUES (%s)", (country_name,))
        conn.commit()
        cursor.execute("SELECT id FROM countries WHERE name = %s", (country_name,))
        country_map[country_name] = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO universities (name, region, country_id, city, logo, overall_score, rank_int)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        uni.get("title"),
        uni.get("region"),
        country_map.get(country_name),
        uni.get("city"),
        uni.get("logo"),
        float(uni.get("overall_score")) if uni.get("overall_score") and uni.get("overall_score").replace('.', '', 1).isdigit() else None,
        int(uni.get("rank")) if uni.get("rank") else None
    ))
    conn.commit()
    university_id = cursor.lastrowid

    fee, scholarship, domestic, international, english, academic = (None, False, None, None, None, None)
    for item in uni.get("more_info", []):
        label, value = item.get("label"), item.get("value", "")
        if "Fees" in label:
            fee = ''.join([c for c in value if c.isdigit() or c == '.'])
            fee = float(fee) if fee else None
        elif "Scholarship" in label:
            scholarship = (value.lower() == "yes")
        elif "Student Mix" in label:
            try:
                parts = value.replace("%", "").split()
                domestic = float(parts[1])
                international = float(parts[3])
            except:
                pass
        elif "English" in label:
            english = value
        elif "Academic" in label:
            academic = value

    cursor.execute("""
        INSERT INTO detail_infors (university_id, fee, scholarship, domestic, international, english_test, academic_test)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (university_id, fee, scholarship, domestic, international, english, academic))
    conn.commit()

    for score_type, indicators in uni.get("scores", {}).items():
        if score_type not in score_type_map:
            cursor.execute("INSERT IGNORE INTO score_types (name) VALUES (%s)", (score_type,))
            conn.commit()
            cursor.execute("SELECT id FROM score_types WHERE name = %s", (score_type,))
            score_type_map[score_type] = cursor.fetchone()[0]

        for sc in indicators:
            indicator_id = int(sc["indicator_id"])
            if indicator_id not in indicator_map:
                cursor.execute("INSERT IGNORE INTO indicators (id, name) VALUES (%s, %s)", (indicator_id, sc["indicator_name"]))
                conn.commit()
                indicator_map[indicator_id] = indicator_id

            rank_val = ''.join([c for c in sc["rank"] if c.isdigit()])
            rank_val = int(rank_val) if rank_val else None

            cursor.execute("""
                INSERT INTO scores (indicator_id, score_type_id, rank_int, score, university_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                indicator_id,
                score_type_map[score_type],
                rank_val,
                float(sc["score"]) if sc["score"] and sc["score"].replace('.', '', 1).isdigit() else None,
                university_id
            ))
    conn.commit()

print("✅ Dữ liệu đã được nhập thành công vào MySQL!")

cursor.close()
conn.close()
# print(len(data))