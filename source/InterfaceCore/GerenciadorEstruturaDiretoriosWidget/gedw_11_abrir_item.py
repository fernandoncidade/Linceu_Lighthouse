import os
import sys
import subprocess
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def abrir_item(self, index=None):
    try:
        if index is None:
            indices = self.tree.selectionModel().selectedIndexes()
            if not indices:
                return

            index = indices[0]

        info = self.model.fileInfo(index)
        caminho = info.absoluteFilePath()

        if info.isDir():
            if self.tree.isExpanded(index):
                self.tree.collapse(index)

            else:
                self.tree.expand(index)

        else:
            try:
                if sys.platform.startswith('win'):
                    os.startfile(caminho)

                elif sys.platform.startswith('darwin'):
                    subprocess.run(['open', caminho])

                else:
                    subprocess.run(['xdg-open', caminho])

                logger.info(f"Aberto arquivo: {caminho}")

            except Exception as e:
                logger.error(f"Erro ao abrir arquivo {caminho}: {e}", exc_info=True)
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "open_error"),
                    QCoreApplication.translate("LinceuLighthouse", "cannot_open_file").format(caminho)
                )

    except Exception as e:
        logger.error(f"Erro ao abrir item: {e}", exc_info=True)
