# main.py
import os
import warnings

# 1. Silencia avisos de bibliotecas e a saudação do Pygame antes de carregar o sistema
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from core.brain import FenixBrain

if __name__ == "__main__":
    # Inicializando o sistema com o tratamento correto para o criador
    # O Senhor é Airton, mas o sistema o tratará como Senhor.
    fenix = FenixBrain(nome_usuario="Senhor")
    
    try:
        fenix.start()
    except KeyboardInterrupt:
        print("\n[SISTEMA]: Finalizado manualmente pelo Criador.")
    except Exception as e:
        print(f"\n[ERRO CRÍTICO]: {e}")