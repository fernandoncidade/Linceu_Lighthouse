from PySide6.QtWidgets import QTabWidget
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_painel_graficos(self):
    try:
        self.tab_widget = QTabWidget()
        return self.tab_widget

    except Exception as e:
        logger.error(f"Erro ao criar painel de gráficos: {e}", exc_info=True)
