import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_massivo(self, nome_arquivo, caminho_completo, tempo_atual):
    try:
        if nome_arquivo in self.observador.ultima_modificacao:
            ultimo_tempo = self.observador.ultima_modificacao[nome_arquivo]
            if (tempo_atual - ultimo_tempo) < self.min_intervalo:
                return False

        self.modificacoes_recentes[nome_arquivo] = tempo_atual
        self.count_modificacoes[nome_arquivo] = self.count_modificacoes.get(nome_arquivo, 0) + 1
        self.observador.ultima_modificacao[nome_arquivo] = tempo_atual
        ext = os.path.splitext(nome_arquivo)[1].lower()
        self._limpar_cache_metadados(caminho_completo, ext)
        self.notificar_evento(self.observador.loc.get_text("op_modified"), nome_arquivo, caminho_completo, caminho_completo)
        return True

    except Exception as e:
        logger.error(f"Erro ao processar modificação massiva: {e}", exc_info=True)
        return False
