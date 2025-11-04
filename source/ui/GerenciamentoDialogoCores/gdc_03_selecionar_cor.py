from PySide6.QtGui import QColor
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _selecionar_cor(self, cor_hex):
    try:
        cor = QColor(cor_hex)
        self.preview_nova.setStyleSheet(f"background-color: {cor_hex};")
        self.cor_selecionada = cor

    except Exception as e:
        logger.error(f"Erro ao selecionar cor {cor_hex}: {e}", exc_info=True)
