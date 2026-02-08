from PySide6.QtWidgets import QDialog
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def accept(self):
    try:
        if self.cor_selecionada and self.cor_selecionada.isValid():
            self.corSelecionada.emit(self.cor_selecionada)

        QDialog.accept(self)

    except Exception as e:
        logger.error(f"Erro ao confirmar seleção de cor: {e}", exc_info=True)
