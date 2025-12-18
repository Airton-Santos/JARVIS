# core/brain.py
from core.pesquisa import pesquisar_resumido
from core.ai import bode_responder
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.auth import FenixAuth
import sys, os, asyncio
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame
import pyautogui 

init(autoreset=True)
pygame.mixer.init()

# ------------------- Funções de Voz -------------------
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

# ------------------- Brain (Fênix) -------------------
class FenixBrain:
    def __init__(self, nome_usuario="Senhor"):
        self.nome_ia = "Fênix"
        self.nome_projeto = "FENIX"
        self.nome_usuario = nome_usuario
        
        self.cfg = ConfigAudio()
        self.auth = FenixAuth()
        
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor = self.cfg.configurar_reconhecedor(self.reconhecedor)

    def start(self):
        if not self.auth.autenticar():
            return

        with sr.Microphone() as source:
            print(f"{Fore.YELLOW}Calibrando sensores acústicos...{Style.RESET_ALL}")
            self.reconhecedor.adjust_for_ambient_noise(source, duration=2)

        print(f"{Fore.RED}{self.nome_ia}:{Style.RESET_ALL} Standby Ativo.")
        falar(f"Núcleo {self.nome_projeto} online. Aguardando ativação.")

        while True:
            # 1. MODO STANDBY
            print(f"{Fore.CYAN}Aguardando ativação...{Style.RESET_ALL}", end="\r", flush=True)
            ativacao = capturar_voz(self.reconhecedor, timeout=None, phrase_limit=5)
            
            if ativacao and any(word.lower() in ativacao.lower() for word in self.cfg.WAKE_WORDS):
                falar(f"Sim {self.nome_usuario}, sistemas de voz ativos.")
                
                # 2. MODO CONVERSA ATIVA
                while True:
                    print(f"{Fore.GREEN}>>> ESCUTANDO COMANDO ATIVO... <<<{Style.RESET_ALL}")
                    comando = capturar_voz(self.reconhecedor, timeout=8, phrase_limit=10)

                    if not comando: break
                    comando = comando.lower()

                    print(f"{Fore.BLUE}[OUVIDO]: {comando}{Style.RESET_ALL}")

                    # --- GATILHOS DE SEGURANÇA ---
                    if any(cmd in comando for cmd in self.cfg.CMD_DESLIGAR):
                        falar("Desligando sistemas. Até logo.")
                        sys.exit()

                    elif any(cmd in comando for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                        falar("Comando de voz suspenso. Em standby.")
                        break

                    # --- IDENTIDADE DO CRIADOR (AIRTON/BAGRE) ---
                    elif any(q in comando for q in ["quem é você", "o que é você", "projeto fênix", "quem te criou", "seu desenvolvedor"]):
                        info = (
                            f"Eu sou o Fênix, Fluxo de Execução em Núcleo de Inteligência em X-Interface. "
                            f"Fui desenvolvido pelo Senhor Airton, conhecido por seus amigos como Bagre. "
                            f"Ele me criou em prol da automação e da evolução tecnológica."
                        )
                        falar(info)

                    # --- FUNÇÃO DE ESCRITA (DITADO) ---
                    elif any(cmd in comando for cmd in self.cfg.CMD_ATIVAR_ESCRITA):
                        falar("Modo de escrita habilitado. Diga seu texto.")
                        print(f"{Fore.MAGENTA}>>> MODO ESCRITA ATIVO: DIGITANDO... <<<{Style.RESET_ALL}")
                        
                        while True:
                            ditado = capturar_voz(self.reconhecedor, timeout=None, phrase_limit=15)
                            if not ditado: continue
                            
                            processado = ditado.lower().strip()

                            # VERIFICAÇÃO DE SAÍDA: Bloqueia a digitação se o comando for de desativar
                            if "desativar escrita" in processado or "encerrar escrita" in processado or "parar escrita" in processado:
                                falar("Protocolo de escrita encerrado. Voltando aos comandos.")
                                print(f"{Fore.CYAN}>>> MODO COMANDO REATIVADO <<<{Style.RESET_ALL}")
                                break
                            
                            # Digita o texto apenas se não for o comando de saída
                            pyautogui.write(ditado + " ", interval=0.01)
                            print(f"{Fore.YELLOW}Escrito:{Style.RESET_ALL} {ditado}")

                    # --- LÓGICA DE PESQUISA ---
                    elif "pesquisar" in comando:
                        termo = comando.replace("pesquisar", "").strip()
                        if termo:
                            res = pesquisar_resumido(termo)
                            falar(res['resumo'])
                    
                    # --- RESPOSTA DA IA ---
                    else:
                        resposta = bode_responder(comando)
                        falar(resposta)