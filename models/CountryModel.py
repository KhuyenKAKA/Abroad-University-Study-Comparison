from db import get_connection
import datetime

class CountryModel:
    @staticmethod
    def get_id_by_name(name):
        """Lấy id by name"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            lower_name = name.lower()
            
            cursor.execute('SELECT id FROM countries wHERE LOWER(name) = %s', (lower_name,))
            id = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return id if id else None
        except Exception as err:
            print(f"Lỗi: {err}")
            return []
    @staticmethod
    def get_name_by_id(id):
        """Lấy name by id"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT name FROM countries wHERE id = %s', (id,))
            name = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return name if name else None
        except Exception as err:
            print(f"Lỗi: {err}")
            return []