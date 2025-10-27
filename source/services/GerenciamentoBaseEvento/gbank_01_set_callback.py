from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def set_callback(self, callback):
    try:
        self.callback = callback

    except Exception as e:
        logger.error(f"Erro ao definir callback: {e}", exc_info=True)
