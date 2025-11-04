from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _rebuild_tab_mapping(self):
    try:
        if not self._shared_dialog:
            self._tab_for_chart.clear()
            return

        tabw = self._shared_dialog.tab_widget
        self._tab_for_chart.clear()
        views = [self.cpu_view, self.mem_view, self.disk_view]
        for chart_index, view in enumerate(views):
            idx_tab = tabw.indexOf(view)
            if idx_tab != -1:
                self._tab_for_chart[chart_index] = idx_tab

    except Exception as e:
        logger.error(f"Erro ao reconstruir mapeamento de abas: {e}", exc_info=True)
