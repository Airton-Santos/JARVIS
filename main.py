import os
import warnings
import threading
from core.interface import FenixUI
from core.brain import FenixBrain

# Silenciar avisos
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def rodar_sistema(interface):
    """Função que rodará o cérebro em uma thread separada"""
    fenix = FenixBrain(interface=interface, nome_usuario="Senhor")
    try:
        fenix.start()
    except Exception as e:
        interface.log_msg(f"ERRO NO NÚCLEO: {e}")

if __name__ == "__main__":
    # 1. Cria a Interface
    app = FenixUI()
    
    # 2. Cria a Thread para o Cérebro não travar a UI
    brain_thread = threading.Thread(target=rodar_sistema, args=(app,), daemon=True)
    
    # 3. No botão 'SISTEMA ON' da sua Interface, você pode chamar brain_thread.start()
    # Ou iniciar automaticamente aqui:
    brain_thread.start()
    
    # 4. Inicia a Interface (Loop Principal)
    app.mainloop()