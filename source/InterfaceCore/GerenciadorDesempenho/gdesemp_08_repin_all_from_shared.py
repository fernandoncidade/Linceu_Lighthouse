from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _repin_all_from_shared(self):
    try:
        if not self._shared_dialog:
            return

        idxs = [i for i, d in enumerate(self.detached_dialogs) if d == self._shared_dialog]
        for i in idxs:
            if self.pin_buttons[i].isChecked() is False:
                self.pin_buttons[i].setChecked(True)

    except Exception as e:
        logger.error(f"Erro ao repin all from shared: {e}", exc_info=True)

    finally:
        self._shared_dialog = None
        self._tab_for_chart.clear()
