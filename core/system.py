import psutil
import os
import shutil

def obter_processos_pesados():
    """Retorna os 3 processos que mais usam RAM"""
    processos = []
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            processos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    processos = sorted(processos, key=lambda p: p['memory_info'].rss, reverse=True)[:3]
    resultado = ""
    for p in processos:
        mb = p['memory_info'].rss / (1024 * 1024)
        resultado += f"{p['name']} consumindo {mb:.0f} megas. "
    return resultado

def saude_hardware():
    """Verifica Disco e CPU"""
    uso_disco = psutil.disk_usage('/').percent
    cpu_total = psutil.cpu_percent(interval=1)
    return f"O processador está em {cpu_total} por cento de uso e o disco principal está com {uso_disco} por cento ocupado."

def encerrar_processo(nome_processo):
    """Protocolo de encerramento forçado"""
    try:
        for proc in psutil.process_iter(['name']):
            if nome_processo.lower() in proc.info['name'].lower():
                proc.terminate()
                return True
        return False
    except:
        return False

def limpar_temporarios():
    """Limpeza real da pasta TEMP do Windows"""
    pasta_temp = os.environ.get('TEMP')
    arquivos_removidos = 0
    
    if not pasta_temp:
        return "Senhor, não consegui localizar a pasta de arquivos temporários."

    for nome in os.listdir(pasta_temp):
        caminho_completo = os.path.join(pasta_temp, nome)
        try:
            if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                os.unlink(caminho_completo) # Deleta arquivo
                arquivos_removidos += 1
            elif os.path.isdir(caminho_completo):
                shutil.rmtree(caminho_completo) # Deleta pasta
                arquivos_removidos += 1
        except Exception:
            # Muitos arquivos estarão em uso pelo Windows, apenas ignoramos esses
            continue
            
    return f"Protocolo de limpeza concluído. Consegui remover {arquivos_removidos} itens desnecessários."

def analisar_conexoes():
    """Identifica programas usando a rede agora"""
    conexoes = psutil.net_connections()
    processos_ativos = []
    for conn in conexoes:
        if conn.status == 'ESTABLISHED' and conn.pid:
            try:
                p = psutil.Process(conn.pid)
                if p.name() not in processos_ativos:
                    processos_ativos.append(p.name())
            except: continue
    
    if processos_ativos:
        return "Programas conectados à rede: " + ", ".join(processos_ativos[:4])
    return "Nenhuma conexão externa ativa no momento."

def ajustar_volume_app(nivel):
    """
    Ajusta o volume especificamente do processo do Projeto Fenix.
    Nivel: 0.0 a 1.0
    """
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == "python.exe": # Ou o nome do seu .exe
                volume.SetMasterVolume(nivel, None)
    except Exception as e:
        print(f"Erro ao ajustar volume: {e}")

def encerrar_projeto():
    """Finaliza todos os protocolos e fecha o programa"""
    # Aqui o senhor pode adicionar comandos para salvar logs antes de sair
    print("Encerrando Projeto Fenix. Até logo, Senhor.")
    os._exit(0) # Força o fechamento de todas as threads (inclusive a do microfone)