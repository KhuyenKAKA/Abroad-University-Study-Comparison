import customtkinter as ctk
import sys
import os
from PIL import Image, ImageDraw, ImageOps

current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)             
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from controller.ChatbotController import ChatbotController
except ImportError:
    ChatbotController = None

THEME_COLOR = "#2563EB"  
HOVER_COLOR = "#1D4ED8" 
BG_COLOR = "#FFFFFF"    
CHAT_BG = "#F3F4F6"     
BOT_BUBBLE = "#E5E7EB"   
USER_BUBBLE = THEME_COLOR 
TEXT_COLOR_MAIN = "#1F2937" 
FONT_MAIN = ("Segoe UI", 14)
FONT_BOLD = ("Segoe UI", 14, "bold")

class LoadingBubble(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.bubble = ctk.CTkFrame(self, fg_color=BOT_BUBBLE, corner_radius=20)
        self.bubble.pack(anchor="w", padx=10, pady=5)
        
        self.dots = []
        for i in range(3):
            dot = ctk.CTkLabel(
                self.bubble, 
                text="•", 
                font=("Arial", 30), 
                text_color="#9CA3AF", 
                width=15
            )
            dot.pack(side="left", padx=2, pady=(0, 5))
            self.dots.append(dot)
            
        self.running = True
        self.animate(0)

    def animate(self, step):
        if not self.running: return
        for i, dot in enumerate(self.dots):
            if i == step % 3:
                dot.configure(text_color="#4B5563") 
            else:
                dot.configure(text_color="#9CA3AF") 
        self.after(250, lambda: self.animate(step + 1))

    def stop(self):
        self.running = False
        self.destroy()

ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue") 

class ChatApp(ctk.CTk):
    def create_circular_avatar(self, image_path, output_size=(100, 100)):
        """
        Hàm này nhận đường dẫn ảnh, cắt thành hình vuông ở giữa,
        sau đó bo tròn và trả về đối tượng PIL Image.
        """
        try:
            img = Image.open(image_path)
            img = ImageOps.fit(img, output_size, centering=(0.5, 0.5))

            mask = Image.new('L', output_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + output_size, fill=255)

            circular_img = img.convert("RGBA")
            circular_img.putalpha(mask)

            return circular_img

        except Exception as e:
            print(f"Lỗi xử lý ảnh tròn: {e}")
            return None
        
    def __init__(self):
        super().__init__()

        image_path = os.path.join(project_root, "assets", "bot_avatar.jpg")
        processed_pil_image = self.create_circular_avatar(image_path, output_size=(100, 100))

        if processed_pil_image:
            self.bot_avatar_img = ctk.CTkImage(
                light_image=processed_pil_image,
                dark_image=processed_pil_image,
                size=(35, 35) 
            )
            print("Đã load và xử lý avatar thành công.")
        else:
            print(f"⚠️ Không thể load ảnh tại: {image_path}. Sử dụng avatar mặc định.")
            self.bot_avatar_img = None

        self.title("UC Bot - Trợ lý du học")
        self.geometry("420x650") 
        self.configure(fg_color=BG_COLOR) 

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=THEME_COLOR, height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="UC Bot Support", 
            font=("Segoe UI", 18, "bold"), 
            text_color="white"
        )
        self.title_label.pack(pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            self.header_frame, 
            text="● Online", 
            font=("Segoe UI", 12), 
            text_color="#86EFAC" 
        )
        self.status_label.pack(pady=(0, 10))

        self.chat_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color=CHAT_BG,
            corner_radius=0
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew")

        self.input_frame = ctk.CTkFrame(self, fg_color="white", height=80)
        self.input_frame.grid(row=2, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        separator = ctk.CTkFrame(self.input_frame, height=1, fg_color="#E5E7EB")
        separator.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.entry_field = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Nhập câu hỏi của bạn...", 
            height=50, 
            corner_radius=25,
            border_width=1,
            border_color="#D1D5DB",
            fg_color="#F9FAFB",
            font=FONT_MAIN
        )
        self.entry_field.grid(row=1, column=0, sticky="ew", padx=(15, 10), pady=15)
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(
            self.input_frame, 
            text="➤",
            width=50, 
            height=50, 
            corner_radius=25, 
            fg_color=THEME_COLOR, 
            hover_color=HOVER_COLOR,
            font=("Arial", 20),
            command=self.send_message
        )
        self.send_button.grid(row=1, column=1, padx=(0, 15))

        self.loading_indicator = None 
        if ChatbotController:
            try:
                self.controller = ChatbotController(self)
                self.add_message_to_chat("bot", "Xin chào! 👋\nMình là UC Bot. Mình có thể giúp gì cho kế hoạch du học của bạn?")
            except Exception as e:
                self.add_message_to_chat("bot", f"Lỗi khởi động: {e}")
                self.controller = None
        else:
            self.controller = None
            self.add_message_to_chat("bot", "Chế độ Giao diện (Không có Controller).")

    def send_message(self):
        user_input = self.entry_field.get()
        if user_input.strip() == "": return

        self.add_message_to_chat("user", user_input)
        self.entry_field.delete(0, "end")

        if self.controller:
            self.controller.process_input(user_input)
        else:
            self.show_loading()
            self.after(1500, lambda: [self.hide_loading(), self.add_message_to_chat("bot", "Đây là tin nhắn mẫu trả lời cho giao diện đẹp hơn!")])

    def add_message_to_chat(self, sender, message):
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        
        if sender == "bot":
            msg_container.pack(anchor="w", pady=5, padx=10, fill="x")
            
            if self.bot_avatar_img:
                avatar = ctk.CTkLabel(
                    msg_container, 
                    text="", 
                    image=self.bot_avatar_img,
                    width=35, height=35
                )
            else:
                avatar = ctk.CTkButton(
                    msg_container, text="AI", width=36, height=36, corner_radius=18,
                    fg_color="#10B981", hover=False, state="disabled", text_color="white"
                )
            # -----------------------
            
            avatar.pack(side="left", anchor="n")
            
            bubble = ctk.CTkLabel(
                msg_container, 
                text=message, 
                fg_color=BOT_BUBBLE, 
                text_color=TEXT_COLOR_MAIN,
                corner_radius=18, 
                wraplength=260, 
                justify="left", 
                padx=15, pady=12, 
                font=FONT_MAIN
            )
            bubble.pack(side="left", padx=(10, 0))

        else:
            msg_container.pack(anchor="e", pady=5, padx=10, fill="x")
            bubble = ctk.CTkLabel(
                msg_container, 
                text=message, 
                fg_color=USER_BUBBLE, 
                text_color="white",
                corner_radius=18, 
                wraplength=260, 
                justify="left", 
                padx=15, pady=12, 
                font=FONT_MAIN
            )
            bubble.pack(side="right")

        self.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def show_loading(self):
        if self.loading_indicator: return
        self.send_button.configure(state="disabled")
        
        self.loading_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.loading_container.pack(anchor="w", pady=5, padx=10, fill="x")
        
        if self.bot_avatar_img:
            avatar = ctk.CTkLabel(
                self.loading_container, text="", image=self.bot_avatar_img, width=35, height=35
            )
        else:
            avatar = ctk.CTkButton(
                self.loading_container, text="AI", width=36, height=36, corner_radius=18,
                fg_color="#10B981", hover=False, state="disabled", text_color="white"
            )
        avatar.pack(side="left", anchor="n")
        # --------------------------

        self.loading_indicator = LoadingBubble(self.loading_container)
        self.loading_indicator.pack(side="left", padx=(5, 0))
        
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def hide_loading(self):
        if self.loading_indicator:
            self.loading_indicator.stop()
            self.loading_indicator = None
            if hasattr(self, 'loading_container'):
                self.loading_container.destroy()
        
        self.send_button.configure(state="normal")

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()