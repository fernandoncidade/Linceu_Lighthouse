from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QWidget
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def changeEvent(self, event):
    if event.type() == QEvent.LanguageChange:
        try:
            if hasattr(self.model, "retranslate"):
                self.model.retranslate()

        except Exception as e:
            logger.error(f"Erro ao retraduzir cabeçalhos: {e}", exc_info=True)

    QWidget.changeEvent(self, event)
