# core/stt.py
import speech_recognition as sr

def capturar_voz(reconhecedor, timeout=None, phrase_limit=None):
    with sr.Microphone() as source:
        try:
            audio = reconhecedor.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            return texto.lower().strip()
        except:
            return None