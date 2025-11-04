from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def aplicar_cores_linha_especifica(self, tabela, row, tipo_operacao_valor=None):
    try:
        if not hasattr(self.interface, 'tabela_dados') or row >= tabela.rowCount():
            return

        cores = self._obter_cores_operacao()
        cor_padrao = QColor(255, 255, 255)
        cor_texto_padrao = QApplication.palette().color(QPalette.Text)

        header_indices = self._obter_indices_colunas(tabela)

        nome_tipo_operacao = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS["tipo_operacao"]["nome"].replace('\n', ' ').strip()
        indice_tipo_operacao = header_indices.get(nome_tipo_operacao, None)

        if tipo_operacao_valor is None and indice_tipo_operacao is not None:
            item_tipo = tabela.item(row, indice_tipo_operacao)
            tipo_operacao_valor = item_tipo.text() if item_tipo else ""

        for key, coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items():
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

            if key == "tipo_operacao":
                cor = cores.get(tipo_operacao_valor, cor_padrao)
                cor_texto = self.calcular_cor_texto_ideal(cor, False)

            elif key in self.colunas_para_colorir:
                cor = cores.get(tipo_operacao_valor, cor_padrao)
                cor_texto = self.calcular_cor_texto_ideal(cor, eh_coluna_personalizada=True)

            else:
                continue

            item.setBackground(cor)
            item.setForeground(cor_texto)

    except Exception as e:
        logger.error(f"Erro ao aplicar cores na linha {row}: {e}", exc_info=True)
        raise
