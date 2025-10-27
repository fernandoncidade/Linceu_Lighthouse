from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtWidgets import QPushButton
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class BotaoRotacionado(QPushButton):
    def __init__(self, texto, parent=None):
        try:
            super().__init__(texto, parent)
            self.setText(texto)
            self._calcular_tamanho()

        except Exception as e:
            logger.error(f"Erro ao inicializar BotaoRotacionado: {e}", exc_info=True)

    def setText(self, texto):
        try:
            super().setText(texto)
            self._calcular_tamanho()

        except Exception as e:
            logger.error(f"Erro ao definir texto do BotaoRotacionado: {e}", exc_info=True)

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.save()
            if self.isDown():
                painter.fillRect(self.rect(), self.palette().button().color().darker(110))

            else:
                painter.fillRect(self.rect(), self.palette().button().color())

            painter.setPen(self.palette().dark().color())
            painter.drawRect(0, 0, self.width()-1, self.height()-1)
            painter.translate(0, self.height())
            painter.rotate(270)

            fm = painter.fontMetrics()
            texto_largura = fm.horizontalAdvance(self.text())
            x = (self.height() - texto_largura) / 2
            y = (self.width() + fm.ascent() - fm.descent()) / 2
            if self.isEnabled():
                painter.setPen(self.palette().buttonText().color())

            else:
                painter.setPen(self.palette().disabled().buttonText().color())

            painter.drawText(x, y, self.text())
            painter.restore()

        except Exception as e:
            logger.error(f"Erro ao pintar BotaoRotacionado: {e}", exc_info=True)

    def _calcular_tamanho(self):
        try:
            fm = QFontMetrics(self.font())
            texto_largura = fm.horizontalAdvance(self.text())
            texto_altura = fm.height()
            largura_botao = texto_altura + 5
            altura_botao = texto_largura + 20
            self.setFixedSize(QSize(largura_botao, altura_botao))

        except Exception as e:
            logger.error(f"Erro ao calcular tamanho do BotaoRotacionado: {e}", exc_info=True)
