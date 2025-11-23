from models.UserModel import UserModel
import re
import ui.session as session_data
from controller.StudyBGController import StudyBGController
class UserController:
    @staticmethod
    def add_user(first_name, last_name, email, password, confirm_password):
        # -- Validate --
        if not first_name.strip():
            return False, "Vui lòng nhập họ"
        
        if not last_name.strip():
            return False, "Vui lòng nhập tên"
        
        if not email.strip():
            return False, "Vui lòng nhập email"
        
        if not password.strip():
            return False, "Vui lòng nhập mật khẩu"
        
        if not confirm_password.strip():
            return False, "Vui lòng xác nhận mật khẩu"
        
        if password != confirm_password:
            return False, "Password không trùng khớp!"
        if not validate_email(email.strip()):
            return False, "Định dạng email không hợp lệ (ví dụ: example@domain.com)"
        if email_exists(email.strip()):
            return False, "Email này đã được đăng ký trong hệ thống"
        if len(password) < 6:
            return False, "Password phải ≥ 6 ký tự"
        # -- Thêm user --
        try:
            success, user_id = UserModel.create_user(first_name, last_name, email, password)
            if not success:
                return False, "Đăng ký không thành công, vui lòng thử lại!" 
            StudyBGController.create_bg(user_id)
            return True, " Đăng ký thành công!"
        except Exception as e:
            return False, f"Lỗi DB: {str(e)}"
        
    def update_user(data):
        return UserModel.update_user(data)
    def get_user_by_email(email):
        country_id = UserModel.get_user_by_email(email)
        if isinstance(country_id, dict):
            id = country_id.get("id")
        return id
    def get_current_user():
        user_id = session_data.session.get("user_id")
        if user_id is None:
            return None
        user = UserModel.get_user_by_id(user_id)
        return user
    def get_pass_by_id(user_id):
        return UserModel.get_pass_by_id(user_id)
    def verify_password(plain_password, hashed_password):
        return UserModel.verify_password(plain_password, hashed_password)
    def hash_password(password):
        return UserModel.hash_password(password)
    def update_password(user_id, new_hashed_password):
        return UserModel.update_password(user_id, new_hashed_password)

def validate_email(email):
    """Kiểm tra định dạng email hợp lệ"""
    # Regex pattern để kiểm tra email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def email_exists(email):
        """Kiểm tra email đã tồn tại trong database"""
        user = UserModel.get_user_by_email(email.strip())
        return user is not None