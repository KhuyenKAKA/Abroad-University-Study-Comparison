import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps
import os
import sys

# --- CẤU HÌNH ĐƯỜNG DẪN ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from controller.ChatbotController import ChatbotController
except ImportError:
    ChatbotController = None

# --- MÀU SẮC & FONT ---
COLOR_PAGE_BG = "#eef2f6"       # Màu nền trang (xám xanh nhạt để làm nổi bật box chat)
COLOR_CHAT_BG = "#ffffff"       # Màu nền khung chat (Trắng hoặc xám rất nhạt)
COLOR_HEADER_FOOTER = "#ffffff"
COLOR_BLUE_LOGO = "#1e90ff"     
COLOR_BLUE_BTN = "#1F3AB0"    
COLOR_GREEN_BTN = "#28a745"
COLOR_BOT_BUBBLE = "#f1f3f5"
COLOR_USER_BUBBLE = "#1F3AB0"

FONT_NAV = ("Arial", 10)
FONT_LOGO = ("Arial", 16, "bold")
FONT_CHAT = ("Arial", 11)

# ========================================================
# CLASS: HIỆU ỨNG LOADING
# ========================================================
class LoadingBubble(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BOT_BUBBLE, **kwargs)
        self.dots = []
        for i in range(3):
            dot = tk.Label(self, text="•", font=("Arial", 24), fg="#adb5bd", bg=COLOR_BOT_BUBBLE)
            dot.pack(side="left", padx=2)
            self.dots.append(dot)
        self.running = True
        self.animate(0)

    def animate(self, step):
        if not self.running: return
        for i, dot in enumerate(self.dots):
            if i == step % 3:
                dot.config(fg="#495057")
            else:
                dot.config(fg="#adb5bd")
        self.after(300, lambda: self.animate(step + 1))

    def stop(self):
        self.running = False
        self.destroy()

