from core.pesquisa import pesquisar_resumido
from core.ai import gpt_local_responder
import sys
import time
from colorama import Fore, Style, init

# Inicializa colorama para cores no terminal
init(autoreset=True)

def imprimir_com_loading(gerar_resposta_func, *args, **kwargs):
    """
    Mostra uma animação de 'Jarvis está respondendo' enquanto a resposta é gerada.
    """
    loading = ["|", "/", "-", "\\"]  # animação de círculo girando
    print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} ", end="")

    # Loop rápido do loading inicial
    for i in range(10):
        sys.stdout.write(loading[i % len(loading)])
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")

    # Gera a resposta real
    resposta = gerar_resposta_func(*args, **kwargs)

    # Limpa o loading e mostra a resposta final
    sys.stdout.write("\b")  # apaga o último caractere do loading
    print(f"{Fore.RED}JARVIS:{Style.RESET_ALL} {resposta}\n")
    return resposta

class JarvisBrain:
    def __init__(self, nome_usuario="Senhor"):
        self.nome_usuario = nome_usuario
        self.funcoes = {
            "pesquisar": "Pesquisa algo e retorna resumo + links",
            "status": "Mostra status do sistema",
            "listar funcoes": "Lista todas as funções disponíveis",
            "sair": "Desliga o JARVIS"
        }
        self.conversa = []

    def listar_funcoes(self):
        print("Funções disponíveis:")
        for key, desc in self.funcoes.items():
            print(f"- {key}: {desc}")

    def start(self):
        print(f"Olá, {self.nome_usuario}. Eu sou o JARVIS.")
        print("Sistema online e pronto.")

        while True:
            comando = input("O que deseja fazer? ").strip()

            if comando.lower() == "sair":
                print("JARVIS: Desligando o sistema. Até mais!")
                break

            elif comando.lower() == "status":
                print("JARVIS: Todos os sistemas funcionando normalmente.")

            elif comando.lower() == "listar funcoes":
                self.listar_funcoes()

            else:
                # Se o comando for vazio
                if comando.strip() == "":
                    print("JARVIS: Não entendi, digite algo.")
                    continue

                # Verifica se é uma pesquisa
                if "pesquisar" in comando.lower():
                    termo = comando.lower().replace("pesquisar", "").strip()
                    if termo == "":
                        termo = input("JARVIS: O que deseja pesquisar? ").strip()

                    resultados = pesquisar_resumido(termo)
                    print(f"\nJARVIS: Aqui está o que encontrei sobre '{termo}':\n")
                    print(f"Resumo: {resultados['resumo']}\n")
                    print(f"Fonte principal: {resultados['fonte']}\n")
                    if resultados["outros_links"]:
                        print("Outros links:")
                        for link in resultados["outros_links"]:
                            print(f"- {link}")
                    print()  # linha em branco
                else:
                    # Conversa normal com GPT local com loading animado
                    imprimir_com_loading(gpt_local_responder, comando, self.conversa)
