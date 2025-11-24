import json
import os
import threading
import re

from dotenv import load_dotenv
from datetime import date

from google import genai
from google.genai import types

import mysql.connector
from mysql.connector import pooling


class ChatbotController:
    def __init__(self, view):
        self.view = view

        self.client = None
        self.MODEL_NAME = None

        self.full_data = []

        # MySQL
        self.db_pool = None
        self.current_user_id = None 

        self.initialize_system()

    def initialize_system(self):

        self.load_env_and_setup_client()
        self.setup_mysql_pool()

        self.full_data = self.load_json_data()
        if not self.full_data:
            self.send_to_ui("Lỗi: Không tìm thấy file dữ liệu raw_data_visualize.json.")
            return

        if not self.client or not self.MODEL_NAME:
            self.send_to_ui("Lỗi: Chưa cấu hình xong AI (kiểm tra .env và service_account.json).")
            return

        print("✅ Chatbot Controller sẵn sàng.")

    def load_env_and_setup_client(self):

        try:
       
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            env_paths = [
                os.path.join(current_dir, ".env"),
                os.path.join(project_root, ".env"),
            ]
            for p in env_paths:
                if os.path.exists(p):
                    load_dotenv(p)
                    break

            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            model_name = os.getenv("GEMINI_TUNED_MODEL_NAME")
            use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")

            if not project_id:
                raise RuntimeError("Thiếu GOOGLE_CLOUD_PROJECT trong .env")
            if not model_name:
                model_name = "models/gemini-1.5-flash"
                print("GEMINI_TUNED_MODEL_NAME không có trong .env, dùng tạm:", model_name)

            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = use_vertex
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
            os.environ["GOOGLE_CLOUD_LOCATION"] = location

            self.client = genai.Client(
                http_options=types.HttpOptions(api_version="v1")
            )
            self.MODEL_NAME = model_name

            print("Đã khởi tạo GenAI client (Vertex AI)")
            print("   Project:", project_id, "| Location:", location)
            print("   Model:", self.MODEL_NAME)

        except Exception as e:
            self.client = None
            self.MODEL_NAME = None
            print("Lỗi khởi tạo AI:", e)
            self.send_to_ui(f"Lỗi khởi tạo AI: {e}")

    def setup_mysql_pool(self):
        """Tạo connection pool tới MySQL (nếu cấu hình đầy đủ)."""
        try:
            host = os.getenv("MYSQL_HOST", "localhost")
            port = int(os.getenv("MYSQL_PORT", "3306"))
            user = os.getenv("MYSQL_USER")
            password = os.getenv("MYSQL_PASSWORD")
            database = os.getenv("MYSQL_DB")

            if not (user and password and database):
                print("Thiếu cấu hình MySQL trong .env, bỏ qua kết nối MySQL.")
                return

            self.db_pool = pooling.MySQLConnectionPool(
                pool_name="chatbot_pool",
                pool_size=5,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            )
            print("Đã tạo MySQL connection pool.")
        except Exception as e:
            self.db_pool = None
            print("Không thể kết nối MySQL:", e)

    def set_current_user(self, user_id: int):
        self.current_user_id = user_id

    def load_user_profile_from_db(self):
        if not self.db_pool or not self.current_user_id:
            return ""

        try:
            conn = self.db_pool.get_connection()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT 
                    u.first_name,
                    u.last_name,
                    u.gender,
                    u.dob,
                    c.name AS country_name,
                    s.level,
                    s.major,
                    s.academic_rate,
                    s.gpa,
                    s.graduate_year,
                    s.act,
                    s.gmat,
                    s.sat,
                    s.cat,
                    s.gre,
                    s.stat,
                    s.ielts,
                    s.toefl,
                    s.pearson_test,
                    s.cam_adv_test,
                    s.inter_bac
                FROM users u
                LEFT JOIN countries c ON u.country_id = c.id
                LEFT JOIN study_bg s ON s.user_id = u.id
                WHERE u.id = %s
                """,
                (self.current_user_id,),
            )
            row = cur.fetchone()

            cur.close()
            conn.close()

            if not row:
                return ""

            lines = ["THÔNG TIN HỌC SINH (lấy tự động từ hệ thống):"]

            full_name = " ".join(
                [x for x in [row.get("first_name"), row.get("last_name")] if x]
            ).strip()
            if full_name:
                lines.append(f"- Họ tên: {full_name}")

            gender_val = row.get("gender")
            if gender_val is not None:
                lines.append(f"- Giới tính: {'Nam' if bool(gender_val) else 'Nữ'}")

            dob = row.get("dob")
            if dob:
                today = date.today()
                age = today.year - dob.year - (
                    (today.month, today.day) < (dob.month, dob.day)
                )
                lines.append(f"- Tuổi (ước tính): {age}")

            country_name = row.get("country_name")
            if country_name:
                lines.append(f"- Quốc gia đang sinh sống/học tập: {country_name}")

            # Thông tin học thuật từ study_bg
            level = row.get("level")
            if level:
                lines.append(f"- Bậc học hiện tại/dự định: {level}")  

            major = row.get("major")
            if major:
                lines.append(f"- Ngành quan tâm / ngành đã học: {major}")

            academic_rate = row.get("academic_rate")
            if academic_rate:
                lines.append(f"- Xếp loại học lực (academic rate): {academic_rate}")

            gpa = row.get("gpa")
            if gpa is not None:
                lines.append(f"- GPA (nếu có, thang 4.0 hoặc theo hệ thống của trường): {gpa}")

            grad_year = row.get("graduate_year")
            if grad_year:
                lines.append(f"- Năm tốt nghiệp (dự kiến/đã tốt nghiệp): {grad_year}")

            # Các bài test chuẩn hoá
            test_lines = []
            for label, key in [
                ("IELTS", "ielts"),
                ("TOEFL", "toefl"),
                ("Pearson Test", "pearson_test"),
                ("Cambridge Advanced Test", "cam_adv_test"),
                ("International Baccalaureate", "inter_bac"),
                ("SAT", "sat"),
                ("ACT", "act"),
                ("GMAT", "gmat"),
                ("GRE", "gre"),
            ]:
                val = row.get(key)
                if val not in (None, 0, 0.0, ""):
                    test_lines.append(f"{label}: {val}")

            if test_lines:
                lines.append("- Điểm các bài thi chuẩn hoá (nếu có): " + "; ".join(test_lines))

            # Có thể dùng stat / cat nếu bạn định nghĩa rõ (mình để lại nhưng không in nếu không cần)
            # stat = row.get("stat")
            # cat = row.get("cat")

            lines.append(
                "- Khi tư vấn, hãy DỰA THEO toàn bộ hồ sơ trên "
                "(bậc học, ngành, GPA, năm tốt nghiệp, điểm tiếng Anh/standardized tests) "
                "để đánh giá khả năng cạnh tranh và gợi ý trường/phương án phù hợp."
            )

            return "\n".join(lines) + "\n"

        except Exception as e:
            print("Lỗi đọc hồ sơ user từ MySQL:", e)
            return ""

    def load_json_data(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            paths = [
                os.path.join(current_dir, "..", "data", "raw_data_visualize.json"),
                os.path.join(current_dir, "data", "raw_data_visualize.json"),
            ]
            for p in paths:
                if os.path.exists(p):
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        print(f" Đã load {len(data)} bản ghi trường đại học từ {p}")
                        return data
            print(" Không tìm thấy raw_data_visualize.json ở các đường dẫn mặc định.")
            return []
        except Exception as e:
            print(" Lỗi đọc JSON:", e)
            return []

    #  tìm trường và format dữ liệu
    def find_relevant_universities(self, query):
        """
        Tìm kiếm thông minh theo:
        - tên trường (có hoặc không có viết tắt trong ngoặc)
        - viết tắt (MIT, UCL,...)
        - quốc gia
        """
        query_lower = query.lower()
        results = []
        if len(query_lower) < 2:
            return []

        for item in self.full_data:
            raw_title = item.get("title", "")
            title_lower = raw_title.lower()
            country_lower = item.get("country", "").lower()

            abbreviation = ""
            match = re.search(r"\((.*?)\)", title_lower)
            if match:
                abbreviation = match.group(1)

            main_name = re.sub(r"\(.*?\)", "", title_lower).strip()

            is_match_abbr = (
                (len(abbreviation) >= 2 and abbreviation == query_lower)
                or (len(abbreviation) > 2 and abbreviation in query_lower)
            )
            is_match_main = (len(main_name) > 3 and main_name in query_lower)
            is_match_full = query_lower in title_lower
            is_match_country = (len(country_lower) > 2 and country_lower in query_lower)

            if is_match_abbr or is_match_main or is_match_full or is_match_country:
                results.append(item)

        return results[:5]  

    def format_full_data_for_ai(self, relevant_items):
        """
        Trích xuất TOÀN BỘ dữ liệu chi tiết của các trường để AI phân tích sâu:
        - Thông tin cơ bản
        - more_info: học phí, học bổng, student mix...
        - scores: các chỉ số QS (Academic Reputation, Employer, v.v.)
        """
        if not relevant_items:
            return "Không tìm thấy dữ liệu."

        full_text_report = ""

        for item in relevant_items:
            try:
                
                title = item.get("title", "N/A")
                rank = item.get("rank_display", item.get("rank", "N/A"))
                score = item.get("overall_score", "N/A")
                loc = f"{item.get('city', '')}, {item.get('country', '')}"
                region = item.get("region", "")

                school_profile = f"=== HỒ SƠ TRƯỜNG: {title} ===\n"
                school_profile += f"- Địa điểm: {loc} ({region})\n"
                school_profile += f"- Xếp hạng thế giới (QS): {rank}\n"
                school_profile += f"- Điểm tổng (Overall Score): {score}\n"

                if "more_info" in item and isinstance(item["more_info"], list):
                    school_profile += "- Thông tin tuyển sinh & Chi phí:\n"
                    for info in item["more_info"]:
                        val = str(info.get("value", "")).strip()
                        lbl = str(info.get("label", "")).strip()
                        if val and "Generate" not in val:
                            school_profile += f"  + {lbl}: {val}\n"

                if "scores" in item and isinstance(item["scores"], dict):
                    school_profile += "- Chi tiết các chỉ số đánh giá (Quan trọng):\n"
                    for category, indicators in item["scores"].items():
                        school_profile += f"  * Nhóm {category}:\n"
                        if isinstance(indicators, list):
                            for ind in indicators:
                                i_name = ind.get("indicator_name", "")
                                i_rank = ind.get("rank", "")
                                i_score = ind.get("score", "")
                                school_profile += (
                                    f"    -> {i_name}: {i_score}/100 (Rank {i_rank})\n"
                                )

                school_profile += (
                    "\n=> GỢI Ý PHÂN TÍCH: "
                    "Dựa trên các chỉ số trên, hãy đánh giá trường theo các khía cạnh sau: "
                    "chất lượng học thuật, cơ hội việc làm, mức độ quốc tế hóa, học phí, học bổng, "
                    "và sự phù hợp với mục tiêu của từng học sinh (ví dụ: học top, tiết kiệm chi phí, "
                    "ưu tiên học bổng, môi trường quốc tế...).\n"
                )

                full_text_report += school_profile + "\n-------------------\n"
            except Exception:
                continue

        return full_text_report
    # nhận dạng các intent
    def detect_intent_and_targets(self, msg: str):
        """
        Phân loại intent:
        - info: hỏi thông tin 1 trường
        - compare: so sánh nhiều trường
        - recommend: xin tư vấn chọn trường
        - chit_chat: chưa rõ, hoặc nói chung chung
        Đồng thời trả về danh sách trường liên quan (tối đa 3).
        """
        msg_lower = msg.lower()
        found_items = self.find_relevant_universities(msg)
        n = len(found_items)

        compare_keywords = ["so sánh", "compare", " vs ", " versus ", " giữa ", "với", "between"]
        recommend_keywords = [
            "nên chọn",
            "nên học",
            "should i choose",
            "recommend",
            "tư vấn",
            "phù hợp",
            "hợp với tôi",
            "which one",
            "better",
        ]

        if any(k in msg_lower for k in compare_keywords) or n >= 2:
            intent = "compare"
        elif any(k in msg_lower for k in recommend_keywords):
            intent = "recommend"
        elif n == 1:
            intent = "info"
        else:
            intent = "chit_chat"

        # Giới hạn số trường đưa vào context
        if intent in ["compare", "recommend"]:
            found_items = found_items[:3]
        elif intent == "info":
            found_items = found_items[:1]

        return intent, found_items

    # xử lý input từ ui
    def process_input(self, user_msg: str):
        if not self.client or not self.MODEL_NAME:
            self.send_to_ui("Bot chưa sẵn sàng (lỗi cấu hình AI).")
            return

        self.view.show_loading()
        t = threading.Thread(target=self._smart_reply_thread, args=(user_msg,))
        t.start()

    def _smart_reply_thread(self, msg: str):
        """
        Chạy trong thread:
        - Nhận dạng intent
        - Lấy dữ liệu trường liên quan (RAG)
        - Lấy hồ sơ user từ MySQL (nếu có)
        - Ghép prompt phù hợp
        - Gọi model đã fine-tune để sinh câu trả lời
        """
        try:
            intent, found_items = self.detect_intent_and_targets(msg)

            # Lấy hồ sơ user 
            user_profile_text = self.load_user_profile_from_db()
            if user_profile_text:
                user_profile_block = (
                    "=== THÔNG TIN HỌC SINH ===\n"
                    + user_profile_text
                    + "\nKhi tư vấn, hãy ưu tiên các gợi ý phù hợp với hồ sơ này.\n\n"
                )
            else:
                user_profile_block = ""

            if found_items:
                data_context = self.format_full_data_for_ai(found_items)

                if intent == "info":
                    prompt = f"""
{user_profile_block}
Bạn là cố vấn du học quốc tế cho học sinh Việt Nam.
Người dùng hỏi: "{msg}"

