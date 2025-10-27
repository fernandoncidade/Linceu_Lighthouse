from PySide6.QtWidgets import QPushButton
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class BotaoCor(QPushButton):
    def __init__(self, cor, tamanho=30):
        super().__init__()
        self.cor = cor
        self.setFixedSize(tamanho, tamanho)
        self.setStyleSheet(f"background-color: {cor}; border: 1px solid #888888;")
        self.setToolTip(cor)

def _adicionar_grid_cores(self, grid_layout, lista_cores, colunas):
    try:
        row, col = 0, 0
        for cor_hex in lista_cores:
            botao = BotaoCor(cor_hex)
            botao.clicked.connect(lambda checked=False, c=cor_hex: self._selecionar_cor(c))
            grid_layout.addWidget(botao, row, col)

            col += 1
            if col >= colunas:
                col = 0
                row += 1

    except Exception as e:
        logger.error(f"Erro ao adicionar grade de cores: {e}", exc_info=True)
