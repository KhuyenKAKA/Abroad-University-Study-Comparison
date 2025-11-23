from models.CountryModel import CountryModel    

class CountryController:
    @staticmethod
    def get_id_by_name(name):
        return CountryModel.get_id_by_name(name)
    def get_name_by_id(id):
        return CountryModel.get_name_by_id(id)