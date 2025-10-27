import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QInputDialog, QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def renomear_selecionado(self):
    try:
        indices = self.tree.selectionModel().selectedIndexes()
        if not indices:
            return

        index = indices[0]
        info = self.model.fileInfo(index)
        caminho_original = info.absoluteFilePath()
        nome_original = info.fileName()

        novo_nome, ok = QInputDialog.getText(
            self,
            QCoreApplication.translate("LinceuLighthouse", "rename"),
            QCoreApplication.translate("LinceuLighthouse", "enter_new_name"),
            text=nome_original
        )

        if ok and novo_nome and novo_nome != nome_original:
            pasta_pai = os.path.dirname(caminho_original)
            novo_caminho = os.path.join(pasta_pai, novo_nome)

            if os.path.exists(novo_caminho):
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "rename_error"),
                    QCoreApplication.translate("LinceuLighthouse", "file_already_exists")
                )
                return

            try:
                os.rename(caminho_original, novo_caminho)
                self.arquivo_operacao_realizada.emit("renamed", caminho_original, novo_caminho)
                logger.info(f"Renomeado {caminho_original} para {novo_caminho}")

            except Exception as e:
                logger.error(f"Erro ao renomear: {e}", exc_info=True)
                QMessageBox.critical(
                    self,
                    QCoreApplication.translate("LinceuLighthouse", "rename_error"),
                    str(e)
                )

    except Exception as e:
        logger.error(f"Erro ao renomear selecionado: {e}", exc_info=True)
