from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_pin_toggled(self, index, checked):
    try:
        if checked:
            self._pin_chart(index)

        else:
            self._detach_chart(index)

    except Exception as e:
        logger.error(f"Erro ao alternar pin/detach para chart {index}: {e}", exc_info=True)
