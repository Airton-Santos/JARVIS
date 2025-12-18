# core/stt.py
import speech_recognition as sr

def ouvir_microfone():
    # Inicializa o reconhecedor
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as source:
        # Ajusta o ruído ambiente
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        print("Jarvis: Ouvindo...")
        
        try:
            # Ouve o áudio
            audio = reconhecedor.listen(source, timeout=5, phrase_time_limit=10)
            print("Jarvis: Reconhecendo...")
            
            # Converte áudio em texto (usando Google de forma gratuita)
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")
            return texto.lower()
            
        except sr.UnknownValueError:
            return "não entendi o que você disse."
        except sr.RequestError:
            return "erro de conexão com o serviço de voz."
        except Exception as e:
            return ""