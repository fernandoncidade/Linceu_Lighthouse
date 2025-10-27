from PySide6.QtWidgets import QApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_visualizacao_tabela(self):
    try:
        if hasattr(self.interface, 'tabela_dados') and self.atualizacao_pendente:
            self.interface.tabela_dados.viewport().update()
            QApplication.processEvents()
            self.atualizacao_pendente = False

    except Exception as e:
        logger.error(f"Erro ao atualizar visualização da tabela: {e}", exc_info=True)
