from PySide6.QtWidgets import QHeaderView
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def ajustar_larguras_colunas(self, tabela_dados, colunas_visiveis):
    try:
        header = tabela_dados.horizontalHeader()
        font = header.font()
        font_metrics = QFontMetrics(font)

        PADDING = 40
        MIN_WIDTH = 10
        MAX_WIDTH = 350

        self.larguras_calculadas = {}

        for i, (key, coluna) in enumerate(colunas_visiveis):
            texto_cabecalho = coluna["nome"]

            texto_largura = font_metrics.horizontalAdvance(texto_cabecalho)

            max_content_width = 0
            for row in range(min(10, tabela_dados.rowCount())):
                item = tabela_dados.item(row, i)
                if item and item.text():
                    content_width = font_metrics.horizontalAdvance(item.text())
                    max_content_width = max(max_content_width, content_width)

            largura_total = max(texto_largura, max_content_width) + PADDING
            largura_ideal = min(max(largura_total, MIN_WIDTH), MAX_WIDTH)
            self.larguras_calculadas[i] = largura_ideal

            tabela_dados.setColumnWidth(i, largura_ideal)
            header.setSectionResizeMode(i, QHeaderView.Interactive)

            item = tabela_dados.horizontalHeaderItem(i)
            if item:
                item.setTextAlignment(Qt.AlignCenter)
    
    except Exception:
        logger.error("Erro ao ajustar larguras das colunas", exc_info=True)
        raise
