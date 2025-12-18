# core/ai.py
import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import CTransformers

# 1. Obtém o caminho absoluto da pasta do projeto (JARVIS)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Caminho para a pasta models
MODEL_PATH = os.path.join(BASE_DIR, "models", "bode-7b-alpaca-q8_0.gguf")

# --- TESTE DE SEGURANÇA ---
if not os.path.exists(MODEL_PATH):
    print(f"\n[ERRO] O modelo não foi encontrado em: {MODEL_PATH}")
    print("Verifica se o nome da pasta e do ficheiro estão corretos.\n")
# --------------------------

# 3. Prompt de Personalidade: Agora ele sabe quem é o JARVIS e quem é o BAGRE
template = """Você é o JARVIS, a inteligência artificial que está para ajudar em qualquer coisa. Você é prestativo, sarcástico e muito inteligente.
Sua tarefa é responder ao Bagre de forma direta e elegante.

Bagre pergunta: {instruction}

JARVIS responde:"""

prompt = PromptTemplate(template=template, input_variables=["instruction"])

# 4. Configuração Otimizada:
# 'stop' impede que a IA comece a inventar perguntas e respostas sozinha.
config = {
    'max_new_tokens': 150, 
    'temperature': 0.2, # Menor temperatura = menos respostas estranhas
    'top_p': 0.9,
    'context_length': 2048,
    'stop': ["Bagre pergunta:", "JARVIS responde:", "\n\n"] 
}

# Inicializa o modelo
llm = CTransformers(model=MODEL_PATH, model_type="llama", config=config)

chain = prompt | llm

def bode_responder(mensagem: str) -> str:
    try:
        # Chamada do modelo
        resposta = chain.invoke({"instruction": mensagem})
        
        # Limpeza da resposta
        texto_limpo = str(resposta).strip()
        
        # Se por acaso a IA repetir o prompt, tentamos pegar só a resposta
        if "JARVIS responde:" in texto_limpo:
            texto_limpo = texto_limpo.split("JARVIS responde:")[-1].strip()
            
        return texto_limpo
    except Exception as e:
        return f"Senhor, tive um problema nos meus circuitos: {e}"