import os
import shutil
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def excluir_selecionados(self):
    try:
        caminhos = self.obter_selecionados()
        if not caminhos:
            return

        resposta = QMessageBox.question(
            self,
            QCoreApplication.translate("LinceuLighthouse", "confirm_delete"),
            QCoreApplication.translate("LinceuLighthouse", "confirm_delete_items").format(len(caminhos)),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if resposta != QMessageBox.StandardButton.Yes:
            return

        sucesso = 0
        erro = 0

        for caminho in caminhos:
            try:
                if os.path.isdir(caminho):
                    shutil.rmtree(caminho)

                else:
                    os.remove(caminho)

                self.arquivo_operacao_realizada.emit("deleted", caminho, "")
                sucesso += 1

            except Exception as e:
                logger.error(f"Erro ao excluir {caminho}: {e}", exc_info=True)
                erro += 1

        if sucesso > 0:
            logger.info(f"Excluídos {sucesso} itens com sucesso")

        if erro > 0:
            logger.warning(f"Falha ao excluir {erro} itens")

    except Exception as e:
        logger.error(f"Erro ao excluir selecionados: {e}", exc_info=True)
