from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class MenuPersistente(QMenu):
    def __init__(self, titulo, parent=None):
        try:
            super().__init__(titulo, parent)
            self.setAttribute(Qt.WA_DeleteOnClose, False)
            self.setMouseTracking(True)

        except Exception as e:
            logger.error(f"Erro ao inicializar MenuPersistente: {e}", exc_info=True)

    def mousePressEvent(self, event):
        try:
            action = self.actionAt(event.pos())
            if action and action.isEnabled():
                if not action.menu():
                    action.trigger()
                    event.accept()
                    return

            super().mousePressEvent(event)

        except Exception as e:
            logger.error(f"Erro no mousePressEvent: {e}", exc_info=True)

    def leaveEvent(self, event):
        try:
            pos = self.mapFromGlobal(self.parent().cursor().pos())
            if not self.rect().contains(pos):
                self.close()

            super().leaveEvent(event)

        except Exception as e:
            logger.error(f"Erro no leaveEvent: {e}", exc_info=True)

    def mouseReleaseEvent(self, event):
        try:
            action = self.actionAt(event.pos())
            if action and action.isEnabled() and not action.menu():
                event.accept()
                return

            super().mouseReleaseEvent(event)

        except Exception as e:
            logger.error(f"Erro no mouseReleaseEvent: {e}", exc_info=True)
