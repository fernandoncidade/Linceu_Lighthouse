from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from PySide6.QtCore import QTimer, Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def redefinir_cores_todas_colunas(self):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados
        cor_texto_padrao = QApplication.palette().color(QPalette.Text)

        cores = self._obter_cores_operacao()

        header_indices = self._obter_indices_colunas(tabela)
        nome_tipo_operacao = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS["tipo_operacao"]["nome"].replace('\n', ' ').strip()
        indice_tipo_operacao = header_indices.get(nome_tipo_operacao, None)

        linhas = tabela.rowCount()
        colunas = tabela.columnCount()

        def aplicar_linha(row):
            if row >= linhas:
                tabela.viewport().update()
                QApplication.processEvents()
                return

            for col in range(colunas):
                item = tabela.item(row, col)
                if item:
                    if col == indice_tipo_operacao:
                        valor = item.text()
                        cor = cores.get(valor)
                        if cor:
                            item.setBackground(cor)
                            cor_texto = self.calcular_cor_texto_ideal(cor, False)
                            item.setForeground(cor_texto)

                    else:
                        item.setBackground(Qt.NoBrush)
                        item.setForeground(cor_texto_padrao)

            QTimer.singleShot(0, lambda: aplicar_linha(row + 1))

        self._invalidar_cache_cores()
        aplicar_linha(0)

    except Exception as e:
        logger.error(f"Erro ao redefinir cores de todas as colunas: {e}", exc_info=True)
        raise
