from source.utils.LogManager import LogManager
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from source.utils.IconUtils import get_icon_path
logger = LogManager.get_logger()


class GerenciadorBotoesUI:
    def __init__(self, parent):
        self.parent = parent
        self.buttons_data = []

    def add_button_with_label(self, layout, label_text, icon_name, callback, icon_path=None, translation_key=None):
        try:
            layout_h = QHBoxLayout()
            label = QLabel(label_text, self.parent)
            layout_h.addWidget(label)

            button = self.create_button()
            icon_file = get_icon_path(icon_name)
            button.setIcon(QIcon(icon_file))
            button.clicked.connect(callback)
            layout_h.addWidget(button)
            layout.addLayout(layout_h)

            if translation_key is None:
                translation_key = label_text

            self.buttons_data.append({'label': label, 'translation_key': translation_key})
            return button

        except Exception as e:
            logger.error(f"Erro ao adicionar botão: {e}", exc_info=True)

    def update_buttons_text(self, loc):
        try:
            for entry in self.buttons_data:
                entry['label'].setText(loc.get_text(entry['translation_key']))

        except Exception as e:
            logger.error(f"Erro ao atualizar texto dos botões: {e}", exc_info=True)

    def create_button(self):
        try:
            button = QPushButton()
            button.setMinimumWidth(3 * button.fontMetrics().horizontalAdvance('m'))
            button.setMaximumWidth(3 * button.fontMetrics().horizontalAdvance('m'))
            button.setFont(QFont('Arial', 9))
            return button

        except Exception as e:
            logger.error(f"Erro ao criar botão: {e}", exc_info=True)
