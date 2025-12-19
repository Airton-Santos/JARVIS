from core.pesquisa import pesquisar_resumido
from core.ai import bode_responder
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
# from core.auth import FenixAuth # Remova o comentário se for usar autenticação
import sys, os, asyncio
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame
import pyautogui 
import threading

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
    def __init__(self, interface=None, nome_usuario="Senhor"):
        self.nome_ia = "Fênix"
        self.nome_projeto = "FENIX"
        self.nome_usuario = nome_usuario
        self.interface = interface # Conexão com a UI
        self.cfg = ConfigAudio()
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor = self.cfg.configurar_reconhecedor(self.reconhecedor)

    def log(self, mensagem, cor=Fore.WHITE):
        print(f"{cor}{mensagem}{Style.RESET_ALL}")
        if self.interface:
            self.interface.log_msg(mensagem)

    def start(self):
        # Calibragem
        self.log("Calibrando sensores acústicos...", Fore.YELLOW)
        with sr.Microphone() as source:
            self.reconhecedor.adjust_for_ambient_noise(source, duration=2)

        self.log(f"Núcleo {self.nome_projeto} online.", Fore.RED)
        falar(f"Núcleo {self.nome_projeto} online. Bem-vindo, {self.nome_usuario}.")

        while True:
            if self.interface: self.interface.mudar_status("STANDBY", "#005555")
            
            ativacao = capturar_voz(self.reconhecedor, timeout=None, phrase_limit=5)
            
            if ativacao and any(word.lower() in ativacao.lower() for word in self.cfg.WAKE_WORDS):
                if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                falar(f"Sim {self.nome_usuario}.")
                
                while True:
                    comando = capturar_voz(self.reconhecedor, timeout=8, phrase_limit=10)
                    if not comando: break
                    
                    comando = comando.lower().strip()
                    self.log(f"[OUVIDO]: {comando}", Fore.BLUE)

                    if any(cmd in comando for cmd in self.cfg.CMD_DESLIGAR):
                        falar("Desligando sistemas.")
                        sys.exit()

                    elif any(cmd in comando for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                        falar("Em standby.")
                        break

                    elif "pesquisar" in comando:
                        termo = comando.replace("pesquisar", "").strip()
                        falar(f"Pesquisando {termo}")
                        res = pesquisar_resumido(termo)
                        falar(res['resumo'])
                    
                    else:
                        resposta = bode_responder(comando)
                        falar(resposta)
                        self.log(f"Fênix: {resposta}", Fore.GREEN)