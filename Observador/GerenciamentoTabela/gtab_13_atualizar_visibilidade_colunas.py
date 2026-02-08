from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def atualizar_visibilidade_colunas(self, atualizar_em_massa=False):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados

        colunas_ordenadas = sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"])

        if atualizar_em_massa:
            if tabela.columnCount() != len(colunas_ordenadas):
                self.configurar_tabela(tabela)
                return

            tabela.blockSignals(True)
            try:
                for i, (key, coluna) in enumerate(colunas_ordenadas):
                    if i < tabela.columnCount():
                        tabela.setColumnHidden(i, not coluna["visivel"])

                self.aplicar_quebra_linha_todos_cabecalhos(tabela)
                self.ajustar_altura_cabecalho(tabela)

            finally:
                tabela.blockSignals(False)
                self._invalidar_cache_cores()
                tabela.viewport().update()
                QApplication.processEvents()

            return

        if tabela.columnCount() != len(colunas_ordenadas):
            self.configurar_tabela(tabela)
            return

        tabela.blockSignals(True)

        try:
            for i, (key, coluna) in enumerate(colunas_ordenadas):
                if i < tabela.columnCount():
                    tabela.setColumnHidden(i, not coluna["visivel"])

            self.aplicar_quebra_linha_todos_cabecalhos(tabela)
            self.ajustar_altura_cabecalho(tabela)

        finally:
            tabela.blockSignals(False)
            self._invalidar_cache_cores()
            tabela.viewport().update()
            QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao atualizar visibilidade das colunas: {e}", exc_info=True)
        raise
