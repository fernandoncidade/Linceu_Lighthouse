from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_traducoes_carregadas(self, idioma: str):
    try:
        if getattr(self, "_aguardando_conclusao_traducao", False):
            self._aguardando_conclusao_traducao = False
            QMessageBox.information(self.interface, self.loc.get_text("success"), self.loc.get_text("translation_complete"))

    except Exception as e:
        logger.error(f"Erro ao exibir confirmação de conclusão da tradução: {e}", exc_info=True)
