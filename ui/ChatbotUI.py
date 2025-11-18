import customtkinter as ctk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)             
if project_root not in sys.path:
    sys.path.append(project_root)

from controller.ChatbotController import ChatbotController

class LoadingBubble(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Bong bóng màu xám
        self.bubble = ctk.CTkFrame(self, fg_color="#E0E0E0", corner_radius=15)
        self.bubble.pack(anchor="w", padx=5, pady=5)
        
        # 3 dấu chấm
        self.dots = []
        for i in range(3):
            dot = ctk.CTkLabel(
                self.bubble, 
                text="•", 
                font=("Arial", 26), 
                text_color="#999999",
                width=10
            )
            dot.pack(side="left", padx=2, pady=0)
            self.dots.append(dot)
            
        self.running = True
        self.animate(0)

    def animate(self, step):
        if not self.running: return
        
        # Logic nhấp nháy: Làm đậm từng dấu chấm theo nhịp
        for i, dot in enumerate(self.dots):
            if i == step % 3:
                dot.configure(text_color="#333333") # Màu đậm
            else:
                dot.configure(text_color="#AAAAAA") # Màu nhạt

        # Lặp lại sau 300ms
        self.after(300, lambda: self.animate(step + 1))

    def stop(self):
        self.running = False
        self.destroy()

ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue")  

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("UC Bot - Tư vấn du học")
        self.geometry("400x550")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(self.header_frame, text="UC Bot", font=ctk.CTkFont(size=20, weight="bold")).pack()
        ctk.CTkFrame(self, height=2, fg_color="#E0E0E0").grid(row=0, column=0, sticky="ew", pady=(40, 0))

        # --- Chat Area ---
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Input Area ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=20)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry_field = ctk.CTkEntry(self.input_frame, placeholder_text="Hỏi thông tin trường...", height=45, corner_radius=22)
        self.entry_field.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.input_frame, text="Gửi", width=80, fg_color = "#1F3AB0",  height=45, corner_radius=22, command=self.send_message)
        self.send_button.grid(row=0, column=1)

        # --- Biến quản lý Loading ---
        self.loading_indicator = None 

        # --- Kết nối Controller ---
        if ChatbotController:
            try:
                self.controller = ChatbotController(self)
                self.add_message_to_chat("bot", "Xin chào! Mình là AI hỗ trợ tra cứu thông tin đại học. Bạn muốn tìm trường nào?")
            except Exception as e:
                self.add_message_to_chat("bot", f"Lỗi khởi động: {e}")
                self.controller = None
        else:
            self.controller = None
            self.add_message_to_chat("bot", "Lỗi: Không tìm thấy file Controller.")

    def send_message(self):
        user_input = self.entry_field.get()
        if user_input.strip() == "": return

        # Hiện tin nhắn User
        self.add_message_to_chat("user", user_input)
        self.entry_field.delete(0, "end")

        if self.controller:
            self.controller.process_input(user_input)
        else:
            self.add_message_to_chat("bot", "Lỗi kết nối Controller.")

    def add_message_to_chat(self, sender, message):
        if sender == "bot":
            fg_color = "#F2F2F2"
            text_color = "#111111"
            anchor = "w"
        else:
            fg_color = "#1F3AB0" 
            text_color = "#FFFFFF" 
            anchor = "e" 

        msg_label = ctk.CTkLabel(
            self.chat_frame, 
            text=message, 
            fg_color=fg_color, 
            text_color=text_color,
            corner_radius=16, 
            wraplength=280, 
            justify="left", 
            padx=15, 
            pady=10, 
            font=ctk.CTkFont(size=14)
        )
        msg_label.pack(anchor=anchor, pady=6, padx=5)
        
        # Auto scroll
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    # --- HIỆN HIỆU ỨNG LOADING (BONG BÓNG ĐỘNG) ---
    def show_loading(self):
        if self.loading_indicator: return
        
        self.send_button.configure(state="disabled")
        
        # Tạo bong bóng loading
        self.loading_indicator = LoadingBubble(self.chat_frame)
        self.loading_indicator.pack(anchor="w", pady=5, padx=5)
        
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    # --- ẨN HIỆU ỨNG ---
    def hide_loading(self):
        if self.loading_indicator:
            self.loading_indicator.stop()
            self.loading_indicator = None
        
        self.send_button.configure(state="normal")

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()