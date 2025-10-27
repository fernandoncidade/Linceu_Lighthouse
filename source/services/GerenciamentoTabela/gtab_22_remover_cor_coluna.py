from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_cor_coluna(self, coluna_key):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados
        cor_texto_padrao = QApplication.palette().color(QPalette.Text)

        header_indices = self._obter_indices_colunas(tabela)
        nome_coluna = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[coluna_key]["nome"]

        indice_coluna = None
        for header, idx in header_indices.items():
            if nome_coluna.replace('\n', ' ').strip() == header:
                indice_coluna = idx
                break

        if indice_coluna is None:
            return

        for row in range(tabela.rowCount()):
            item = tabela.item(row, indice_coluna)
            if item:
                item.setBackground(Qt.NoBrush)
                item.setForeground(cor_texto_padrao)

        tabela.viewport().update()
        QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao remover cor da coluna '{coluna_key}': {e}", exc_info=True)
        raise
