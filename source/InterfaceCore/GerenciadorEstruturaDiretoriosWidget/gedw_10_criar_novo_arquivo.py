import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QInputDialog, QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def criar_novo_arquivo(self, pasta_pai=None):
    try:
        if pasta_pai is None:
            indices = self.tree.selectionModel().selectedIndexes()
            if indices:
                info = self.model.fileInfo(indices[0])
                pasta_pai = info.absoluteFilePath() if info.isDir() else os.path.dirname(info.absoluteFilePath())

            else:
                pasta_pai = self.root_path

        nome_arquivo, ok = QInputDialog.getText(
            self,
            QCoreApplication.translate("LinceuLighthouse", "new_file"),
            QCoreApplication.translate("LinceuLighthouse", "enter_file_name"),
            text=QCoreApplication.translate("LinceuLighthouse", "new_file_default_name")
        )

        if ok and nome_arquivo:
            caminho_novo_arquivo = os.path.join(pasta_pai, nome_arquivo)

            if os.path.exists(caminho_novo_arquivo):
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "file_exists"),
                    QCoreApplication.translate("LinceuLighthouse", "file_already_exists")
                )
                return

            try:
                with open(caminho_novo_arquivo, 'w', encoding='utf-8') as f:
                    f.write('')

                self.arquivo_operacao_realizada.emit("created", caminho_novo_arquivo, "file")
                logger.info(f"Criado novo arquivo: {caminho_novo_arquivo}")

            except Exception as e:
                logger.error(f"Erro ao criar arquivo: {e}", exc_info=True)
                QMessageBox.critical(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "create_file_error"),
                    str(e)
                )

    except Exception as e:
        logger.error(f"Erro ao criar novo arquivo: {e}", exc_info=True)
