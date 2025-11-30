import mysql.connector
from db import get_connection
class UniversityModel:
    # done
    def get_all_university():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("use universities_db")
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
    # done
    def get_universities_with_name(name:str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("use universities_db")
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

    # done
    # cau truc filter: { 'region': '', 'country': '', 'ranking': (int(),int()) }
    def get_universities_with_condition(filter):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        # universities, country, 
        where_condition = ""
        if filter['region'] is not None:
            where_condition += f"u.region like '{filter['region']}'"
        if filter['country'] is not None:
            if where_condition != "":
                where_condition += f" and c.name like '{filter['country']}'"
            else:
                where_condition += f" c.name like '{filter['country']}'"
        if filter['ranking'] is not None:
            if where_condition != "":
                where_condition += f" and u.rank_int >= {filter['ranking'][0]} and u.rank_int <= {filter['ranking'][1]}"
            else:
                where_condition += f" u.rank_int >= {filter['ranking'][0]} and u.rank_int <= {filter['ranking'][1]}"
        if where_condition != "":
            where_condition = 'where '+where_condition

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

    # not working yet
    def add_university(data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("use universities_db")
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
            INSERT INTO universities (name, region, country_id, city, logo, overall_score, rank_int, path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("title"),
            data.get("region"),
            country_id,
            data.get("city"),
            data.get("logo"),
            data.get("overall_score"),
            data.get('rank'),
            data.get('path')
        ))
        conn.commit()
        university_id = cursor.lastrowid

        # 3️⃣ Thêm detail_infors
        d = data.get("detail_infors", {})
        cursor.execute("""
            INSERT INTO detail_infors (university_id, fee, scholarship, domestic, international, english_test, academic_test, total_stu, ug_rate, pg_rate, inter_total, inter_ug_rate, inter_pg_rate)
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
        for st_name, indicators in data.get("scores", {}).items():
            # score_type
            cursor.execute("INSERT IGNORE INTO score_types (name) VALUES (%s)", (st_name,))
            conn.commit()
            cursor.execute("SELECT id FROM score_types WHERE name=%s", (st_name,))
            st_id = cursor.fetchone()[0]
            score_type_map[st_name] = st_id

            for sc in indicators:
                indicator_id = sc["indicator_id"]
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
                    score_type_map[st_name],
                    rank_val,
                    float(sc["score"]) if sc["score"] and str(sc["score"]).replace('.', '', 1).isdigit() else None,
                    university_id
                ))
        conn.commit()

        if data['entry_infor']['bachelor']['exists']:
            cursor.execute("""
            INSERT INTO entry_infor (
                university_id, degree_type, SAT, GRE, GMAT, ACT, ATAR, GPA, TOEFL, IELTS
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            university_id,
            1,
            data['entry_infor']['bachelor']["SAT"],
            data['entry_infor']['bachelor']["GRE"],
            data['entry_infor']['bachelor']["GMAT"],
            data['entry_infor']['bachelor']["ACT"],
            data['entry_infor']['bachelor']["ATAR"],
            data['entry_infor']['bachelor']["GPA"],
            data['entry_infor']['bachelor']["TOEFL"],
            data['entry_infor']['bachelor']["IELTS"]
        ))
            
        if data['entry_infor']['master']['exists']:
            cursor.execute("""
            INSERT INTO entry_infor (
                university_id, degree_type, SAT, GRE, GMAT, ACT, ATAR, GPA, TOEFL, IELTS
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            university_id,
            2,
            data['entry_infor']['master']["SAT"],
            data['entry_infor']['master']["GRE"],
            data['entry_infor']['master']["GMAT"],
            data['entry_infor']['master']["ACT"],
            data['entry_infor']['master']["ATAR"],
            data['entry_infor']['master']["GPA"],
            data['entry_infor']['master']["TOEFL"],
            data['entry_infor']['master']["IELTS"]
        ))
        conn.commit()
        return university_id

    # not working yet
    def update_university(data, uni_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("use universities_db")
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
            UPDATE universities
            SET name = %s,
                region = %s,
                country_id = %s,
                city = %s,
                logo = %s,
                overall_score = %s,
                rank_int = %s,
                path = %s
            WHERE id = %s
        """, (
            data.get("title"),
            data.get("region"),
            country_id,
            data.get("city"),
            data.get("logo"),
            data.get("overall_score"),
            data.get('rank'),
            data.get('path'),
            uni_id
        ))
        conn.commit()
        university_id = uni_id

        cursor.execute(
            "DELETE FROM detail_infors WHERE university_id=%s",
            (university_id,)
        )
        # 3️⃣ Thêm detail_infors
        d = data.get("detail_infors", {})
        cursor.execute("""
            INSERT INTO detail_infors (university_id, fee, scholarship, domestic, international, english_test, academic_test, total_stu, ug_rate, pg_rate, inter_total, inter_ug_rate, inter_pg_rate)
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

        cursor.execute(
            "DELETE FROM scores WHERE university_id=%s",
            (university_id,)
        )

        # 4️⃣ Thêm scores
        score_type_map = {}
        indicator_map = {}
        for st_name, indicators in data.get("scores", {}).items():
            # score_type
            cursor.execute("INSERT IGNORE INTO score_types (name) VALUES (%s)", (st_name,))
            conn.commit()
            cursor.execute("SELECT id FROM score_types WHERE name=%s", (st_name,))
            st_id = cursor.fetchone()[0]
            score_type_map[st_name] = st_id

            for sc in indicators:
                indicator_id = sc["indicator_id"]
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
                    score_type_map[st_name],
                    rank_val,
                    float(sc["score"]) if sc["score"] and str(sc["score"]).replace('.', '', 1).isdigit() else None,
                    university_id
                ))
        conn.commit()

        cursor.execute(
            "DELETE FROM entry_infor WHERE university_id=%s",
            (university_id,)
        )
        if data['entry_infor']['bachelor']['exists']:
            cursor.execute("""
            INSERT INTO entry_infor (
                university_id, degree_type, SAT, GRE, GMAT, ACT, ATAR, GPA, TOEFL, IELTS
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            university_id,
            1,
            data['entry_infor']['bachelor']["SAT"],
            data['entry_infor']['bachelor']["GRE"],
            data['entry_infor']['bachelor']["GMAT"],
            data['entry_infor']['bachelor']["ACT"],
            data['entry_infor']['bachelor']["ATAR"],
            data['entry_infor']['bachelor']["GPA"],
            data['entry_infor']['bachelor']["TOEFL"],
            data['entry_infor']['bachelor']["IELTS"]
        ))
            
        if data['entry_infor']['master']['exists']:
            cursor.execute("""
            INSERT INTO entry_infor (
                university_id, degree_type, SAT, GRE, GMAT, ACT, ATAR, GPA, TOEFL, IELTS
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            university_id,
            2,
            data['entry_infor']['master']["SAT"],
            data['entry_infor']['master']["GRE"],
            data['entry_infor']['master']["GMAT"],
            data['entry_infor']['master']["ACT"],
            data['entry_infor']['master']["ATAR"],
            data['entry_infor']['master']["GPA"],
            data['entry_infor']['master']["TOEFL"],
            data['entry_infor']['master']["IELTS"]
        ))
        conn.commit()
        return university_id

    # done
    def delete_university(uni_id):
        """
        Xóa 1 trường và tất cả dữ liệu liên quan (scores, detail_infors)
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("use universities_db")
        # xóa scores
        cursor.execute("DELETE FROM scores WHERE university_id=%s", (uni_id,))
        # xóa detail_infors
        cursor.execute("DELETE FROM detail_infors WHERE university_id=%s", (uni_id,))
        # xóa university_texts nếu có
        cursor.execute("DELETE FROM university_texts WHERE university_id=%s", (uni_id,))
        cursor.execute("DELETE FROM entry_infor WHERE university_id=%s", (uni_id,))
        # xóa universities
        cursor.execute("DELETE FROM universities WHERE id=%s", (uni_id,))
        conn.commit()

    
sample_data = {
        "title": "Ghost University",
        "path": "/universities/massachusetts-institute-technology-mit",
        "region": "North America",
        "country": "United States",
        "city": "Cambridge",
        "logo": "https://duocphamtim.vn/wp-content/uploads/2022/12/rau-ma-scaled.jpeg",
        "overall_score": 0,
        "rank_display": "1",
        "rank": "1518",
        "more_info": [
            {
                "label": "International Fees",
                "value": ""
            },
            {
                "label": "Scholarship",
                "value": "No"
            },
            {
                "label": "Student Mix",
                "value": "Domestic 67%   International 33%"
            },
            {
                "label": "English Tests",
                "value": "Generate Result"
            },
            {
                "label": "Academic Tests",
                "value": "Generate Result"
            }
        ],
        "scores": {
            "Research & Discovery": [
                {
                    "indicator_id": "73",
                    "indicator_name": "Citations per Faculty",
                    "rank": "7",
                    "score": "100"
                },
                {
                    "indicator_id": "76",
                    "indicator_name": "Academic Reputation",
                    "rank": "4",
                    "score": "100"
                }
            ],
            "Learning Experience": [
                {
                    "indicator_id": "36",
                    "indicator_name": "Faculty Student Ratio",
                    "rank": "16",
                    "score": "100"
                }
            ],
            "Employability": [
                {
                    "indicator_id": "77",
                    "indicator_name": "Employer Reputation",
                    "rank": "2",
                    "score": "100"
                },
                {
                    "indicator_id": "3819456",
                    "indicator_name": "Employment Outcomes",
                    "rank": "7",
                    "score": "100"
                }
            ],
            "Global Engagement": [
                {
                    "indicator_id": "14",
                    "indicator_name": "International Student Ratio",
                    "rank": "153",
                    "score": "91.6"
                },
                {
                    "indicator_id": "15",
                    "indicator_name": "International Research Network",
                    "rank": "98",
                    "score": "94.1"
                },
                {
                    "indicator_id": "18",
                    "indicator_name": "International Faculty Ratio",
                    "rank": "63",
                    "score": "100"
                },
                {
                    "indicator_id": "3924415",
                    "indicator_name": "International Student Diversity",
                    "rank": "130",
                    "score": "92.3"
                }
            ],
            "Sustainability": [
                {
                    "indicator_id": "3897497",
                    "indicator_name": "Sustainability Score",
                    "rank": "33",
                    "score": "93.8"
                }
            ]
        },
        'detail_infors': {
            'fee': None, #double
            'scholarship': None, #bool
            'domestic': None, #float
            'international': None, #float
            'english_test': None, #string
            'academic_test': None, #string
            'total_stu': None, #int
            'ug_rate': None, # float
            'pg_rate': None, # float
            'inter_total': None, #int
            'inter_ug_rate': None, #float
            'inter_pg_rate': None #float
        },
        'entry_infor': {
            'bachelor':{
                "exists": True,
                "SAT": None,
                "GRE": None,
                "GMAT": None,
                "ACT": None,
                "ATAR" :None,
                "GPA":None,
                "TOEFL": None,
                "IELTS": None
            },
            'master':{
                "exists": True,
                "SAT": None,
                "GRE": None,
                "GMAT": None,
                "ACT": None,
                "ATAR" :None,
                "GPA":None,
                "TOEFL": None,
                "IELTS": None
            },
        }
    }


# print(UniversityModel.get_universities_with_condition(conditions)[0])

# UniversityModel.add_university(sample_data)
# UniversityModel.update_university(sample_data,1514)
