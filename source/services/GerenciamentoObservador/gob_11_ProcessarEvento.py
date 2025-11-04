import os
import time
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def processar_evento(self, acao, nome_arquivo, tempo_evento=None):
    try:
        if self.pausado or not self._pause_event.is_set():
            return

        if self.falhas_consecutivas >= self.max_falhas:
            self.reiniciar_monitoramento()
            return

        caminho_completo = os.path.join(self.diretorio, nome_arquivo)
        tempo_atual = tempo_evento if tempo_evento else time.time()

        if nome_arquivo in self.eventos_ignorados:
            self.eventos_ignorados.remove(nome_arquivo)
            return

        if acao == 3 and os.path.isdir(caminho_completo):
            return

        ext = os.path.splitext(nome_arquivo)[1].lower()
        arquivos_especiais = {'.heic', '.xlsx', '.xls', '.docx', '.pdf', '.mp4', '.mov', '.avi', '.mkv', '.xml'}

        tempo_limite_especial = 0.1
        tempo_limite_normal = 0.05

        if acao == 2:
            if nome_arquivo in self.arquivos_recem_excluidos:
                tempo_limite = tempo_limite_especial if ext in arquivos_especiais else tempo_limite_normal
                if (tempo_atual - self.arquivos_recem_excluidos[nome_arquivo]) < tempo_limite:
                    return

            self.evento_excluido.processar(nome_arquivo, caminho_completo, tempo_atual)
            return

        elif acao in [4, 5]:
            with self.registros_lock:
                self.evento_renomeado.processar(nome_arquivo, caminho_completo, acao)
            return

        elif acao == 1:
            if nome_arquivo in self.arquivos_recem_adicionados:
                tempo_limite = tempo_limite_especial if ext in arquivos_especiais else tempo_limite_normal
                if (tempo_atual - self.arquivos_recem_adicionados[nome_arquivo]) < tempo_limite:
                    return

            self.arquivos_recem_adicionados[nome_arquivo] = tempo_atual
            self.evento_adicionado.processar(nome_arquivo, caminho_completo, tempo_atual)
            return

        elif acao == 3:
            if nome_arquivo in self.arquivos_recem_modificados:
                tempo_limite = tempo_limite_especial if ext in arquivos_especiais else tempo_limite_normal
                if (tempo_atual - self.arquivos_recem_modificados[nome_arquivo]) < tempo_limite:
                    return

            if os.path.exists(caminho_completo):
                self.evento_modificado.processar(nome_arquivo, caminho_completo, tempo_atual)

        self.falhas_consecutivas = 0

    except Exception as e:
        self.falhas_consecutivas += 1
        self.ultimo_erro = str(e)
        logger.error(f"Erro ao processar evento (tentativa {self.falhas_consecutivas}): {e}", exc_info=True)