Dưới đây là HỒ SƠ CHI TIẾT của trường liên quan:
{data_context}

YÊU CẦU:
1. Giải thích thông tin về TRƯỜNG mà người dùng hỏi.
2. Tóm tắt các điểm mạnh chính dựa trên các chỉ số (scores).
3. Nêu thêm thông tin về học phí, học bổng, tỉ lệ sinh viên quốc tế nếu có.
4. Nếu có hồ sơ học sinh ở trên, hãy kết nối phân tích với hồ sơ đó (GPA, IELTS, ngân sách...) để gợi ý cá nhân hóa.
5. Trình bày rõ ràng, dùng gạch đầu dòng, in đậm các mục quan trọng.
6. Trả lời bằng cùng ngôn ngữ với câu hỏi (nếu user dùng tiếng Việt thì trả lời tiếng Việt).
"""

                elif intent == "compare":
                    prompt = f"""
{user_profile_block}
Bạn là chuyên gia tư vấn chọn trường đại học quốc tế.
Người dùng hỏi: "{msg}"

Dưới đây là HỒ SƠ CHI TIẾT của các trường cần so sánh:
{data_context}

NHIỆM VỤ:
1. So sánh các trường theo:
   - Xếp hạng & điểm tổng.
   - Các chỉ số quan trọng (Academic Reputation, Employer Reputation, ... nếu có).
   - Học phí, học bổng, tỉ lệ sinh viên quốc tế.
