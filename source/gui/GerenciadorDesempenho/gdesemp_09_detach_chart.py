from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class _SharedDetachDialog(QDialog):
    def __init__(self, parent, on_about_to_close):
        super().__init__(parent)
        self._on_about_to_close = on_about_to_close
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(False)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        layout.addWidget(self.tab_widget)

    def closeEvent(self, event):
        try:
            if self._on_about_to_close:
                self._on_about_to_close()

        finally:
            super().closeEvent(event)

def _detach_chart(self, index):
    try:
        if self.detached_dialogs[index] and self._shared_dialog and self.detached_dialogs[index] == self._shared_dialog:
            self._shared_dialog.raise_()
            self._shared_dialog.activateWindow()
            return

        view = [self.cpu_view, self.mem_view, self.disk_view][index]
        parent = view.parent()
        if parent:
            try:
                parent.layout().removeWidget(view)

            except Exception:
                pass

        view.setParent(None)

        if hasattr(self.interface, "loc") and hasattr(self.interface.loc, "carregar_preferencia_idioma"):
            idioma_salvo = self.interface.loc.carregar_preferencia_idioma()
            if hasattr(self.interface.loc, "set_idioma"):
                self.interface.loc.set_idioma(idioma_salvo)

        if not self._shared_dialog:
            flags = (
                Qt.Window |
                Qt.WindowTitleHint |
                Qt.WindowSystemMenuHint |
                Qt.WindowMinimizeButtonHint |
                Qt.WindowMaximizeButtonHint |
                Qt.WindowCloseButtonHint
            )

            self._shared_dialog = _SharedDetachDialog(self.interface, on_about_to_close=self._repin_all_from_shared)
            self._shared_dialog.setWindowFlags(flags)
            self._shared_dialog.resize(620, 460)

            try:
                if hasattr(self.interface, "loc"):
                    title = self.interface.loc.get_text("performance_charts")

                else:
                    title = self.interface.get_text("performance_charts")

            except Exception:
                title = "Gráficos de Desempenho Destacados"

            self._shared_dialog.setWindowTitle(title)

        try:
            if hasattr(self.interface, "loc"):
                labels_tab = [
                    self.interface.loc.get_text("CPU_Porcentagem"),
                    self.interface.loc.get_text("Memoria_RAM_Porcentagem"),
                    self.interface.loc.get_text("Discos_Porcentagem")
                ]

            else:
                labels_tab = [
                    self.interface.get_text("CPU_Porcentagem"),
                    self.interface.get_text("Memoria_RAM_Porcentagem"),
                    self.interface.get_text("Discos_Porcentagem")
                ]

        except Exception:
            labels_tab = ["CPU (%)", "Memória RAM (%)", "Discos (%)"]

        tabw = self._shared_dialog.tab_widget
        if tabw.indexOf(view) == -1:
            tab_index = tabw.addTab(view, labels_tab[index])
            self._tab_for_chart[index] = tab_index

        self.detached_dialogs[index] = self._shared_dialog
        if not self._shared_dialog.isVisible():
            self._shared_dialog.show()

        self._update_shared_dialog_title()

    except Exception as e:
        logger.error(f"Erro ao destacar gráfico {index}: {e}", exc_info=True)
        try:
            self.pin_buttons[index].setChecked(True)

        except Exception:
            pass
