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

    def create_new_university(data):
        import mysql.connector
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
        cursor = conn.cursor()
        cursor.execute("use universities_db_clone")
        
    

structure_sample_data = {
    "id": None, #int
    "name": None, #varchar
    "region": None, #varchar
    "country_id": None, #int
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
        'internaltional': None, #int
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