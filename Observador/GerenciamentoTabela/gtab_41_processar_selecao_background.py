from PySide6.QtCore import QTimer
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_selecao_background(gt):
    try:
        QTimer.singleShot(0, gt.ajustar_cor_selecao)
        return True

    except Exception as e:
        logger.error(f"Erro no processamento background de seleção: {e}", exc_info=True)
        return False
