from core.ai import bode_responder
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.system import obter_processos_pesados, saude_hardware, limpar_temporarios, encerrar_processo
import sys, os, asyncio
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame

init(autoreset=True)
pygame.mixer.init()

async def falar_async(texto):
    voice = "pt-BR-AntonioNeural"
    output_file = "res.mp3"
    communicate = edge_tts.Communicate(texto, voice)
    await communicate.save(output_file)
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.01)
    pygame.mixer.music.unload()
    if os.path.exists(output_file):
        try: os.remove(output_file)
        except: pass

def falar(texto):
    asyncio.run(falar_async(texto))

class FenixBrain:
    def __init__(self, interface=None, nome_usuario="Fenix"):
        self.nome_ia = "Feni"
        self.nome_projeto = "FENIX"
        self.nome_usuario = nome_usuario
        self.interface = interface 
        self.cfg = ConfigAudio()
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor = self.cfg.configurar_reconhecedor(self.reconhecedor)

    def log(self, mensagem, cor=Fore.WHITE):
        print(f"{cor}{mensagem}{Style.RESET_ALL}")
        if self.interface:
            self.interface.log_msg(mensagem)

    def executar_diagnostico(self):
        """Fluxo direto: Pergunta e executa o que o senhor leu na interface"""
        self.log("Aguardando instrução de diagnóstico...", Fore.YELLOW)
        falar("O que o senhor deseja verificar no sistema?") # Pergunta curta e direta
        
        escolha = capturar_voz(self.reconhecedor, timeout=7).lower()
        
        if "processos" in escolha or "memória" in escolha:
            falar("Analisando processos.")
            falar(obter_processos_pesados())
            
        elif "saúde" in escolha or "hardware" in escolha:
            falar(saude_hardware())
            
        elif "limpeza" in escolha or "temporários" in escolha:
            falar("Iniciando limpeza.")
            falar(limpar_temporarios())
            
        elif "rede" in escolha or "conexão" in escolha:
            from core.system import analisar_conexoes
            falar(analisar_conexoes())
            
        else:
            falar("Entendido. Voltando para escuta passiva.")

    def start(self):
        self.log("Calibrando sensores acústicos...", Fore.YELLOW)
        with sr.Microphone() as source:
            self.reconhecedor.adjust_for_ambient_noise(source, duration=2)

        self.log(f"Núcleo {self.nome_projeto} online.", Fore.RED)
        falar(f"Sistema {self.nome_projeto} ativo. Às suas ordens, Senhor {self.nome_usuario}.")

        while True:
            if self.interface: self.interface.mudar_status("STANDBY", "#005555")
            
            ativacao = capturar_voz(self.reconhecedor, timeout=None, phrase_limit=5)
            
            if ativacao and any(word.lower() in ativacao.lower() for word in self.cfg.WAKE_WORDS):
                if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                falar(f"Sim Senhor.")
                
                while True:
                    comando = capturar_voz(self.reconhecedor, timeout=8, phrase_limit=10)
                    if not comando: break
                    
                    comando = comando.lower().strip()
                    self.log(f"[OUVIDO]: {comando}", Fore.BLUE)

                    # --- INTERCEPTOR DE COMANDOS DE SISTEMA (Ação Direta) ---
                    if any(cmd in comando for cmd in self.cfg.CMD_DESLIGAR):
                        falar("Desativando núcleo neural. Até logo, Senhor.")
                        sys.exit()

                    elif any(cmd in comando for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                        falar("Entrando em modo de espera.")
                        break

                    elif "verificar computador" in comando:
                        self.executar_diagnostico()

                    # --- NÚCLEO DE INTELIGÊNCIA ARTIFICIAL ---
                    else:
                        resposta = bode_responder(comando)
                        self.log(f"Fênix: {resposta}", Fore.GREEN)
                        falar(resposta)