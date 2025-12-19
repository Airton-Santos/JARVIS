import customtkinter as ctk
import psutil
import time
import threading

class FenixUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO MESTRE ---
        self.title("PROJECT FENIX - CORE SYSTEM")
        self.geometry("1000x650")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#0a0a0a") # Preto quase puro

        # Grid Layout (Coluna 0: Menu, Coluna 1: Conteúdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_console()
        
        # Iniciar Telemetria
        self.update_metrics()

    def setup_sidebar(self):
        # Painel Lateral
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#111111", border_width=1, border_color="#1f1f1f")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Logo/Nome
        self.logo_label = ctk.CTkLabel(self.sidebar, text="FÊENIX", font=("Orbitron", 35, "bold"), text_color="#00fbff")
        self.logo_label.pack(pady=(30, 10))
        
        self.sub_label = ctk.CTkLabel(self.sidebar, text="NÚCLEO DE INTELIGÊNCIA", font=("Consolas", 10), text_color="#005555")
        self.sub_label.pack(pady=(0, 30))

        # --- TELEMETRIA (AZUL) ---
        self.ram_label = ctk.CTkLabel(self.sidebar, text="MEMORY USAGE: 0%", font=("Consolas", 12), text_color="#00fbff")
        self.ram_label.pack(pady=(20, 5))
        self.ram_bar = ctk.CTkProgressBar(self.sidebar, width=200, height=8, progress_color="#00fbff", fg_color="#051a1a")
        self.ram_bar.set(0)
        self.ram_bar.pack()

        self.cpu_label = ctk.CTkLabel(self.sidebar, text="CPU LOAD: 0%", font=("Consolas", 12), text_color="#00fbff")
        self.cpu_label.pack(pady=(20, 5))
        self.cpu_bar = ctk.CTkProgressBar(self.sidebar, width=200, height=8, progress_color="#00fbff", fg_color="#051a1a")
        self.cpu_bar.set(0)
        self.cpu_bar.pack()

        # --- BOTÕES DE COMANDO ---
        self.btn_power = self.create_menu_button("SISTEMA ON", "#00fbff", self.toggle_system)
        self.btn_power.pack(pady=(50, 10), padx=20)
        
        self.btn_reset = self.create_menu_button("REINICIAR NÚCLEO", "#00fbff", None)
        self.btn_reset.pack(pady=10, padx=20)

        # Indicador de Status inferior
        self.status_led = ctk.CTkLabel(self.sidebar, text="● SYSTEM READY", text_color="#00fbff", font=("Consolas", 11))
        self.status_led.pack(side="bottom", pady=20)

    def setup_main_console(self):
        # Console Central
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.console_title = ctk.CTkLabel(self.main_container, text="TERMINAL DE EXECUÇÃO", font=("Consolas", 14, "bold"), text_color="#00fbff")
        self.console_title.pack(anchor="w", pady=(0, 10))

        self.textbox = ctk.CTkTextbox(self.main_container, fg_color="#050505", border_color="#1f1f1f", border_width=1, 
                                     text_color="#00fbff", font=("Consolas", 13), corner_radius=10)
        self.textbox.pack(expand=True, fill="both")
        
        self.log_msg("Inicializando protocolos Fenix...")
        self.log_msg("Aguardando comando do usuário...")

    def create_menu_button(self, text, color, command):
        return ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", border_width=1, border_color=color,
                            text_color=color, hover_color="#0a2a2a", font=("Consolas", 12, "bold"), 
                            height=40, command=command)

    def log_msg(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.textbox.insert("end", f"[{timestamp}] > {msg}\n")
        self.textbox.see("end")

    def update_metrics(self):
        # Atualiza RAM e CPU
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        
        self.ram_bar.set(ram / 100)
        self.ram_label.configure(text=f"MEMORY USAGE: {ram}%")
        
        self.cpu_bar.set(cpu / 100)
        self.cpu_label.configure(text=f"CPU LOAD: {cpu}%")
        
        self.after(2000, self.update_metrics)

    def toggle_system(self):
        self.log_msg("Alterando estado do microfone...")
        # Lógica para ligar o Brain entrará aqui

    def mudar_status(self, status, cor):
        self.status_led.configure(text=f"● {status}", text_color=cor)

if __name__ == "__main__":
    app = FenixUI()
    app.mainloop()