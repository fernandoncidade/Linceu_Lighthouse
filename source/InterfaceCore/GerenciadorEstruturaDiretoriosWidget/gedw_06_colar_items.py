import os
import shutil
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def colar_items(self, pasta_destino=None):
    try:
        if not self.clipboard_items:
            return

        if pasta_destino is None:
            indices = self.tree.selectionModel().selectedIndexes()
            if indices:
                info = self.model.fileInfo(indices[0])
                pasta_destino = info.absoluteFilePath() if info.isDir() else os.path.dirname(info.absoluteFilePath())

            else:
                pasta_destino = self.root_path

        sucesso = 0
        erro = 0

        for caminho_origem, operacao in self.clipboard_items:
            try:
                nome_arquivo = os.path.basename(caminho_origem)
                caminho_destino = os.path.join(pasta_destino, nome_arquivo)

                if os.path.exists(caminho_destino):
                    resposta = QMessageBox.question(
                        self,
                        QCoreApplication.translate("LinceuLighthouse", "file_exists"),
                        QCoreApplication.translate("LinceuLighthouse", "file_exists_overwrite").format(nome_arquivo),
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
                    )

                    if resposta == QMessageBox.StandardButton.Cancel:
                        break

                    elif resposta == QMessageBox.StandardButton.No:
                        continue

                if operacao == 'copy':
                    if os.path.isdir(caminho_origem):
                        shutil.copytree(caminho_origem, caminho_destino, dirs_exist_ok=True)

                    else:
                        shutil.copy2(caminho_origem, caminho_destino)

                    self.arquivo_operacao_realizada.emit("copied", caminho_origem, caminho_destino)

                elif operacao == 'cut':
                    shutil.move(caminho_origem, caminho_destino)
                    self.arquivo_operacao_realizada.emit("moved", caminho_origem, caminho_destino)

                sucesso += 1

            except Exception as e:
                logger.error(f"Erro ao colar {caminho_origem}: {e}", exc_info=True)
                erro += 1

        if self.clipboard_items and self.clipboard_items[0][1] == 'cut':
            self.clipboard_items = []

        if sucesso > 0:
            logger.info(f"Colados {sucesso} itens com sucesso")

        if erro > 0:
            logger.warning(f"Falha ao colar {erro} itens")

    except Exception as e:
        logger.error(f"Erro ao colar itens: {e}", exc_info=True)
