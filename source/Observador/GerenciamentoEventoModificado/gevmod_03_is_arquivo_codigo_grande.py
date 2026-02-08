import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def is_arquivo_codigo_grande(self, caminho):
    try:
        ext = os.path.splitext(caminho)[1].lower()
        if ext not in self.EXTENSOES_CODIGO:
            return False

        if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada:
            return False

        with open(caminho, 'rb') as f:
            return sum(1 for _ in f) > self.CODIGO_LINHA_THRESHOLD

    except Exception as e:
        logger.error(f"Erro ao verificar arquivo de código grande: {e}", exc_info=True)
        return False
