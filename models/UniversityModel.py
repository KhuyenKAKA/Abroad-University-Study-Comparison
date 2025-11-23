import mysql.connector

class UniversityModel:
    def get_all_university():
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="user",       
            password="Tung@09092004"  
        )
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