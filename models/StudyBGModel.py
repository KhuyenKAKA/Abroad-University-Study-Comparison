from db import get_connection

class StudyBGModel:
    @staticmethod
    def get_bg_by_id(id):
        """Lấy background study by id"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM study_bg WHERE user_id = %s', (id,))
            bg = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return bg if bg else None
        except Exception as err:
            print(f"Lỗi: {err}")
            return None
    @staticmethod
    def create_default(user_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO study_bg (
                user_id, level, major, academic_rate, gpa,
                graduate_year, act, gmat, sat,
                cat, gre, stat, ielts, toefl,
                pearson_test, cam_adv_test, inter_bac
            )
            VALUES (
                %s, NULL, NULL, NULL, NULL,
                NULL, NULL, NULL, NULL,
                NULL, NULL, NULL, NULL, NULL,
                NULL, NULL, NULL
            )
        """

        cursor.execute(sql, (user_id,))
        conn.commit()

        cursor.close()
        conn.close()
    @staticmethod
    def update_bg(payload): 
        """Cập nhật study background"""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = """
                UPDATE study_bg
                SET level = %s,
                    major = %s,
                    academic_rate = %s,
                    gpa = %s,
                    graduate_year = %s,
                    act = %s,
                    gmat = %s,
                    sat = %s,
                    cat = %s,
                    gre = %s,
                    stat = %s,
                    ielts = %s,
                    toefl = %s,
                    pearson_test = %s,
                    cam_adv_test = %s,
                    inter_bac = %s
                WHERE user_id = %s
            """

            cursor.execute(sql, (
                payload.get('level'),
                payload.get('major'),
                payload.get('academic_rate'),
                payload.get('gpa'),
                payload.get('graduate_year'),
                payload.get('act'),
                payload.get('gmat'),
                payload.get('sat'),
                payload.get('cat'),
                payload.get('gre'),
                payload.get('stat'),
                payload.get('ielts'),
                payload.get('toefl'),
                payload.get('pearson_test'),
                payload.get('cam_adv_test'),
                payload.get('inter_bac'),
                payload.get('user_id')
            ))

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Cập nhật thành công"
        except Exception as err:
            print(f"Lỗi: {err}")
            return False, "Cập nhật thất bại"