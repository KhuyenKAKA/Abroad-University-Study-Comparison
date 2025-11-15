import tkinter as tk
from tkinter import scrolledtext

class ChatbotUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("University Comparison - Chatbot")
        self.master.geometry("500x600")
        self.master.configure(bg="#F2F2F2")

        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.master, text="Chatbot Hỗ Trợ Tư Vấn Du Học", font=("Arial", 16, "bold"), bg="#F2F2F2").pack(pady=10)

        # Chat display box
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_display.configure(state='disabled')

        # Frame bottom
        bottom_frame = tk.Frame(self.master, bg="#F2F2F2")
        bottom_frame.pack(pady=10, fill=tk.X)

        # Entry box
        self.entry = tk.Entry(bottom_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        send_btn = tk.Button(bottom_frame, text="Gửi", command=self.send_message, font=("Arial", 12), bg="#4CAF50", fg="white")
        send_btn.pack(side=tk.RIGHT, padx=5)

    def send_message(self, event=None):
        user_msg = self.entry.get().strip()
        if user_msg == "":
            return

        # Display user message
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"Bạn: {user_msg}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

        # Bot response
        bot_reply = "abc xyz"  # Replace with actual chatbot logic

        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"Chatbot: {bot_reply}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

        self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()
