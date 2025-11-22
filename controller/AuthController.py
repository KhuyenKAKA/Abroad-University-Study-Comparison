from models.UserModel import UserModel
from ui.session import session

class AuthController:

    @staticmethod
    def login(email, password):
        user = UserModel.get_user_by_email(email)

        if user is None:
            return False, "Email không tồn tại!"

        if not UserModel.verify_password(password, user["password"]):
            return False, "Sai mật khẩu!"

        # Lưu session
        session["is_logged_in"] = True
        session["user_id"] = user["id"]
        session["role_type"] = user["role_type"]
        session["name"] = f'{user["first_name"]} {user["last_name"]}'

        return True, "Đăng nhập thành công!"

    @staticmethod
    def logout():
        session["is_logged_in"] = False
        session["user_id"] = None
        session["role_type"] = None
        session["name"] = None
