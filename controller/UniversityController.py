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
    
    