2. Nếu có hồ sơ học sinh ở trên, hãy phân tích trường nào phù hợp hơn với:
   - GPA và IELTS hiện tại.
   - Ngân sách (budget).
   - Quốc gia/major mong muốn.
3. Phân tích ưu / nhược điểm từng trường.
4. Đưa ra nhận xét trường nào nổi bật hơn cho từng mục tiêu (học top, tiết kiệm chi phí, ưu tiên học bổng...).
5. Trình bày dạng gạch đầu dòng hoặc bảng so sánh dễ đọc.
6. Trả lời bằng cùng ngôn ngữ với câu hỏi.
"""

                elif intent == "recommend":
                    prompt = f"""
{user_profile_block}
Bạn là chuyên gia tư vấn du học quốc tế.
Người dùng hỏi: "{msg}"

Dưới đây là HỒ SƠ CHI TIẾT của các trường liên quan:
{data_context}

NHIỆM VỤ:
1. Giả sử người dùng đang phân vân giữa các trường này.
2. Dựa trên:
   - Ranking và chất lượng học thuật.
   - Cơ hội việc làm (Employer Reputation nếu có).
   - Học phí, học bổng, tỉ lệ sinh viên quốc tế.
   - HỒ SƠ HỌC SINH (GPA, IELTS, ngân sách, ngành, quốc gia mong muốn) trong phần đầu nếu có.
   Hãy phân tích trường nào PHÙ HỢP hơn cho từng kiểu học sinh (ưu tiên top, ưu tiên học bổng, ưu tiên tiết kiệm...).
