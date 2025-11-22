from db import get_connection
import datetime
import bcrypt



class UserModel:
    @staticmethod
    def create_user(first_name, last_name, email, password, role_type=1):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO users (
                first_name, last_name, email, password, insert_date, update_date, role_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        now = datetime.datetime.now()
        hashed_password = UserModel.hash_password(password)
        cursor.execute(sql, (first_name, last_name, email, hashed_password, now, now, role_type))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    @staticmethod
    def delete_user(user_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM user WHERE id = %s"
        cursor.execute(sql, (user_id,))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    def is_admin(role_type):
        return role_type == 2
    @staticmethod
    def get_user_by_email(email):
        """Lấy thông tin người dùng theo email"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return user
        except Exception as err:
            print(f"Lỗi: {err}")
            return None

    def get_all_users(self):
        """Lấy tất cả người dùng"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return users
        except Exception as err:
            print(f"Lỗi: {err}")
            return []

    def hash_password(password):
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            return hashed.decode()

    def verify_password(password, hashed_password):
            return bcrypt.checkpw(password.encode(), hashed_password.encode())