# core/auth.py
import os
import msvcrt
from colorama import Fore, Style

class FenixAuth:
    def __init__(self):
        self.USUARIO_AUTORIZADO = os.getenv("FENIX_USER", "bagre")
        self.SENHA_AUTORIZADA = os.getenv("FENIX_PASS", "1234")

    def _input_senha(self, prompt="Senha: "):
        """Captura a senha mascarando os caracteres com asteriscos"""
        senha = ""
        print(prompt, end="", flush=True)
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:
                print()
                break
            elif ch == b'\x08': # Backspace
                if len(senha) > 0:
                    senha = senha[:-1]
                    print("\b \b", end="", flush=True)
            else:
                senha += ch.decode()
                print("*", end="", flush=True)
        return senha

    def autenticar(self):
        """Executa o protocolo de autenticação do Projeto Fenix"""
        print(f"{Fore.RED}=== PROTOCOLO DE ACESSO: NÚCLEO FENIX ==={Style.RESET_ALL}")
        usuario = input("ID de Usuário: ").strip()
        senha = self._input_senha("Código de Acesso: ")
        
        if usuario == self.USUARIO_AUTORIZADO and senha == self.SENHA_AUTORIZADA:
            print(f"{Fore.GREEN}Identidade confirmada. Bem-vindo, {usuario}.{Style.RESET_ALL}\n")
            return True
        
        print(f"{Fore.RED}ACESSO NEGADO: Credenciais Inválidas.{Style.RESET_ALL}")
        return False