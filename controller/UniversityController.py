import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from models.UniversityModel import UniversityModel
class UniversityController:
    def search_by_name(name):
        return UniversityModel.get_universities_with_name(name)
    
    def get_all_university():
        return UniversityModel.get_all_university()
    def get_all_university_by_condition(dict):
        return UniversityModel.get_universities_with_condition(dict)
    
    def delete_university(id):
        return UniversityModel.delete_university(id)
    
    def update_university(data, id):
        return UniversityModel.update_university(data, id)
    
    def add_university(data):
        return UniversityModel.add_university(data)
    
    
    def get_uni_detail(list_id):
        data = UniversityModel.get_uni_detail(list_id)
        return data
    def get_data_chart(list_id):
        data = UniversityModel.get_data_chart(list_id)
        chart_data = []
        keys = ["SAT", "GRE", "GMAT", "ACT", "ATAR", "GPA", "TOEFL", "IELTS"]

        if data:
            for row in data:
                name = row[0]
                values = row[1:] 

                item = {"name": name}

                for key, val in zip(keys, values):
                    if val == "0" or val is None:
                        continue
                    clean_val = val.replace("+", "").strip()
                    try:
                        if "." in clean_val:
                            clean_val = float(clean_val)
                        else:
                            clean_val = int(clean_val)
                    except:
                        continue

                    item[key] = clean_val

                chart_data.append(item)
        return chart_data
    def get_uni(id):
        data = UniversityModel.get_uni(id)
        return data

    def get_uni_detail_entry(typeDegree, id):
        data = UniversityModel.get_data_detail_entry(typeDegree, id)
        return data
    def get_data_detail_2(id):
        data = UniversityModel.get_data_detail_2(id)
        return data

