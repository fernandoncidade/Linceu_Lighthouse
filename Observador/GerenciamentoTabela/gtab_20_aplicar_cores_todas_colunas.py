from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QTimer, Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def aplicar_cores_todas_colunas(self):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados

        if tabela.rowCount() == 0:
            return

        cores = self._obter_cores_operacao()
        cor_padrao = QColor(255, 255, 255)
        cor_texto_padrao = QApplication.palette().color(QPalette.Text)
        header_indices = self._obter_indices_colunas(tabela)
        nome_tipo_operacao = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS["tipo_operacao"]["nome"].replace('\n', ' ').strip()
        indice_tipo_operacao = header_indices.get(nome_tipo_operacao, None)
        if indice_tipo_operacao is None:
            return

        linhas = tabela.rowCount()
        colunas = list(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items())

        def processar_linha(row):
            if row >= linhas:
                tabela.viewport().update()
                QApplication.processEvents()
                return

            item_tipo = tabela.item(row, indice_tipo_operacao)
            tipo_operacao_valor = item_tipo.text() if item_tipo else ""

            for key, coluna in colunas:
                nome_coluna = coluna["nome"].replace('\n', ' ').strip()
                indice_coluna = header_indices.get(nome_coluna, None)
                if indice_coluna is None or indice_coluna >= tabela.columnCount():
                    continue

                item = tabela.item(row, indice_coluna)
                if not item:
                    continue

                if key != "tipo_operacao" and key not in self.colunas_para_colorir:
                    item.setBackground(Qt.NoBrush)
                    item.setForeground(cor_texto_padrao)
                    continue

                if not self.cores_visiveis:
                    item.setBackground(Qt.NoBrush)
                    item.setForeground(cor_texto_padrao)
                    continue

                cor = cores.get(tipo_operacao_valor, cor_padrao)
                eh_personalizada = self.eh_coluna_personalizada_colorida(key) if hasattr(self, 'eh_coluna_personalizada_colorida') else (key != "tipo_operacao")
                cor_texto = self.calcular_cor_texto_ideal(cor, eh_coluna_personalizada=eh_personalizada)
                item.setBackground(cor)
                item.setForeground(cor_texto)

            QTimer.singleShot(0, lambda: processar_linha(row + 1))

        processar_linha(0)

    except Exception as e:
        logger.error(f"Erro ao aplicar cores em todas as colunas: {e}", exc_info=True)
        raise
