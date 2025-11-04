import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def calcular_intervalo(self, caminho_completo):
    try:
        ext = os.path.splitext(caminho_completo)[1].lower()

        if ext in self.EXTENSOES_RAPIDAS:
            return self.min_intervalo

        if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada:
            return self.min_intervalo

        tamanho = os.path.getsize(caminho_completo)
        if tamanho > self.grande_arquivo_threshold:
            return min(self.tempo_espera_grande_arquivo, 1.0)

        return self._calcular_intervalo_original(caminho_completo)

    except Exception as e:
        logger.error(f"Erro ao calcular intervalo: {e}", exc_info=True)
        return self.min_intervalo
