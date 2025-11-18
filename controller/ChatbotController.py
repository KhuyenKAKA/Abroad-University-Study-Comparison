import json
import os
import threading
import re
import google.generativeai as genai
from dotenv import load_dotenv

class ChatbotController:
    def __init__(self, view):
        self.view = view
        self.model = None
        self.chat_session = None
        self.full_data = [] 
        self.API_KEY = None
        
        self.initialize_system()

    def initialize_system(self):
        self.load_env_key()
        if not self.API_KEY:
            self.send_to_ui("Lỗi: Chưa có API Key trong file .env.")
            return

        self.full_data = self.load_json_data()
        if self.full_data:
            self.setup_gemini_basic()
        else:
            self.send_to_ui("Lỗi: Không tìm thấy file dữ liệu.")

    def load_env_key(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            paths = [os.path.join(current_dir, '.env'), os.path.join(project_root, '.env')]
            for p in paths:
                if os.path.exists(p):
                    load_dotenv(p)
                    self.API_KEY = os.getenv("GEMINI_API_KEY")
                    if self.API_KEY: return
            self.API_KEY = os.getenv("GEMINI_API_KEY")
        except: pass

    def load_json_data(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            paths = [
                os.path.join(current_dir, '..', 'data', 'raw_data_visualize.json'),
                os.path.join(current_dir, 'data', 'raw_data_visualize.json')
            ]
            for p in paths:
                if os.path.exists(p):
                    with open(p, 'r', encoding='utf-8') as f:
                        return json.load(f)
            return []
        except: return []

    def setup_gemini_basic(self):
        try:
            genai.configure(api_key=self.API_KEY)
            # Model flash đủ nhanh và thông minh để phân tích dữ liệu text này
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            self.chat_session = self.model.start_chat(history=[])
            print("Chatbot Controller: Sẵn sàng.")
        except Exception as e:
            self.send_to_ui(f"Lỗi kết nối AI: {e}")

    def find_relevant_universities(self, query):
        """Tìm kiếm thông minh hỗ trợ viết tắt"""
        query_lower = query.lower()
        results = []
        if len(query) < 2: return [] 
        
        for item in self.full_data:
            raw_title = item.get('title', '')
            title_lower = raw_title.lower()
            country_lower = item.get('country', '').lower()
            
            # Trích xuất viết tắt (VD: UCL, MIT)
            abbreviation = ""
            match = re.search(r'\((.*?)\)', title_lower)
            if match: abbreviation = match.group(1)
            
            main_name = re.sub(r'\(.*?\)', '', title_lower).strip()

            # Logic so khớp
            is_match_abbr = (len(abbreviation) >= 2 and abbreviation == query_lower) or (len(abbreviation) > 2 and abbreviation in query_lower)
            is_match_main = (len(main_name) > 3 and main_name in query_lower)
            is_match_full = (query_lower in title_lower)
            is_match_country = (len(country_lower) > 2 and country_lower in query_lower)

            if is_match_abbr or is_match_main or is_match_full or is_match_country:
                results.append(item)
        
        return results[:5] # Lấy top 5

    # --- ĐÂY LÀ HÀM QUAN TRỌNG NHẤT ĐÃ ĐƯỢC VIẾT LẠI ---
    def format_full_data_for_ai(self, relevant_items):
        """
        Trích xuất TOÀN BỘ dữ liệu chi tiết của trường để AI phân tích sâu.
        Bao gồm: Điểm thành phần (scores), Học phí, Student Mix...
        """
        if not relevant_items: return "Không tìm thấy dữ liệu."
        
        full_text_report = ""
        
        for item in relevant_items:
            try:
                # 1. Thông tin cơ bản
                title = item.get('title', 'N/A')
                rank = item.get('rank_display', 'N/A')
                score = item.get('overall_score', 'N/A')
                loc = f"{item.get('city', '')}, {item.get('country', '')}"
                region = item.get('region', '')
                
                school_profile = f"=== HỒ SƠ TRƯỜNG: {title} ===\n"
                school_profile += f"- Địa điểm: {loc} ({region})\n"
                school_profile += f"- Xếp hạng thế giới: {rank}\n"
                school_profile += f"- Điểm tổng (Overall Score): {score}\n"

                # 2. Thông tin thêm (Học phí, Học bổng, Tỉ lệ sinh viên...)
                if 'more_info' in item and isinstance(item['more_info'], list):
                    school_profile += "- Thông tin tuyển sinh & Chi phí:\n"
                    for info in item['more_info']:
                        val = str(info.get('value', '')).strip()
                        lbl = str(info.get('label', '')).strip()
                        if val and "Generate" not in val:
                            school_profile += f"  + {lbl}: {val}\n"

                # 3. ĐIỂM CHI TIẾT CÁC TIÊU CHÍ (SCORES) - Phần quan trọng mới thêm vào
                if 'scores' in item and isinstance(item['scores'], dict):
                    school_profile += "- Chi tiết các chỉ số đánh giá (Quan trọng):\n"
                    # Duyệt qua từng nhóm (VD: Research, Employability...)
                    for category, indicators in item['scores'].items():
                        school_profile += f"  * Nhóm {category}:\n"
                        if isinstance(indicators, list):
                            for ind in indicators:
                                i_name = ind.get('indicator_name', '')
                                i_rank = ind.get('rank', '')
                                i_score = ind.get('score', '')
                                school_profile += f"    -> {i_name}: {i_score}/100 (Rank {i_rank})\n"

                full_text_report += school_profile + "\n-------------------\n"
            except Exception as e:
                continue
                
        return full_text_report

    def process_input(self, user_msg):
        if not self.chat_session:
            self.send_to_ui("Bot chưa sẵn sàng.")
            return
        
        self.view.show_loading()
        t = threading.Thread(target=self._smart_reply_thread, args=(user_msg,))
        t.start()

    def _smart_reply_thread(self, msg):
        try:
            found_items = self.find_relevant_universities(msg)
            
            if found_items:
                # Gọi hàm format mới đầy đủ chi tiết
                data_context = self.format_full_data_for_ai(found_items)
                
                # PROMPT MỚI: Yêu cầu phân tích sâu
                prompt = f"""
                Người dùng hỏi: "{msg}"
                
                Dưới đây là HỒ SƠ CHI TIẾT ĐẦY ĐỦ của trường được trích xuất từ database:
                {data_context}
                
                YÊU CẦU TRẢ LỜI:
                1. Đóng vai chuyên gia tư vấn giáo dục, đưa ra câu trả lời chi tiết và sâu sắc.
                2. Đừng chỉ liệt kê số liệu. Hãy **phân tích** các điểm mạnh của trường dựa trên phần "Chi tiết các chỉ số đánh giá" (ví dụ: nếu điểm Academic Reputation cao, hãy khen ngợi chất lượng đào tạo; nếu Employer Reputation cao, hãy nói về cơ hội việc làm).
                3. Cung cấp đầy đủ thông tin về Học phí và Học bổng nếu có trong dữ liệu.
                4. Trình bày đẹp, dễ đọc (dùng gạch đầu dòng, in đậm các mục quan trọng).
                5. KHÔNG dùng dấu ngoặc kép ("") bao quanh toàn bộ câu trả lời.
                """
            else:
                prompt = f"""User: "{msg}"\n(Không tìm thấy tên trường cụ thể). Hãy trả lời xã giao, hỏi lại tên trường/quốc gia cụ thể."""

            response = self.chat_session.send_message(prompt)
            
            clean_text = response.text.strip().strip('"').strip("'")
            self.send_to_ui(clean_text)
            
        except Exception as e:
            self.send_to_ui(f"Lỗi hệ thống: {e}")

    def send_to_ui(self, text):
        if hasattr(self.view, 'after'):
            self.view.after(0, lambda: self._update_ui_with_result(text))

    def _update_ui_with_result(self, text):
        self.view.hide_loading()
        self.view.add_message_to_chat("bot", text)