from google import genai
from google.genai import types
import re
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# CONFIGURAÇÃO DA CHAVE
API_KEY = "AIzaSyBiyUGyZS6_iIeOD_rMRRuG4nTSVVexQLs" 
client = genai.Client(api_key=API_KEY)

def bode_responder(mensagem: str) -> str:
    """Núcleo Neural FENIX - Busca ativa e Português perfeito"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=mensagem,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                system_instruction=(
                    "Você é a Fenix, assistente do Senhor Bagre que mora em Maceió. "
                    "Responda sempre em texto corrido. Não use listas, asteriscos ou símbolos. "
                    "Fale de forma natural e use corretamente os acentos da língua portuguesa."
                ),
                max_output_tokens=150,
                temperature=0.7
            )
        )
        
        texto = response.text
        
        # LIMPEZA SELETIVA: 
        # Remove símbolos de formatação (*, #, _, etc) e emojis, 
        # mas mantém TODAS as letras (a-z, A-Z), números e ACENTOS (ç, á, à, ã, ê, etc).
        texto_limpo = re.sub(r'[^\w\s\d.,?!áàâãéèêíïóôõúüçÁÀÂÃÉÈÊÍÏÓÔÕÚÜÇ]', '', texto)
        
        # Remove espaços duplos que podem surgir na limpeza
        texto_final = " ".join(texto_limpo.split())
        
        return texto_final
    
    except Exception as e:
        return f"Senhor, erro no processamento: {e}"