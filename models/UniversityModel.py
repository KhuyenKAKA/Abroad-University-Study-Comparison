import mysql.connector

class UniversityModel:
    def get_all_university():
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        # universities, country, 
        querry = """
        SELECT 
            u.id,
            u.rank_int,
            u.overall_score,
            u.name AS university_name,
            u.city,
            c.name AS country_name,
            u.logo,
            st.name AS score_type,
            i.name AS indicator_name,
            s.score
        FROM universities u
        JOIN countries c  ON u.country_id = c.id
        JOIN scores s ON u.id = s.university_id
        JOIN score_types st ON s.score_type_id = st.id
        JOIN indicators i ON i.id = s.indicator_id
        """
        cursor.execute(querry)
        crawl_data = cursor.fetchall()
        crawl_data = sorted(crawl_data, key= lambda x:x[0])
        universities_data = []
        for i in range(int(len(crawl_data[0:500])/10)):
            data = {
                'id':None,
                'rank': None,
                'overall_score': None,
                'name': None,
                'city': None,
                'country': None,
                'logo': None,
                'score': {
                    "Research & Discovery":{
                        "Citations per Faculty":None,
                        "Academic Reputation":None
                    },
                    "Learning Experience":{
                        "Faculty Student Ratio":None
                    },
                    "Employability":{
                        "Employer Reputation": None,
                        "Employment Outcomes": None,
                    },
                    "Global Engagement":{
                        "International Student Ratio": None,
                        "International Research Network": None,
                        "International Faculty Ratio": None,
                        "International Student Diversity": None
                    },
                    "Sustainability":{
                        "Sustainability Score": None
                    }
                }
            }
            for x in crawl_data[i*10:i*10+10]:
                data['id'] = x[0]
                data['rank'] = x[1]
                if x[2] is not None:
                    data['overall_score'] = x[2]
                else:
                    data['overall_score'] = 0.0
                data['name'] = x[3]
                data['city'] = x[4]
                data['country'] = x[5]
                data['logo'] = x[6]
                data['score'][x[7]][x[8]] = x[9]
            universities_data.append(data)
        return universities_data
    
    def get_universities_with_name(name:str):
        import mysql.connector
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        # universities, country, 
        where_condition = ""
        if name.strip():
            where_condition = "where u.name like '%"
            for x in name:
                where_condition+= x+"%"
            where_condition+= "'"

        querry = f"""
        SELECT 
            u.id,
            u.rank_int,
            u.overall_score,
            u.name AS university_name,
            u.city,
            c.name AS country_name,
            u.logo,
            st.name AS score_type,
            i.name AS indicator_name,
            s.score
        FROM universities u
        JOIN countries c  ON u.country_id = c.id
        JOIN scores s ON u.id = s.university_id
        JOIN score_types st ON s.score_type_id = st.id
        JOIN indicators i ON i.id = s.indicator_id
        {where_condition}
        """
        cursor.execute(querry)
        crawl_data = cursor.fetchall()
        crawl_data = sorted(crawl_data, key= lambda x:x[0])
        uni_data = []
        end_data = min(len(crawl_data),500)
        for i in range(int(len(crawl_data[0:end_data])/10)):
            data = {
                'id':None,
                'rank': None,
                'overall_score': None,
                'name': None,
                'city': None,
                'country': None,
                'logo': None,
                'score': {
                    "Research & Discovery":{
                        "Citations per Faculty":None,
                        "Academic Reputation":None
                    },
                    "Learning Experience":{
                        "Faculty Student Ratio":None
                    },
                    "Employability":{
                        "Employer Reputation": None,
                        "Employment Outcomes": None,
                    },
                    "Global Engagement":{
                        "International Student Ratio": None,
                        "International Research Network": None,
                        "International Faculty Ratio": None,
                        "International Student Diversity": None
                    },
                    "Sustainability":{
                        "Sustainability Score": None
                    }
                }
            }
            for x in crawl_data[i*10:i*10+10]:
                data['id'] = x[0]
                data['rank'] = x[1]
                if x[2] is not None:
                    data['overall_score'] = x[2]
                else:
                    data['overall_score'] = 0.0
                data['name'] = x[3]
                data['city'] = x[4]
                data['country'] = x[5]
                data['logo'] = x[6]
                data['score'][x[7]][x[8]] = x[9]
            uni_data.append(data)
        return uni_data
    
    def add_university(data):
        """
        Thêm 1 trường đại học, score, detail_infors
        """
        import mysql.connector
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        # 1️⃣ Xử lý country
        country_name = data.get("country")
        if country_name:
            cursor.execute("INSERT IGNORE INTO countries (name) VALUES (%s)", (country_name,))
            conn.commit()
            cursor.execute("SELECT id FROM countries WHERE name=%s", (country_name,))
            country_id = cursor.fetchone()[0]
        else:
            country_id = None

        # 2️⃣ Thêm vào universities
        cursor.execute("""
            INSERT INTO universities (name, region, country_id, city, logo, overall_score)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get("name"),
            data.get("region"),
            country_id,
            data.get("city"),
            data.get("logo"),
            data.get("overall_score")
        ))
        conn.commit()
        university_id = cursor.lastrowid

        # 3️⃣ Thêm detail_infors
        d = data.get("detail_infors", {})
        cursor.execute("""
            INSERT INTO detail_infors (university_id, fee, scholarship, domestic, international, english_test, academic_test,
                                    total_stu, ug_rate, pg_rate, inter_total, inter_ug_rate, inter_pg_rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            university_id,
            d.get("fee"),
            d.get("scholarship"),
            d.get("domestic"),
            d.get("international"),
            d.get("english_test"),
            d.get("academic_test"),
            d.get("total_stu"),
            d.get("ug_rate"),
            d.get("pg_rate"),
            d.get("inter_total"),
            d.get("inter_ug_rate"),
            d.get("inter_pg_rate")
        ))
        conn.commit()

        # 4️⃣ Thêm scores
        score_type_map = {}
        indicator_map = {}
        for st_name, indicators in data.get("score", {}).items():
            # score_type
            cursor.execute("INSERT IGNORE INTO score_types (name) VALUES (%s)", (st_name,))
            conn.commit()
            cursor.execute("SELECT id FROM score_types WHERE name=%s", (st_name,))
            st_id = cursor.fetchone()[0]
            score_type_map[st_name] = st_id

            for ind_name, value in indicators.items():
                if value:
                    rank_val, score_val = value
                else:
                    rank_val, score_val = None, None

                # indicator
                cursor.execute("INSERT IGNORE INTO indicators (name) VALUES (%s)", (ind_name,))
                conn.commit()
                cursor.execute("SELECT id FROM indicators WHERE name=%s", (ind_name,))
                ind_id = cursor.fetchone()[0]
                indicator_map[ind_name] = ind_id

                # score
                cursor.execute("""
                    INSERT INTO scores (indicator_id, score_type_id, rank_int, score, university_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ind_id, st_id, rank_val, score_val, university_id))
        conn.commit()
        return university_id


    def update_university( data):
        """
        Cập nhật thông tin trường, detail_infors và scores theo data['id']
        """
        import mysql.connector
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        uni_id = data.get("id")
        if not uni_id:
            raise ValueError("data phải có id để update")

        # 1️⃣ Update country nếu có
        country_name = data.get("country")
        if country_name:
            cursor.execute("INSERT IGNORE INTO countries (name) VALUES (%s)", (country_name,))
            conn.commit()
            cursor.execute("SELECT id FROM countries WHERE name=%s", (country_name,))
            country_id = cursor.fetchone()[0]
        else:
            country_id = None

        # 2️⃣ Update universities
        cursor.execute("""
            UPDATE universities
            SET name=%s, region=%s, country_id=%s, city=%s, logo=%s, overall_score=%s
            WHERE id=%s
        """, (
            data.get("name"),
            data.get("region"),
            country_id,
            data.get("city"),
            data.get("logo"),
            data.get("overall_score"),
            uni_id
        ))
        conn.commit()

        # 3️⃣ Update detail_infors
        d = data.get("detail_infors", {})
        cursor.execute("""
            UPDATE detail_infors
            SET fee=%s, scholarship=%s, domestic=%s, international=%s, english_test=%s, academic_test=%s,
                total_stu=%s, ug_rate=%s, pg_rate=%s, inter_total=%s, inter_ug_rate=%s, inter_pg_rate=%s
            WHERE university_id=%s
        """, (
            d.get("fee"),
            d.get("scholarship"),
            d.get("domestic"),
            d.get("international"),
            d.get("english_test"),
            d.get("academic_test"),
            d.get("total_stu"),
            d.get("ug_rate"),
            d.get("pg_rate"),
            d.get("inter_total"),
            d.get("inter_ug_rate"),
            d.get("inter_pg_rate"),
            uni_id
        ))
        conn.commit()

        # 4️⃣ Update scores: xóa cũ rồi thêm mới
        cursor.execute("DELETE FROM scores WHERE university_id=%s", (uni_id,))
        conn.commit()
        score_type_map = {}
        indicator_map = {}
        for st_name, indicators in data.get("score", {}).items():
            # score_type
            cursor.execute("INSERT IGNORE INTO score_types (name) VALUES (%s)", (st_name,))
            conn.commit()
            cursor.execute("SELECT id FROM score_types WHERE name=%s", (st_name,))
            st_id = cursor.fetchone()[0]
            score_type_map[st_name] = st_id

            for ind_name, value in indicators.items():
                if value:
                    rank_val, score_val = value
                else:
                    rank_val, score_val = None, None

                # indicator
                cursor.execute("INSERT IGNORE INTO indicators (name) VALUES (%s)", (ind_name,))
                conn.commit()
                cursor.execute("SELECT id FROM indicators WHERE name=%s", (ind_name,))
                ind_id = cursor.fetchone()[0]

                # score
                cursor.execute("""
                    INSERT INTO scores (indicator_id, score_type_id, rank_int, score, university_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ind_id, st_id, rank_val, score_val, uni_id))
        conn.commit()


    def delete_university(uni_id):
        """
        Xóa 1 trường và tất cả dữ liệu liên quan (scores, detail_infors)
        """
        import mysql.connector
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        # xóa scores
        cursor.execute("DELETE FROM scores WHERE university_id=%s", (uni_id,))
        # xóa detail_infors
        cursor.execute("DELETE FROM detail_infors WHERE university_id=%s", (uni_id,))
        # xóa university_texts nếu có
        cursor.execute("DELETE FROM university_texts WHERE university_id=%s", (uni_id,))
        # xóa universities
        cursor.execute("DELETE FROM universities WHERE id=%s", (uni_id,))
        conn.commit()

    

