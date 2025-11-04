from PySide6.QtGui import QFontMetrics
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def ajustar_altura_cabecalho(self, tabela):
    try:
        header = tabela.horizontalHeader()
        font_metrics = QFontMetrics(header.font())

        max_linhas = 1
        for i in range(tabela.columnCount()):
            if not tabela.isColumnHidden(i):
                item = tabela.horizontalHeaderItem(i)
                if item:
                    texto = item.text()
                    linhas = texto.count('\n') + 1
                    max_linhas = max(max_linhas, linhas)

        altura_linha = font_metrics.height()
        altura_necessaria = max_linhas * altura_linha + 10

        header.setMinimumHeight(altura_necessaria)
        header.setMaximumHeight(altura_necessaria)

    except Exception as e:
        logger.error(f"Erro ao ajustar altura do cabeçalho: {e}", exc_info=True)
        raise