3. Nếu câu hỏi chưa nêu rõ, vẫn phải dùng hồ sơ ở trên (nếu có) để cá nhân hóa lời khuyên.
4. Kết thúc bằng đoạn tóm tắt: “Nếu bạn ưu tiên A, nên chọn X; nếu ưu tiên B, nên chọn Y…”.
5. Trả lời cùng ngôn ngữ với câu hỏi.
"""

                else:  
                    prompt = f"""
{user_profile_block}
Người dùng hỏi: "{msg}"

Dưới đây là một số trường liên quan trong dữ liệu:
{data_context}

Hãy:
1. Giới thiệu thân thiện, ngắn gọn về các trường trên.
2. Nếu có hồ sơ học sinh ở phần đầu, hãy gợi ý sơ bộ trường/loại trường phù hợp với hồ sơ đó.
3. Gợi ý người dùng nếu muốn so sánh hoặc xin tư vấn cụ thể thì nên cung cấp thêm:
   - Ngành học quan tâm (nếu chưa có trong hồ sơ),
   - Ngân sách dự kiến (nếu chưa có),
   - Quốc gia mong muốn (nếu chưa có).
4. Trả lời cùng ngôn ngữ với câu hỏi.
"""
            else:
                
                prompt = f"""
{user_profile_block}
Người dùng hỏi: "{msg}"

