from gpt4all import GPT4All
from deep_translator import GoogleTranslator
import os

# Configuração do modelo local
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "falcon-7b-instruct.gguf")  # caminho do modelo
model = GPT4All(MODEL_PATH, allow_download=False)

SYSTEM_PROMPT = """
Você é um assistente educado, direto e inteligente.
Responda sempre em inglês, com respostas curtas e objetivas.
Se não souber a resposta, diga "I don't know the answer."
Não invente histórias.
Nunca repita frases do usuário.
"""

# Função para conversar com o modelo
def gpt_local_responder(texto_pt, conversa=[]):
    # Traduz entrada do usuário para inglês
    try:
        texto_en = GoogleTranslator(source='pt', target='en').translate(texto_pt)
    except:
        texto_en = texto_pt  # fallback caso a tradução falhe

    # Mantém histórico curto (últimas 4 mensagens)
    conversa = conversa[-4:]

    # Monta prompt completo
    prompt = SYSTEM_PROMPT + "\n"
    for c in conversa:
        prompt += c + "\n"
    prompt += f"User: {texto_en}\nAssistant:"

    # Gera resposta
    resposta_en = model.generate(prompt, max_tokens=150, temp=0.4, top_p=0.9).strip()

    # Adiciona ao histórico
    conversa.append(f"User: {texto_en}")
    conversa.append(f"Assistant: {resposta_en}")

    # Traduz resposta de volta para português
    try:
        resposta_pt = GoogleTranslator(source='en', target='pt').translate(resposta_en)
    except:
        resposta_pt = resposta_en  # fallback caso a tradução falhe

    return resposta_pt
