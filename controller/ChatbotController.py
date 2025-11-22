import json
import os
import threading
import re

from dotenv import load_dotenv

from google import genai
from google.genai import types
from google.oauth2 import service_account


class ChatbotController:
    def __init__(self, view):
        self.view = view

        # Client + model name dùng cho Vertex AI
        self.client = None
        self.MODEL_NAME = None

        # Dữ liệu ranking các trường
        self.full_data = []

        self.initialize_system()

    # ================== KHỞI TẠO HỆ THỐNG ==================
    def initialize_system(self):
        """
        - Load file .env
        - Khởi tạo client Vertex AI (Gemini tuned model)
        - Load dữ liệu raw_data_visualize.json
        """
        self.load_env_and_setup_client()

        self.full_data = self.load_json_data()
        if not self.full_data:
            self.send_to_ui("Lỗi: Không tìm thấy file dữ liệu raw_data_visualize.json.")
            return

        if not self.client or not self.MODEL_NAME:
            self.send_to_ui("Lỗi: Chưa cấu hình xong AI (kiểm tra .env và service_account.json).")
            return

        print("✅ Chatbot Controller sẵn sàng.")

    def load_env_and_setup_client(self):
        """
        - Tìm và load .env
        - Thiết lập biến môi trường cho Vertex AI
        - Tạo genai.Client() theo cấu hình khuyến nghị của google-genai
        """
        try:
            # 1. Tìm file .env
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

            # 2. Đọc env
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            model_name = os.getenv("GEMINI_TUNED_MODEL_NAME")
            use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")

            if not project_id:
                raise RuntimeError("Thiếu GOOGLE_CLOUD_PROJECT trong .env")
            if not model_name:
                # fallback base model nếu chưa có tuned model
                model_name = "models/gemini-1.5-flash"
                print("⚠️ GEMINI_TUNED_MODEL_NAME không có trong .env, dùng tạm:", model_name)

            # 3. Đảm bảo biến dùng Vertex AI được set trong process
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = use_vertex
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
            os.environ["GOOGLE_CLOUD_LOCATION"] = location

            # GOOGLE_APPLICATION_CREDENTIALS đã được load_dotenv đưa vào os.environ,
            # client sẽ tự dùng file service_account.json tương ứng (ADC).

            # 4. Tạo client đúng chuẩn Vertex AI (theo docs google-genai)
            #    https://github.com/googleapis/python-genai
            self.client = genai.Client(
                http_options=types.HttpOptions(api_version="v1")
            )
            self.MODEL_NAME = model_name

            print("✅ Đã khởi tạo GenAI client (Vertex AI)")
            print("   Project:", project_id, "| Location:", location)
            print("   Model:", self.MODEL_NAME)

        except Exception as e:
            self.client = None
            self.MODEL_NAME = None
            print("❌ Lỗi khởi tạo AI:", e)
            self.send_to_ui(f"Lỗi khởi tạo AI: {e}")


    def load_json_data(self):
        """
        Đọc file raw_data_visualize.json từ:
        - ../data/raw_data_visualize.json
        - ./data/raw_data_visualize.json
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            paths = [
                os.path.join(current_dir, "..", "data", "raw_data_visualize.json"),
                os.path.join(current_dir, "data", "raw_data_visualize.json")
            ]
            for p in paths:
                if os.path.exists(p):
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        print(f"✅ Đã load {len(data)} bản ghi trường đại học từ {p}")
                        return data
            print("❌ Không tìm thấy raw_data_visualize.json ở các đường dẫn mặc định.")
            return []
        except Exception as e:
            print("❌ Lỗi đọc JSON:", e)
            return []

    # ================== RAG: TÌM TRƯỜNG & FORMAT DỮ LIỆU ==================
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

            # Trích xuất viết tắt (VD: UCL, MIT)
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
            is_match_full = (query_lower in title_lower)
            is_match_country = (len(country_lower) > 2 and country_lower in query_lower)

            if is_match_abbr or is_match_main or is_match_full or is_match_country:
                results.append(item)

        return results[:5]  # lấy top 5

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
                # 1. Thông tin cơ bản
                title = item.get("title", "N/A")
                rank = item.get("rank_display", item.get("rank", "N/A"))
                score = item.get("overall_score", "N/A")
                loc = f"{item.get('city', '')}, {item.get('country', '')}"
                region = item.get("region", "")

                school_profile = f"=== HỒ SƠ TRƯỜNG: {title} ===\n"
                school_profile += f"- Địa điểm: {loc} ({region})\n"
                school_profile += f"- Xếp hạng thế giới (QS): {rank}\n"
                school_profile += f"- Điểm tổng (Overall Score): {score}\n"

                # 2. Thông tin thêm (Học phí, Học bổng, Tỉ lệ sinh viên...)
                if "more_info" in item and isinstance(item["more_info"], list):
                    school_profile += "- Thông tin tuyển sinh & Chi phí:\n"
                    for info in item["more_info"]:
                        val = str(info.get("value", "")).strip()
                        lbl = str(info.get("label", "")).strip()
                        if val and "Generate" not in val:
                            school_profile += f"  + {lbl}: {val}\n"

                # 3. Điểm chi tiết các tiêu chí (scores)
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

                # 4. Gợi ý cho AI cách phân tích
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

    # ================== NHẬN DẠNG INTENT ==================
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
            "nên chọn", "nên học", "should i choose", "recommend",
            "tư vấn", "phù hợp", "hợp với tôi", "which one", "better"
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

    # ================== XỬ LÝ INPUT TỪ UI ==================
    def process_input(self, user_msg: str):
        """
        Hàm được view gọi khi người dùng nhấn gửi.
        Chạy xử lý AI trên thread riêng để không block Tkinter.
        """
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
        - Ghép prompt phù hợp
        - Gọi model đã fine-tune để sinh câu trả lời
        """
        try:
            intent, found_items = self.detect_intent_and_targets(msg)

            if found_items:
                data_context = self.format_full_data_for_ai(found_items)

                if intent == "info":
                    prompt = f"""
Bạn là cố vấn du học quốc tế cho học sinh Việt Nam.
Người dùng hỏi: "{msg}"

Dưới đây là HỒ SƠ CHI TIẾT của trường liên quan:
{data_context}

YÊU CẦU:
1. Giải thích thông tin về TRƯỜNG mà người dùng hỏi.
2. Tóm tắt các điểm mạnh chính dựa trên các chỉ số (scores).
3. Nêu thêm thông tin về học phí, học bổng, tỉ lệ sinh viên quốc tế nếu có.
4. Trình bày rõ ràng, dùng gạch đầu dòng, in đậm các mục quan trọng.
5. Trả lời bằng cùng ngôn ngữ với câu hỏi (nếu user dùng tiếng Việt thì trả lời tiếng Việt).
"""

                elif intent == "compare":
                    prompt = f"""
Bạn là chuyên gia tư vấn chọn trường đại học quốc tế.
Người dùng hỏi: "{msg}"

Dưới đây là HỒ SƠ CHI TIẾT của các trường cần so sánh:
{data_context}

NHIỆM VỤ:
1. So sánh các trường theo:
   - Xếp hạng & điểm tổng.
   - Các chỉ số quan trọng (Academic Reputation, Employer Reputation, ... nếu có).
   - Học phí, học bổng, tỉ lệ sinh viên quốc tế.
2. Phân tích ưu / nhược điểm từng trường.
3. Đưa ra nhận xét trường nào nổi bật hơn ở từng khía cạnh.
4. Trình bày dạng gạch đầu dòng hoặc bảng so sánh dễ đọc.
5. Trả lời bằng cùng ngôn ngữ với câu hỏi.
"""

                elif intent == "recommend":
                    prompt = f"""
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
   Hãy phân tích trường nào PHÙ HỢP hơn cho các mục tiêu khác nhau:
   - Muốn học ở môi trường top thế giới.
   - Ngân sách hạn chế / ưu tiên chi phí.
   - Muốn nhiều cơ hội học bổng.
   - Thích môi trường nhiều sinh viên quốc tế.
3. Nếu câu hỏi chưa nêu rõ ngân sách / ngành học, hãy gợi ý vài câu hỏi ngắn để hiểu thêm nhu cầu,
   nhưng vẫn đưa ra gợi ý sơ bộ.
4. Kết thúc bằng đoạn tóm tắt: “Nếu bạn ưu tiên A, nên chọn X; nếu ưu tiên B, nên chọn Y…”.
5. Trả lời cùng ngôn ngữ với câu hỏi.
"""

                else:  # chit_chat nhưng vẫn có data
                    prompt = f"""
Người dùng hỏi: "{msg}"

Dưới đây là một số trường liên quan trong dữ liệu:
{data_context}

Hãy:
1. Giới thiệu thân thiện, ngắn gọn về các trường trên.
2. Gợi ý người dùng nếu muốn so sánh hoặc xin tư vấn cụ thể thì nên cung cấp:
   - Ngành học quan tâm,
   - Ngân sách dự kiến,
   - Quốc gia mong muốn,
   - Mức độ quan tâm tới học bổng.
3. Trả lời cùng ngôn ngữ với câu hỏi.
"""
            else:
                # Không tìm thấy trường nào khớp trong dữ liệu
                prompt = f"""
Người dùng hỏi: "{msg}"

Hiện không tìm thấy trường cụ thể nào trong database khớp với câu hỏi.
Hãy:
1. Trả lời lịch sự rằng bạn chưa có dữ liệu chi tiết về trường đó.
2. Gợi ý người dùng cung cấp:
   - Tên trường (tiếng Anh),
   - Quốc gia,
   - Ngành học,
   - Ngân sách dự kiến.
3. Nêu một số gợi ý chung về cách chọn trường du học (theo ranking, ngành, tài chính, học bổng...).
4. Trả lời bằng ngôn ngữ của câu hỏi.
"""

            # Gọi model đã fine-tune / base model qua Vertex AI
            response = self.client.models.generate_content(
                model=self.MODEL_NAME,
                contents=prompt
            )
            clean_text = (response.text or "").strip()
            self.send_to_ui(clean_text if clean_text else "Bot không trả lời được câu này, bạn thử hỏi lại cách khác nhé.")

        except Exception as e:
            self.send_to_ui(f"Lỗi AI: {str(e)}")

    # ================== HỖ TRỢ UI ==================
    def send_to_ui(self, text: str):
        if hasattr(self.view, "after"):
            self.view.after(0, lambda: self._update_ui_with_result(text))

    def _update_ui_with_result(self, text: str):
        self.view.hide_loading()
        self.view.add_message_to_chat("bot", text)
