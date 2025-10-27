import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QInputDialog, QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def criar_nova_pasta(self, pasta_pai=None):
    try:
        if pasta_pai is None:
            indices = self.tree.selectionModel().selectedIndexes()
            if indices:
                info = self.model.fileInfo(indices[0])
                pasta_pai = info.absoluteFilePath() if info.isDir() else os.path.dirname(info.absoluteFilePath())

            else:
                pasta_pai = self.root_path

        nome_pasta, ok = QInputDialog.getText(
            self,
            QCoreApplication.translate("LinceuLighthouse", "new_folder"),
            QCoreApplication.translate("LinceuLighthouse", "enter_folder_name"),
            text=QCoreApplication.translate("LinceuLighthouse", "new_folder_default_name")
        )

        if ok and nome_pasta:
            caminho_nova_pasta = os.path.join(pasta_pai, nome_pasta)

            if os.path.exists(caminho_nova_pasta):
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "folder_exists"),
                    QCoreApplication.translate("LinceuLighthouse", "folder_already_exists")
                )
                return

            try:
                os.makedirs(caminho_nova_pasta)
                self.arquivo_operacao_realizada.emit("created", caminho_nova_pasta, "folder")
                logger.info(f"Criada nova pasta: {caminho_nova_pasta}")

            except Exception as e:
                logger.error(f"Erro ao criar pasta: {e}", exc_info=True)
                QMessageBox.critical(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "create_folder_error"),
                    str(e)
                )

    except Exception as e:
        logger.error(f"Erro ao criar nova pasta: {e}", exc_info=True)
