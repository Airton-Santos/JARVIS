# core/brain.py
from core.pesquisa import pesquisar_resumido
from core.ai import bode_responder
import sys, time, os
from colorama import Fore, Style, init
import msvcrt

init(autoreset=True)

USUARIO_AUTORIZADO = os.getenv("JARVIS_USER", "bagre")
SENHA_AUTORIZADA = os.getenv("JARVIS_PASS", "1234")

# ------------------- Funções de autenticação -------------------
def input_senha(prompt="Senha: "):
    senha = ""
    print(prompt, end="", flush=True)
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print()
            break
        elif ch == b'\x08':
            if len(senha) > 0:
                senha = senha[:-1]
                print("\b \b", end="", flush=True)
        else:
            senha += ch.decode()
            print("*", end="", flush=True)
    return senha

def autenticar_usuario():
    print(f"{Fore.RED}=== AUTENTICAÇÃO JARVIS ==={Style.RESET_ALL}")
    usuario = input("Usuário: ").strip()
    senha = input_senha("Senha: ")

    if usuario == USUARIO_AUTORIZADO and senha == SENHA_AUTORIZADA:
        print(f"{Fore.GREEN}Acesso autorizado!{Style.RESET_ALL}\n")
        return True
    else:
        print(f"{Fore.RED}Acesso negado!{Style.RESET_ALL}")
        return False

# ------------------- Brain -------------------
class JarvisBrain:
    def __init__(self, nome_usuario="Senhor"):
        self.nome_usuario = nome_usuario
        self.funcoes = {
            "pesquisar": "Pesquisa algo e retorna resumo + links",
            "status": "Mostra status do sistema",
            "listar funcoes": "Lista todas as funções disponíveis",
            "sair": "Desliga o JARVIS"
        }

    def listar_funcoes(self):
        print("Funções disponíveis:")
        for key, desc in self.funcoes.items():
            print(f"- {key}: {desc}")

    def start(self):
        if not autenticar_usuario():
            return

        print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} Olá, {self.nome_usuario}. Eu sou o JARVIS.")
        print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} Sistema online e pronto.\n")

        while True:
            comando = input("O que deseja fazer? ").strip()

            if comando.lower() == "sair":
                print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} Desligando o sistema. Até mais!")
                break

            elif comando.lower() == "status":
                print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} Todos os sistemas funcionando normalmente.")

            elif comando.lower() == "listar funcoes":
                self.listar_funcoes()

            elif "pesquisar" in comando.lower():
                termo = comando.lower().replace("pesquisar", "").strip()
                if termo == "":
                    termo = input(f"{Fore.RED}JARVIS:{Style.RESET_ALL} O que deseja pesquisar? ").strip()

                resultados = pesquisar_resumido(termo)
                print(f"\n{Fore.RED}JARVIS:{Style.RESET_ALL} Aqui está o que encontrei sobre '{termo}':\n")
                print(f"Resumo: {resultados['resumo']}\n")
                print(f"Fonte principal: {resultados['fonte']}\n")
                if resultados["outros_links"]:
                    print("Outros links:")
                    for link in resultados["outros_links"]:
                        print(f"- {link}")
                print()
            else:
                # Qualquer outro texto vai para a IA Bode
                print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} Pensando...")
                resposta = bode_responder(comando)
                print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} {resposta}\n")
