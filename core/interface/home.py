import customtkinter as ctk
import time

class HomeTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Aba Console (estilo antigo)
        self.textbox = ctk.CTkTextbox(self, fg_color="#050505", border_color="#1f1f1f", 
                                     border_width=1, text_color="#00fbff", font=("Consolas", 13))
        self.textbox.pack(expand=True, fill="both", padx=10, pady=10)

    def log_msg(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.textbox.insert("end", f"[{timestamp}] > {msg}\n")
        self.textbox.see("end")