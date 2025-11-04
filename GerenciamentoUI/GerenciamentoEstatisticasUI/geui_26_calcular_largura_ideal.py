from PySide6.QtGui import QFont, QFontMetrics

def _calcular_largura_ideal(self, graficos):
    font = QFont()
    font_metrics = QFontMetrics(font)

    max_text_width = 0

    for grafico in graficos:
        text_width = font_metrics.horizontalAdvance(grafico["titulo"])
        max_text_width = max(max_text_width, text_width)

    textos_interface = [
        self.loc.get_text("save_selected"),
        self.loc.get_text("save_all"),
        self.loc.get_text("refresh"),
        self.loc.get_text("select_all"),
        self.loc.get_text("select_graphs")
    ]

    for texto in textos_interface:
        text_width = font_metrics.horizontalAdvance(texto)
        max_text_width = max(max_text_width, text_width)

    checkbox_padding = 40
    scroll_padding = 30 
    min_panel_width = max_text_width + checkbox_padding + scroll_padding

    max_width = max(min_panel_width, 200)
    max_width = min(max_width, 400)

    return max_width
