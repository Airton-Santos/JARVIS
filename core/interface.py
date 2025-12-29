import customtkinter as ctk
import psutil
import time
import threading

class FenixUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO MESTRE ---
        self.title("PROJECT FENIX - CORE SYSTEM")
        self.geometry("1100x700") # Aumentei um pouco a largura para caber a nova aba
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#0a0a0a") 

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
        # Frame de Agrupamento Central
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.center_frame.grid_columnconfigure(0, weight=1) # Console
        self.center_frame.grid_columnconfigure(1, weight=0) # Nova Aba
        self.center_frame.grid_rowconfigure(0, weight=1)

        # --- COLUNA 0: TERMINAL ---
        self.terminal_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.terminal_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.console_title = ctk.CTkLabel(self.terminal_frame, text="TERMINAL DE EXECUÇÃO", font=("Consolas", 14, "bold"), text_color="#00fbff")
        self.console_title.pack(anchor="w", pady=(0, 10))

        self.textbox = ctk.CTkTextbox(self.terminal_frame, fg_color="#050505", border_color="#1f1f1f", border_width=1, 
                                     text_color="#00fbff", font=("Consolas", 13), corner_radius=10)
        self.textbox.pack(expand=True, fill="both")

        # --- COLUNA 1: ABA DE MONITORAMENTO (NOVA) ---
        self.monitor_frame = ctk.CTkFrame(self.center_frame, width=250, fg_color="#111111", border_width=1, border_color="#1f1f1f")
        self.monitor_frame.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(self.monitor_frame, text="MONITORAMENTO", font=("Orbitron", 14, "bold"), text_color="#00fbff").pack(pady=20, padx=20)
        
        # Lista de funções para o senhor visualizar
        funcoes = [
            ("LISTA DE PROCESSOS", "Gerencia RAM e CPU"),
            ("SAÚDE DO HARDWARE", "Sensores de sistema"),
            ("LIMPEZA TEMPORÁRIA", "Otimização de disco"),
            ("ANALISAR REDE", "Tráfego de internet"),
            ("ENCERRAR PROGRAMA", "Finalizar processos")
        ]

        for nome, desc in funcoes:
            f_button = ctk.CTkFrame(self.monitor_frame, fg_color="#1a1a1a", corner_radius=5, height=60)
            f_button.pack(fill="x", padx=15, pady=8)
            f_button.pack_propagate(False)
            
            ctk.CTkLabel(f_button, text=nome, font=("Consolas", 11, "bold"), text_color="#00fbff").pack(anchor="w", padx=10, pady=(5,0))
            ctk.CTkLabel(f_button, text=desc, font=("Consolas", 9), text_color="#005555").pack(anchor="w", padx=10)

        self.log_msg("Inicializando protocolos Fenix...")
        self.log_msg("Interface de monitoramento carregada.")

    def create_menu_button(self, text, color, command):
        return ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", border_width=1, border_color=color,
                            text_color=color, hover_color="#0a2a2a", font=("Consolas", 12, "bold"), 
                            height=40, command=command)

    def log_msg(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.textbox.insert("end", f"[{timestamp}] > {msg}\n")
        self.textbox.see("end")

    def update_metrics(self):
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        self.ram_bar.set(ram / 100)
        self.ram_label.configure(text=f"MEMORY USAGE: {ram}%")
        self.cpu_bar.set(cpu / 100)
        self.cpu_label.configure(text=f"CPU LOAD: {cpu}%")
        self.after(2000, self.update_metrics)

    def toggle_system(self):
        self.log_msg("Alterando estado do microfone...")

    def mudar_status(self, status, cor):
        self.status_led.configure(text=f"● {status}", text_color=cor)

if __name__ == "__main__":
    app = FenixUI()
    app.mainloop()