from PySide6.QtWidgets import QApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_cores_colunas(self, aplicar_em_massa=False):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados

        if aplicar_em_massa:
            tabela.blockSignals(True)
            try:
                self._invalidar_cache_cores()
                self.aplicar_cores_todas_colunas()

            finally:
                tabela.blockSignals(False)
                tabela.viewport().update()
                QApplication.processEvents()

            return

        self._invalidar_cache_cores()
        self.aplicar_cores_todas_colunas()

    except Exception as e:
        logger.error(f"Erro ao atualizar cores das colunas: {e}", exc_info=True)
        raise
