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
        new_user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return True, new_user_id
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
    @staticmethod
    def get_user_by_id(id):
        """Lấy thông tin người dùng theo email"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
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
    
    def update_user(data):

        if not data.get("id"):
            return False, "Không tìm thấy ID người dùng"

        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = """
                UPDATE users SET
                    first_name=%s,
                    last_name=%s,
                    email=%s,
                    phone_number=%s,
                    country_id=%s,
                    gender=%s,
                    dob=%s,
                    postal_code=%s,
                    ethnic_group=%s,
                    main_lang=%s,
                    add_lang=%s,
                    special=%s,
                    update_date=NOW()
                WHERE id=%s
            """

            cursor.execute(sql, (
                data["first_name"],
                data["last_name"],
                data["email"],
                data["phone_number"],
                data["country_id"],
                data["gender"],
                data["dob"],
                data["postal_code"],
                data["ethnic_group"],
                data["main_lang"],
                data["add_lang"],
                data["special"],
                data["id"]
            ))

            conn.commit()
            cursor.close()
            conn.close()

            return True, "Cập nhật thông tin thành công!"

        except Exception as e:
            return False, f"Lỗi DB: {str(e)}"
    def get_pass_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()

        if row:
            return {"id": row[0], "password": row[1]}
        return None

    def update_password(user_id, new_hash):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hash, user_id))
        conn.commit()
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Cập nhật mật khẩu thành công"
        
