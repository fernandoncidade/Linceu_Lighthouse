from PySide6.QtGui import QColor, QIcon, QPixmap, QPainter
from PySide6.QtCore import Qt
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_icone_cor(self, cor_hex):
    try:
        tamanho = 16
        pixmap = QPixmap(tamanho, tamanho)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(cor_hex))
        painter.drawRect(0, 0, tamanho, tamanho)
        painter.end()
        return QIcon(pixmap)

    except Exception as e:
        logger.error(f"Erro ao criar ícone de cor: {e}", exc_info=True)
