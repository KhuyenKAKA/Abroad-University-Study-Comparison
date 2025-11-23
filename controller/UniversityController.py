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