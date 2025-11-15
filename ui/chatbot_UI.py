import customtkinter as ctk

# Thiết lập giao diện chung
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue")  

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("UC Bot")
        self.geometry("400x600")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- 1. Header Frame ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Bạn có thể thêm logo UC Bot ở đây 
        # self.logo = ctk.CTkImage(...) 
        # self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo, text="")
        # self.logo_label.pack()

        self.bot_name_label = ctk.CTkLabel(
            self.header_frame, 
            text="UC Bot", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.bot_name_label.pack()

        # Đường kẻ ngang
        self.divider = ctk.CTkFrame(self, height=1, fg_color="gray")
        self.divider.grid(row=0, column=0, sticky="sew", padx=10, pady=(35, 0))


        # --- 2. Khung Chat  ---
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- 3. Khung Nhập Text ---
        self.input_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Type your message..."
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry.bind("<Return>", self.send_message) # Gửi khi nhấn Enter

        self.send_button = ctk.CTkButton(
            self.input_frame, 
            text="Send", 
            fg_color="#1F3AB0",
            text_color="white",
            width=50,
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1)

        # --- Hiển thị tin nhắn chào mừng ---
        self.show_welcome_message()

    def show_welcome_message(self):
        welcome_text = "Hey, I'm UC Bot (Beta)! University search feeling like 'too many tabs open'? I'll streamline that. Let me help you discover top universities, suggest suitable programmes, and even connect you with counsellors or student ambassadors ready to share real experiences and tips! What do you need today?"
        
        # Thêm tin nhắn của bot vào khung chat
        self.add_message_to_chat("bot", welcome_text)

        # Tạo khung chứa các nút gợi ý
        self.suggestion_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.suggestion_frame.pack(anchor="w", fill="x", padx=10)

        # Các nút gợi ý
        btn1 = ctk.CTkButton(
            self.suggestion_frame, 
            text="Find a university match",
            fg_color="white", # Màu nền
            text_color="#1F3AB0", # Màu chữ
            border_color="#1F3AB0", # Màu viền
            border_width=1,
            hover_color="#E0E7FF",
            command=lambda: self.handle_suggestion("Find a university match")
        )
        btn1.pack(fill="x", pady=2)

        btn2 = ctk.CTkButton(
            self.suggestion_frame, 
            text="Chat with a student ambassador",
            fg_color="white",
            text_color="#1F3AB0",
            border_color="#1F3AB0",
            border_width=1,
            hover_color="#E0E7FF",
            command=lambda: self.handle_suggestion("Chat with a student ambassador")
        )
        btn2.pack(fill="x", pady=2)

        btn3 = ctk.CTkButton(
            self.suggestion_frame, 
            text="Get free counselling",
            fg_color="white",
            text_color="#1F3AB0",
            border_color="#1F3AB0",
            border_width=1,
            hover_color="#E0E7FF",
            command=lambda: self.handle_suggestion("Get free counselling")
        )
        btn3.pack(fill="x", pady=2)

    def handle_suggestion(self, choice):
        # 1. Thêm tin nhắn (lựa chọn của user) vào chat
        self.add_message_to_chat("user", choice)
        
        # 2. Xóa các nút gợi ý
        self.suggestion_frame.destroy()
        
        # 3. Lấy phản hồi từ bot (Đây là nơi gọi API Gemini)
        self.get_bot_response(choice)

    def send_message(self, event=None):
        user_input = self.entry.get()
        if user_input.strip() == "":
            return

        # 1. Thêm tin nhắn của user vào chat
        self.add_message_to_chat("user", user_input)
        
        # 2. Xóa nội dung trong ô nhập liệu
        self.entry.delete(0, "end")
        
        # 3. (Nếu có) Xóa các nút gợi ý nếu user tự gõ
        if hasattr(self, 'suggestion_frame') and self.suggestion_frame.winfo_exists():
            self.suggestion_frame.destroy()

        # 4. Lấy phản hồi từ bot 
        self.get_bot_response(user_input)

    def get_bot_response(self, user_input):
        
        # Giả lập phản hồi của bot
        
        response = f"Ok, let's talk about: '{user_input}'. (This is a simulated response)."
        
        # Thêm phản hồi của bot vào chat
        self.add_message_to_chat("bot", response)

    def add_message_to_chat(self, sender, message):
        if sender == "bot":
            # Tin nhắn của bot (bên trái)
            fg_color = "#F0F0F0"
            text_color = "#111111"
            anchor = "w" # (West)
        else:
            # Tin nhắn của user (bên phải)
            fg_color = "#1F3AB0" 
            text_color = "#FFFFFF" 
            anchor = "e" # (East)

        # Tạo một label cho tin nhắn
        msg_label = ctk.CTkLabel(
            self.chat_frame,
            text=message,
            fg_color=fg_color,
            text_color=text_color,
            corner_radius=10,
            wraplength=300, # Tự động xuống hàng
            justify="left" if sender == "bot" else "right",
            padx=10,
            pady=5
        )
        
        # Dùng pack để căn lề trái/phải
        msg_label.pack(anchor=anchor, pady=5, padx=10)
        
        # Tự động cuộn xuống dưới cùng
        self.after(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        # Hàm này đảm bảo khung chat luôn cuộn xuống tin nhắn mới nhất
        self.chat_frame._parent_canvas.yview_moveto(1.0)


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()