structure_sample_data = {
    "id": None, #int
    "name": None, #varchar
    "region": None, #varchar
    "country": None, #varchar
    "city": None, #varchar
    "logo": None, #varchar
    "overall_score": None, #float
    'score': {
        "Research & Discovery":{
            "Citations per Faculty":None, #(rank_int, score) 
            "Academic Reputation":None #(rank_int, score)
        },
        "Learning Experience":{
            "Faculty Student Ratio":None #(rank_int, score)
        },
        "Employability":{
            "Employer Reputation": None, #(rank_int, score)
            "Employment Outcomes": None, #(rank_int, score)
        },
        "Global Engagement":{
            "International Student Ratio": None, #(rank_int, score)
            "International Research Network": None, #(rank_int, score)
            "International Faculty Ratio": None, #(rank_int, score)
            "International Student Diversity": None #(rank_int, score)
        },
        "Sustainability":{
            "Sustainability Score": None #(rank_int, score)
        }
    },
    "entry_degree_requirement": {
        "General": {
            "SAT": None,  #int
            "GRE": None,  #int
            "GMAT" : None, #int
            "ACT": None, #float
            "ATAR": None, #float
            "GPA": None, #float
            "TOEFL": None,  #int
            "IELTS": None #float
        },
        "Master": {
            "SAT": None,  #int
            "GRE": None,  #int
            "GMAT" : None, #int
            "ACT": None, #float
            "ATAR": None, #float
            "GPA": None, #float
            "TOEFL": None,  #int
            "IELTS": None #float
        }
    },
    "detail_infors": {
        'fee': None, #int
        'scholarship': None,  #int
        'domestic': None,  #int
        'international': None, #int
        'english_test': None, #varchar
        'academic_test': None, #varchar
        'total_stu': None, #int
        'ug_rate': None, #float
        'pg_rate': None, #float
        'inter_total': None, #int
        'inter_ug_rate': None, #float
        'inter_pg_rate': None #float
    }
}

