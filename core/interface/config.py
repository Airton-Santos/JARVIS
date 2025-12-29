import customtkinter as ctk

class ConfigTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        self.label = ctk.CTkLabel(self, text="PROTOCOLOS DE CONFIGURAÇÃO", 
                                 font=("Orbitron", 18, "bold"), text_color="#00fbff")
        self.label.pack(pady=30)

        # --- CONTROLE DE VOLUME ---
        self.vol_label = ctk.CTkLabel(self, text="VOLUME DO SISTEMA", font=("Consolas", 13), text_color="#00fbff")
        self.vol_label.pack(pady=(10, 5))
        
        self.vol_slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=100, button_color="#00fbff", progress_color="#00fbff")
        self.vol_slider.set(0.8) # Padrão 80%
        self.vol_slider.pack(pady=10, padx=80, fill="x")

        # --- SENSIBILIDADE DO MICROFONE ---
        self.mic_label = ctk.CTkLabel(self, text="SENSIBILIDADE DO MICROFONE", font=("Consolas", 13), text_color="#00fbff")
        self.mic_label.pack(pady=(30, 5))
        
        self.mic_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=20, button_color="#00fbff", progress_color="#00fbff")
        self.mic_slider.set(50) # Padrão Médio
        self.mic_slider.pack(pady=10, padx=80, fill="x")

        self.info_label = ctk.CTkLabel(self, text="Ajuste os parâmetros para otimizar a resposta da Feni.", 
                                      font=("Consolas", 10), text_color="#005555")
        self.info_label.pack(pady=40)