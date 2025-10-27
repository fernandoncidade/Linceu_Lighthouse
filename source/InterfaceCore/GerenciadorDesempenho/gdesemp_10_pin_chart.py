from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _pin_chart(self, index):
    try:
        view = [self.cpu_view, self.mem_view, self.disk_view][index]
        dialog = self.detached_dialogs[index]
        if dialog:
            tabw = dialog.tab_widget
            tab_idx = tabw.indexOf(view)
            if tab_idx != -1:
                try:
                    tabw.removeTab(tab_idx)

                except Exception:
                    pass

            view.setParent(None)
            self.detached_dialogs[index] = None
            self._rebuild_tab_mapping()
            if tabw.count() == 0:
                self._shared_dialog = None
                dialog.close()

        container = self.chart_containers[index]
        container.layout().addWidget(view)
        view.show()
        self._update_shared_dialog_title()

    except Exception as e:
        logger.error(f"Erro ao fixar gráfico {index}: {e}", exc_info=True)