Hiện không tìm thấy trường cụ thể nào trong database khớp với câu hỏi.
Hãy:
1. Trả lời lịch sự rằng bạn chưa có dữ liệu chi tiết về trường đó.
2. Nếu có hồ sơ học sinh ở phần đầu, hãy đưa ra một vài gợi ý chung phù hợp với hồ sơ đó
   (ví dụ: nên ưu tiên loại trường, quốc gia nào, mức ranking nào...).
3. Gợi ý người dùng cung cấp thêm:
   - Tên trường (tiếng Anh),
   - Quốc gia,
   - Ngành học,
   - Ngân sách dự kiến.
4. Nêu một số gợi ý chung về cách chọn trường du học (theo ranking, ngành, tài chính, học bổng...).
5. Trả lời bằng ngôn ngữ của câu hỏi.
"""

            response = self.client.models.generate_content(
                model=self.MODEL_NAME,
                contents=prompt,
            )
            clean_text = (response.text or "").strip()
            if not clean_text:
                clean_text = "Bot không trả lời được câu này, bạn thử hỏi lại cách khác nhé."
            self.send_to_ui(clean_text)

        except Exception as e:
            self.send_to_ui(f"Lỗi AI: {str(e)}")

    #  HỖ TRỢ UI 
    def send_to_ui(self, text: str):
        if hasattr(self.view, "after"):
            self.view.after(0, lambda: self._update_ui_with_result(text))

    def _update_ui_with_result(self, text: str):
        self.view.hide_loading()
        self.view.add_message_to_chat("bot", text)
