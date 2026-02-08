from PySide6.QtGui import Qt
from PySide6.QtCore import QMetaObject
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_dados(self):
    try:
        if self.interface.observador:
            self.interface.observador.limpar_estado()

        self.interface.excluidos_recentemente.clear()
        self.interface.gerenciador_colunas.cache_metadados.clear()
        QMetaObject.invokeMethod(self.interface, "atualizar_status", Qt.QueuedConnection)

    except Exception as e:
        logger.error(f"Erro ao limpar dados no gerenciador: {e}", exc_info=True)
