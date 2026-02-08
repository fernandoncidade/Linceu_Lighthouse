from PySide6.QtWidgets import QMessageBox, QApplication, QDialog
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_interface(self):
    try:
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QDialog) and hasattr(widget, 'filtro_panel'):
                if hasattr(widget.filtro_panel, 'atualizar_interface'):
                    widget.filtro_panel.atualizar_interface()

            if isinstance(widget, QMessageBox):
                if widget.standardButtons() & QMessageBox.Yes:
                    widget.setButtonText(QMessageBox.Yes, self.loc.get_text("yes"))

                if widget.standardButtons() & QMessageBox.No:
                    widget.setButtonText(QMessageBox.No, self.loc.get_text("no"))

                if widget.standardButtons() & QMessageBox.Ok:
                    widget.setButtonText(QMessageBox.Ok, self.loc.get_text("ok"))

                if widget.standardButtons() & QMessageBox.Cancel:
                    widget.setButtonText(QMessageBox.Cancel, self.loc.get_text("cancel"))

        if hasattr(self.interface, 'context_menu'):
            for action in self.interface.context_menu.actions():
                if hasattr(action, 'data') and callable(action.data):
                    menu_key = action.data()
                    if isinstance(menu_key, str) and menu_key.startswith("menu_"):
                        action.setText(self.loc.get_text(menu_key))

    except Exception as e:
        logger.error(f"Erro ao atualizar interface do gerenciador de eventos: {e}", exc_info=True)