sample_data = {
    "name": "Đại học EMI, Đại học Kông ngiệp",
    "region": "Asia", #varchar
    "country": "Địa linh", #varchar
    "city": "Đất vua", #varchar
    "logo": "https://duocphamtim.vn/wp-content/uploads/2022/12/rau-ma-scaled.jpeg", #varchar
    "overall_score": 36.36, #float
    'score': {
        "Research & Discovery":{
            "Citations per Faculty":(36, 36.36), #(rank_int, score) 
            "Academic Reputation":(36, 36.36) #(rank_int, score)
        },
        "Learning Experience":{
            "Faculty Student Ratio":(36, 36.36) #(rank_int, score)
        },
        "Employability":{
            "Employer Reputation": (36, 36.36), #(rank_int, score)
            "Employment Outcomes": (36, 36.36), #(rank_int, score)
        },
        "Global Engagement":{
            "International Student Ratio": (36, 36.36), #(rank_int, score)
            "International Research Network": (36, 36.36), #(rank_int, score)
            "International Faculty Ratio": (36, 36.36), #(rank_int, score)
            "International Student Diversity": (36, 36.36) #(rank_int, score)
        },
        "Sustainability":{
            "Sustainability Score": (36, 36.36) #(rank_int, score)
        }
    },
    "entry_degree_requirement": {
        "General": {
            "SAT": 36,  #int
            "GRE": 36,  #int
            "GMAT" : 36, #int
            "ACT": 36, #float
            "ATAR": 36, #float
            "GPA": 36, #float
            "TOEFL": 36,  #int
            "IELTS": 36 #float
        },
        "Master": {
            "SAT": 36,  #int
            "GRE": 36,  #int
            "GMAT" : 36, #int
            "ACT": 36, #float
            "ATAR": 36, #float
            "GPA": 36, #float
            "TOEFL": 36,  #int
            "IELTS": 36 #float
        }
    },
    "detail_infors": {
        'fee': 36, #int
        'scholarship': 36,  #int
        'domestic': 36,  #int
        'international': 36, #int
        'english_test': "36", #varchar
        'academic_test': "36", #varchar
        'total_stu': 36, #int
        'ug_rate': 36, #float
        'pg_rate': 36, #float
        'inter_total': 36, #int
        'inter_ug_rate': 36, #float
        'inter_pg_rate': 36 #float
    }
}

# UniversityModel.add_university(sample_data)
# UniversityModel.delete_university(1507)
