import textwrap
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def aplicar_quebra_linha_cabecalho(self, tabela, coluna_index):
    try:
        if coluna_index not in self.texto_original_cabecalhos:
            return

        texto_original = self.texto_original_cabecalhos[coluna_index]
        largura_coluna = tabela.columnWidth(coluna_index)

        font_metrics = QFontMetrics(tabela.horizontalHeader().font())

        padding = 10
        espaco_disponivel = largura_coluna - padding

        char_width = font_metrics.averageCharWidth()
        max_chars = max(1, int(espaco_disponivel / char_width))

        texto_quebrado = textwrap.fill(texto_original, width=max_chars, break_long_words=False, break_on_hyphens=True)

        item = tabela.horizontalHeaderItem(coluna_index)
        if item:
            item.setText(texto_quebrado)
            item.setTextAlignment(Qt.AlignCenter)

    except Exception:
        logger.error(f"Erro ao aplicar quebra de linha no cabeçalho da coluna {coluna_index}", exc_info=True)