# ========================================================
# CLASS: APP CHÍNH
# ========================================================
class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("UniCompare - Chat Support")
        self.geometry("1200x900") # Tăng chiều cao để nhìn thoáng hơn
        self.configure(bg=COLOR_PAGE_BG)

        self.assets_path = os.path.join(project_root, "assets")
        self.icons = {} 
        self.load_assets()

        # 1. HEADER (Cố định ở trên cùng)
        self.build_header()

        # 2. MAIN SCROLLABLE AREA (Chứa Chat Box + Footer)
        self.build_main_scroll_area()

        # --- INIT CONTROLLER ---
        self.loading_indicator = None
        if ChatbotController:
            try:
                self.controller = ChatbotController(self)
                self.add_message_to_chat("bot", "Xin chào! Mình là trợ lý ảo UniCompare. Mình có thể giúp gì cho bạn?")
            except Exception as e:
                print(f"Lỗi controller: {e}")
                self.controller = None
        else:
            self.controller = None
            self.add_message_to_chat("bot", "Chế độ Demo (Chưa có Controller).")

    def load_assets(self):
        def get_icon(filename, size):
            path = os.path.join(self.assets_path, filename)
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            return None

        self.icons['search'] = get_icon("search.png", (20, 20))
        self.icons['fb'] = get_icon("104498_facebook_icon.png", (15, 15))
        self.icons['ins'] = get_icon("1161953_instagram_icon.png", (15, 15))
        self.icons['li'] = get_icon("5279114_linkedin_network_social network_linkedin logo_icon.png", (15, 15))
        self.icons['x'] = get_icon("11244080_x_twitter_elon musk_twitter new logo_icon.png", (15, 15))

        self.bot_avatar_tk = None
        avatar_path = os.path.join(self.assets_path, "bot_avatar.jpg") 
        if os.path.exists(avatar_path):
            self.bot_avatar_tk = self.create_circular_avatar(avatar_path, (35, 35))

    def create_circular_avatar(self, image_path, size):
        try:
            img = Image.open(image_path)
            img = ImageOps.fit(img, size, centering=(0.5, 0.5))
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            img.putalpha(mask)
            return ImageTk.PhotoImage(img)
        except:
            return None

    # ---------------------------------------------------------
    # 1. HEADER
    # ---------------------------------------------------------
    def build_header(self):
        nav_frame = tk.Frame(self, bg=COLOR_HEADER_FOOTER, height=60)
        nav_frame.pack(fill='x', side="top")
        nav_frame.pack_propagate(False)

        # Logo
        tk.Label(nav_frame, text="UniCompare", font=FONT_LOGO, fg=COLOR_BLUE_LOGO, bg=COLOR_HEADER_FOOTER).pack(side="left", padx=(50, 40))

        # Menu
        menu_items = ["Rankings", "Discover", "Events", "Prepare", "Scholarships", "Chat To Students"]
        for item in menu_items:
            tk.Button(nav_frame, text=item, font=FONT_NAV, bg=COLOR_HEADER_FOOTER, fg="black", bd=0, activebackground="#f0f0f0", cursor="hand2").pack(side="left", padx=5)

        # Right Side
        right_frame = tk.Frame(nav_frame, bg=COLOR_HEADER_FOOTER)
        right_frame.pack(side="right", padx=(0, 50))

        tk.Button(right_frame, text="Free Counselling", bg=COLOR_GREEN_BTN, fg="white", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5).pack(side="left", padx=5)
        
        if self.icons['search']:
            tk.Button(right_frame, image=self.icons['search'], bg=COLOR_HEADER_FOOTER, bd=0).pack(side="left", padx=5)
        else:
            tk.Label(right_frame, text="🔍", bg=COLOR_HEADER_FOOTER).pack(side="left", padx=5)

        tk.Button(right_frame, text="Login", bg=COLOR_BLUE_BTN, fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=5).pack(side="left", padx=5)
        tk.Button(right_frame, text="Sign Up", bg=COLOR_BLUE_BTN, fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=5).pack(side="left", padx=5)

    # ---------------------------------------------------------
    # 2. MAIN SCROLL AREA (PAGE SCROLL)
    # ---------------------------------------------------------
    def build_main_scroll_area(self):
        # Frame container cho Canvas
        self.main_container = tk.Frame(self, bg=COLOR_PAGE_BG)
        self.main_container.pack(fill="both", expand=True)

        # Scrollbar cho trang chính
        self.page_scrollbar = ttk.Scrollbar(self.main_container, orient="vertical")
        self.page_scrollbar.pack(side="right", fill="y")

        # Canvas trang chính
        self.page_canvas = tk.Canvas(self.main_container, bg=COLOR_PAGE_BG, highlightthickness=0, yscrollcommand=self.page_scrollbar.set)
        self.page_canvas.pack(side="left", fill="both", expand=True)
        
        self.page_scrollbar.config(command=self.page_canvas.yview)

        # Frame nội dung bên trong Canvas (Chứa Chat Box + Footer)
        self.content_frame = tk.Frame(self.page_canvas, bg=COLOR_PAGE_BG)
        
        # Liên kết frame với canvas
        self.page_canvas.create_window((0, 0), window=self.content_frame, anchor="nw", tags="content_window")
        
        # Cập nhật kích thước Canvas khi nội dung thay đổi
        self.content_frame.bind("<Configure>", lambda e: self.page_canvas.configure(scrollregion=self.page_canvas.bbox("all")))
        self.page_canvas.bind("<Configure>", lambda e: self.page_canvas.itemconfigure("content_window", width=e.width))

        # --- A. KHỐI CHAT (CHAT WINDOW) ---
        self.build_chat_window(self.content_frame)

        # --- B. FOOTER (Nằm dưới khối chat) ---
        self.build_footer(self.content_frame)

        # Bind scroll chuột cho trang chính
        # Lưu ý: Sẽ cần xử lý xung đột scroll giữa trang chính và vùng tin nhắn
        self.page_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        # Hàm này cho phép cuộn trang chính
        self.page_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # ---------------------------------------------------------
    # 3. CHAT WINDOW (KHUNG CHAT NỔI)
    # ---------------------------------------------------------
    def build_chat_window(self, parent):
        # Frame bao bên ngoài để căn lề (Padding 4 phía như yêu cầu)
        # pady=(50, 50): Cách Header 50px, Cách Footer 50px
        # padx=100: Thu hẹp 2 bên
        outer_frame = tk.Frame(parent, bg=COLOR_PAGE_BG)
        outer_frame.pack(fill="x", pady=20, padx=20) 

        # KHUNG CHAT CHÍNH (Màu xám/trắng nổi bật)
        # Dùng relief='raised' hoặc 'solid' để tạo viền
        self.chat_box = tk.Frame(outer_frame, bg=COLOR_CHAT_BG, bd=1, relief="solid")
        self.chat_box.pack(fill="both", expand=True)

        # --- Header của Chat Box (Tùy chọn, để đẹp hơn) ---
        chat_header = tk.Frame(self.chat_box, bg="#f8f9fa", height=50)
        chat_header.pack(fill="x")
        tk.Label(chat_header, text="💬 Live Support", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333").pack(side="left", padx=20, pady=10)
        tk.Label(chat_header, text="● Online", font=("Arial", 10), bg="#f8f9fa", fg=COLOR_GREEN_BTN).pack(side="left", padx=5)

        # --- Vùng hiển thị tin nhắn (Scroll riêng) ---
        # Fixed height=500 để đảm bảo Footer nằm dưới
        msg_container = tk.Frame(self.chat_box, bg=COLOR_CHAT_BG, height=500) 
        msg_container.pack(fill="x")
        msg_container.pack_propagate(False) # Giữ chiều cao cố định

        self.msg_canvas = tk.Canvas(msg_container, bg=COLOR_CHAT_BG, highlightthickness=0)
        msg_scrollbar = ttk.Scrollbar(msg_container, orient="vertical", command=self.msg_canvas.yview)
        
        self.messages_area = tk.Frame(self.msg_canvas, bg=COLOR_CHAT_BG)
        
        self.messages_area.bind("<Configure>", lambda e: self.msg_canvas.configure(scrollregion=self.msg_canvas.bbox("all")))
        self.msg_window = self.msg_canvas.create_window((0, 0), window=self.messages_area, anchor="nw")
        self.msg_canvas.bind("<Configure>", lambda e: self.msg_canvas.itemconfigure(self.msg_window, width=e.width))

        self.msg_canvas.configure(yscrollcommand=msg_scrollbar.set)
        
        msg_scrollbar.pack(side="right", fill="y")
        self.msg_canvas.pack(side="left", fill="both", expand=True)

        # Xử lý scroll riêng cho vùng tin nhắn khi di chuột vào
        def _bind_msg_scroll(event):
            self.page_canvas.unbind_all("<MouseWheel>")
            self.msg_canvas.bind_all("<MouseWheel>", lambda e: self.msg_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        def _unbind_msg_scroll(event):
            self.msg_canvas.unbind_all("<MouseWheel>")
            self.page_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.msg_canvas.bind("<Enter>", _bind_msg_scroll)
        self.msg_canvas.bind("<Leave>", _unbind_msg_scroll)


        # --- Thanh nhập liệu (Nằm TRONG Chat Box, dưới cùng) ---
        input_frame = tk.Frame(self.chat_box, bg=COLOR_CHAT_BG, height=70)
        input_frame.pack(fill="x", side="bottom")
        
        tk.Frame(input_frame, bg="#dee2e6", height=1).pack(fill="x", side="top") # Separator

        inner_input = tk.Frame(input_frame, bg=COLOR_CHAT_BG)
        inner_input.pack(pady=15)

        self.entry = tk.Entry(inner_input, font=("Arial", 11), width=40, bd=1, relief="solid")
        self.entry.pack(side="left", padx=10, ipady=8)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = tk.Button(inner_input, text="Gửi ➤", bg=COLOR_BLUE_BTN, fg="white", font=("Arial", 10, "bold"), bd=0, padx=20, pady=8, cursor="hand2", command=self.send_message)
        self.send_btn.pack(side="left", padx=10)

    # ---------------------------------------------------------
    # 4. FOOTER (Nằm dưới cùng trang cuộn)
    # ---------------------------------------------------------
    def build_footer(self, parent):
        footer_frame = tk.Frame(parent, bg=COLOR_HEADER_FOOTER, pady=40, padx=50)
        footer_frame.pack(fill="x", side="bottom")

        # Cột Logo
        tk.Label(footer_frame, text="UniCompare", font=FONT_LOGO, fg=COLOR_BLUE_LOGO, bg=COLOR_HEADER_FOOTER).grid(row=0, column=0, sticky="nw")
        tk.Label(footer_frame, text="© QS Quacquarelli Symonds\nLimited 1994 - 2025.\nAll rights reserved.", font=("Arial", 8), fg="gray", bg=COLOR_HEADER_FOOTER, justify="left").grid(row=4, column=0, sticky="sw", pady=(30, 0))

        # Cột Links
        links_data = [
            ("About", []), ("Contact", ["For Students", "Scholarships"]),
            ("Privacy", ["List courses", "Advertise"]), ("Users", ["Cookies", "Terms"])
        ]
        for i, (header, links) in enumerate(links_data):
            col = i + 1
            tk.Label(footer_frame, text=header, font=("Arial", 10, "bold"), bg=COLOR_HEADER_FOOTER).grid(row=0, column=col, sticky="nw", padx=20)
            for j, link in enumerate(links):
                tk.Label(footer_frame, text=link, font=("Arial", 9), fg="gray", bg=COLOR_HEADER_FOOTER).grid(row=j+1, column=col, sticky="nw", padx=20, pady=2)

        # Cột Social
        for i in range(5):
             footer_frame.grid_columnconfigure(i, weight=0)

        footer_frame.grid_columnconfigure(5, weight=1)
        social_frame = tk.Frame(footer_frame, bg=COLOR_HEADER_FOOTER)
        social_frame = tk.Frame(footer_frame, bg=COLOR_HEADER_FOOTER)
        social_frame.grid(row=0, column=5, rowspan=5, sticky="ne", padx=(0, 50))
        tk.Label(social_frame, text="Follow us", font=("Arial", 10, "bold"), bg=COLOR_HEADER_FOOTER).pack(anchor="e")
        
        icons_row = tk.Frame(social_frame, bg=COLOR_HEADER_FOOTER)
        icons_row.pack(anchor="e", pady=5)
        for key in ['fb', 'ins', 'li', 'x']:
            if self.icons[key]: 
                tk.Label(icons_row, image=self.icons[key], bg=COLOR_HEADER_FOOTER).pack(side="left", padx=2)
            else: 
                tk.Label(icons_row, text="[x]", bg=COLOR_HEADER_FOOTER).pack(side="left")

        tk.Label(social_frame, text="Subscribe to newsletter", font=("Arial", 10, "bold"), bg=COLOR_HEADER_FOOTER).pack(anchor="e", pady=(20, 5))
        sub_box = tk.Frame(social_frame, bg=COLOR_HEADER_FOOTER, bd=1, relief="solid")
        sub_box.pack(anchor="e")
        tk.Entry(sub_box, width=20, bd=0).pack(side="left", padx=5)
        tk.Button(sub_box, text="→", bg=COLOR_BLUE_BTN, fg="white", bd=0).pack(side="left")

    # ---------------------------------------------------------
    # LOGIC CHAT
    # ---------------------------------------------------------
    def send_message(self):
        msg = self.entry.get()
        if not msg.strip(): return
        
        self.add_message_to_chat("user", msg)
        self.entry.delete(0, "end")

        if self.controller:
            self.controller.process_input(msg)
        else:
            self.show_loading()
            self.after(2000, lambda: [self.hide_loading(), self.add_message_to_chat("bot", "Đây là phản hồi mẫu.")])

    def add_message_to_chat(self, sender, text):
        # Frame chứa 1 dòng tin nhắn
        row_frame = tk.Frame(self.messages_area, bg=COLOR_CHAT_BG)
        row_frame.pack(fill="x", pady=10, padx=20) 

        if sender == "bot":
            if self.bot_avatar_tk:
                tk.Label(row_frame, image=self.bot_avatar_tk, bg=COLOR_CHAT_BG).pack(side="left", anchor="n")
            else:
                tk.Label(row_frame, text="AI", font=("Arial", 8, "bold"), bg=COLOR_GREEN_BTN, fg="white", width=4, height=2).pack(side="left", anchor="n")

            tk.Label(row_frame, text=text, font=FONT_CHAT, bg=COLOR_BOT_BUBBLE, fg="black", 
                     wraplength=400, justify="left", padx=15, pady=10).pack(side="left", padx=(10, 0))
        else:
            tk.Label(row_frame, text=text, font=FONT_CHAT, bg=COLOR_USER_BUBBLE, fg="white", 
                     wraplength=400, justify="left", padx=15, pady=10).pack(side="right")

        self.scroll_msg_to_bottom()

    def show_loading(self):
        if self.loading_indicator: return
        self.send_btn.config(state="disabled")

        self.loading_container = tk.Frame(self.messages_area, bg=COLOR_CHAT_BG)
        self.loading_container.pack(fill="x", pady=10, padx=20, anchor="w")

        if self.bot_avatar_tk:
            tk.Label(self.loading_container, image=self.bot_avatar_tk, bg=COLOR_CHAT_BG).pack(side="left", anchor="n")
        else:
            tk.Label(self.loading_container, text="AI", font=("Arial", 8, "bold"), bg=COLOR_GREEN_BTN, fg="white", width=4, height=2).pack(side="left", anchor="n")

        wrapper = tk.Frame(self.loading_container, bg=COLOR_BOT_BUBBLE, padx=10, pady=5)
        wrapper.pack(side="left", padx=(10, 0))
        self.loading_indicator = LoadingBubble(wrapper)
        self.loading_indicator.pack()
        self.scroll_msg_to_bottom()

    def hide_loading(self):
        if self.loading_indicator:
            self.loading_indicator.stop()
            self.loading_indicator = None
            if hasattr(self, 'loading_container'):
                self.loading_container.destroy()
        self.send_btn.config(state="normal")

    def scroll_msg_to_bottom(self):
        self.messages_area.update_idletasks()
        self.msg_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()