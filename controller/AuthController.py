from models.UserModel import UserModel
import ui.session as session_data

class AuthController:

    @staticmethod
    def login(email, password):
        user = UserModel.get_user_by_email(email)

        if user is None:
            return False, "Email không tồn tại!"

        if not UserModel.verify_password(password, user["password"]):
            return False, "Sai mật khẩu!"

        # Lưu session
        session_data.session["is_logged_in"] = True
        session_data.session["user_id"] = user["id"]
        session_data.session["role_type"] = user["role_type"]
        session_data.session["name"] = f'{user["first_name"]} {user["last_name"]}' # DEBUG
        return True, "Đăng nhập thành công!"

    @staticmethod
    def logout():
        session_data.session["is_logged_in"] = False
        session_data.session["user_id"] = None
        session_data.session["role_type"] = None
        session_data.session["name"] = None
