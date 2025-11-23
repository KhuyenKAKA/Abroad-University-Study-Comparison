from models.StudyBGModel import StudyBGModel
import ui.session as session_data   
class StudyBGController:   
    @staticmethod
    def get_current_user_bg():
          user_id = session_data.session.get("user_id", None)
          return StudyBGModel.get_bg_by_id(user_id) if user_id else None
    def create_bg(user_id):
        return StudyBGModel.create_default(user_id)
    def update_bg(payload):
         return StudyBGModel.update_bg(payload)