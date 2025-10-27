from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _alternar_todos_checkboxes(self):
    try:
        if self.checkbox_todos.checkState() == Qt.PartiallyChecked:
            self.checkbox_todos.setCheckState(Qt.Checked)

        checked = self.checkbox_todos.checkState() == Qt.Checked
        self.checkbox_todos.blockSignals(True)
        for titulo, data in self.checkboxes_graficos.items():
            checkbox = data['checkbox']
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

        self.checkbox_todos.blockSignals(False)

    except Exception as e:
        logger.error(f"Erro ao alternar todos os checkboxes: {e}", exc_info=True)
