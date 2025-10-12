from PySide6.QtWidgets import QHeaderView
from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def ajustar_larguras_colunas(self, tabela_dados, colunas_visiveis):
    try:
        header = tabela_dados.horizontalHeader()
        header.setMinimumSectionSize(10)
        font = header.font()
        font_metrics = QFontMetrics(font)

        PADDING = 40
        MIN_WIDTH = 10

        self.larguras_calculadas = {}
        for i, (key, coluna) in enumerate(colunas_visiveis):
            texto_cabecalho = self.texto_original_cabecalhos.get(i, coluna["nome"]).replace('\n', ' ')
            texto_largura = font_metrics.horizontalAdvance(texto_cabecalho)
            largura_total = texto_largura + PADDING
            largura_ideal = max(largura_total, MIN_WIDTH)
            self.larguras_calculadas[i] = largura_ideal
            tabela_dados.setColumnWidth(i, int(largura_ideal))
            header.setSectionResizeMode(i, QHeaderView.Interactive)
            item = tabela_dados.horizontalHeaderItem(i)
            if item:
                item.setText(texto_cabecalho)
                item.setTextAlignment(Qt.AlignCenter)
                item.setToolTip(texto_cabecalho)

    except Exception as e:
        logger.error(f"Erro ao ajustar larguras das colunas: {e}", exc_info=True)
        raise
