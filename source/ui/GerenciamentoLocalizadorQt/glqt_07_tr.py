from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def tr(self, text: str, *args) -> str:
    try:
        return self.get_text(text, *args)

    except Exception as e:
        logger.error(f"Erro ao traduzir texto: {e}", exc_info=True)

