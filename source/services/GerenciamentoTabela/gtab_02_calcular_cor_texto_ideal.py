from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def calcular_cor_texto_ideal(self, cor_fundo, eh_coluna_personalizada=False):
    try:
        if not cor_fundo.isValid() or cor_fundo == QColor() or cor_fundo.alpha() == 0:
            tema = self.detectar_tema_windows()
            return QColor(255, 255, 255) if tema == "escuro" else QColor(0, 0, 0)

        r, g, b = cor_fundo.red(), cor_fundo.green(), cor_fundo.blue()

        r_linear = r / 255.0
        g_linear = g / 255.0
        b_linear = b / 255.0

        r_srgb = r_linear <= 0.03928 and r_linear/12.92 or ((r_linear+0.055)/1.055)**2.4
        g_srgb = g_linear <= 0.03928 and g_linear/12.92 or ((g_linear+0.055)/1.055)**2.4
        b_srgb = b_linear <= 0.03928 and b_linear/12.92 or ((b_linear+0.055)/1.055)**2.4

        luminosidade = 0.2126 * r_srgb + 0.7152 * g_srgb + 0.0722 * b_srgb

        if (r, g, b) == (255, 0, 255):
            return QColor(0, 0, 0)

        if eh_coluna_personalizada:
            return QColor(255, 255, 255) if luminosidade <= 0.5 else QColor(0, 0, 0)

        if hasattr(self, '_eh_cor_padrao_qualquer_tema') and self._eh_cor_padrao_qualquer_tema(cor_fundo):
            tema = self.detectar_tema_windows()
            return QColor(255, 255, 255) if tema == "escuro" else QColor(0, 0, 0)

        tema = self.detectar_tema_windows()
        if tema == "claro":
            return QColor(0, 0, 0) if luminosidade >= 0.4 else QColor(255, 255, 255)

        else:
            return QColor(255, 255, 255) if luminosidade <= 0.6 else QColor(0, 0, 0)

    except Exception as e:
        logger.error(f"Erro ao calcular cor do texto ideal: {e}", exc_info=True)
        tema = self.detectar_tema_windows() if hasattr(self, 'detectar_tema_windows') else "claro"
        return QColor(255, 255, 255) if tema == "escuro" else QColor(0, 0, 0)

def _eh_cor_fundo_padrao(self, cor):
    try:
        palette = QApplication.palette()
        cor_base = palette.color(QPalette.ColorRole.Base)
        cor_alternativa = palette.color(QPalette.ColorRole.AlternateBase)
        cor_janela = palette.color(QPalette.ColorRole.Window)

        return (abs(cor.red() - cor_base.red()) < 10 and 
                abs(cor.green() - cor_base.green()) < 10 and 
                abs(cor.blue() - cor_base.blue()) < 10) or \
               (abs(cor.red() - cor_alternativa.red()) < 10 and 
                abs(cor.green() - cor_alternativa.green()) < 10 and 
                abs(cor.blue() - cor_alternativa.blue()) < 10) or \
               (abs(cor.red() - cor_janela.red()) < 10 and 
                abs(cor.green() - cor_janela.green()) < 10 and 
                abs(cor.blue() - cor_janela.blue()) < 10)

    except Exception as e:
        logger.error(f"Erro ao verificar cor de fundo padrão: {e}", exc_info=True)
        return False
