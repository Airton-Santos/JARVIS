# core/config_audio.py
import speech_recognition as sr

class ConfigAudio:
    def __init__(self):
        self.ENERGY_THRESHOLD = 80
        self.PAUSE_THRESHOLD = 0.8
        self.DYNAMIC_ENERGY = False
        
        # TUDO EM MINÚSCULO PARA EVITAR CONFLITO
        self.WAKE_WORDS = ["fênix", "fenix"]
        
        self.CMD_DESLIGAR = ["desligar projeto fênix", "desligar nucleo fênix", "fênix desligar sistema", "desligar fenix"]
        self.CMD_DESATIVAR_VOZ = ["desativar comando por voz", "suspender comando por voz", "pausar comando por voz"]
        
        # COMANDOS DE ESCRITA
        self.CMD_ATIVAR_ESCRITA = ["ativar escrita", "ativar modo escrita", "modo de digitação", "modo de digitaçao"]

    def configurar_reconhecedor(self, reconhecedor):
        reconhecedor.energy_threshold = self.ENERGY_THRESHOLD
        reconhecedor.pause_threshold = self.PAUSE_THRESHOLD
        reconhecedor.dynamic_energy_threshold = self.DYNAMIC_ENERGY
        return reconhecedor