from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _confirmar_mudanca_idioma(self):
    try:
        message_box = QMessageBox(self.interface)
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle(self.loc.get_text("warning"))
        message_box.setText(self.loc.get_text("language_change_confirm"))
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)
        message_box.setButtonText(QMessageBox.Yes, self.loc.get_text("yes"))
        message_box.setButtonText(QMessageBox.No, self.loc.get_text("no"))
        return message_box.exec()

    except Exception as e:
        logger.error(f"Erro ao confirmar mudança de idioma: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
