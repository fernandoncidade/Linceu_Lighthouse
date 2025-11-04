from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_traducoes(self):
    try:
        try:
            cpu_title = self.interface.loc.get_text("CPU_Porcentagem")
            mem_title = self.interface.loc.get_text("Memoria_RAM_Porcentagem")
            disk_title = self.interface.loc.get_text("Discos_Porcentagem")

            if self.cpu_view.chart():
                self.cpu_view.chart().setTitle(cpu_title)

            if self.mem_view.chart():
                self.mem_view.chart().setTitle(mem_title)

            if self.disk_view.chart():
                try:
                    self._update_disk_chart_title()

                except Exception:
                    self.disk_view.chart().setTitle(disk_title)

        except Exception as e:
            logger.error(f"Erro ao atualizar títulos dos gráficos: {e}", exc_info=True)

        try:
            labels = [
                ("CPU", "CPU_Porcentagem"),
                ("RAM", "Memoria_RAM_Porcentagem"), 
                ("Discos", "Discos_Porcentagem")
            ]

            for i, (key_short, key_full) in enumerate(labels):
                if i < len(self.chart_containers) and self.chart_containers[i]:
                    header_widget = self.pin_buttons[i].parent()
                    if header_widget and header_widget.layout():
                        for j in range(header_widget.layout().count()):
                            item = header_widget.layout().itemAt(j)
                            if item and item.widget() and isinstance(item.widget(), type(self.pin_buttons[i].parent().layout().itemAt(0).widget())):
                                label_widget = item.widget()
                                label_widget.setText(self.interface.loc.get_text(key_full))
                                label_widget.setToolTip(self.interface.loc.get_text(key_full))

        except Exception as e:
            logger.error(f"Erro ao atualizar labels dos botões: {e}", exc_info=True)

        if self._shared_dialog and self._shared_dialog.isVisible():
            try:
                self._shared_dialog.setWindowTitle(self.interface.loc.get_text("performance_charts"))

                labels_tab = [
                    self.interface.loc.get_text("CPU_Porcentagem"),
                    self.interface.loc.get_text("Memoria_RAM_Porcentagem"),
                    self.interface.loc.get_text("Discos_Porcentagem")
                ]

                tabw = self._shared_dialog.tab_widget
                for chart_index, view in enumerate([self.cpu_view, self.mem_view, self.disk_view]):
                    idx_tab = tabw.indexOf(view)
                    if idx_tab != -1:
                        tabw.setTabText(idx_tab, labels_tab[chart_index])

                self._update_shared_dialog_title()

            except Exception as e:
                logger.error(f"Erro ao atualizar título da janela destacada: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro geral ao atualizar traduções: {e}", exc_info=True)
