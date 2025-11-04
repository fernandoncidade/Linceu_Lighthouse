from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _get_size_unit(gc, item, unidade):
    try:
        tamanho_bytes = gc._get_tamanho_bytes(item)
        if unidade == "B":
            return int(tamanho_bytes)

        elif unidade == "KB":
            return round(tamanho_bytes / 1024, 2)

        elif unidade == "MB":
            return round(tamanho_bytes / 1024**2, 2)

        elif unidade == "GB":
            return round(tamanho_bytes / 1024**3, 2)

        elif unidade == "TB":
            return round(tamanho_bytes / 1024**4, 2)

        return 0

    except Exception as e:
        logger.error(f"Erro ao obter unidade de tamanho: {e}", exc_info=True)
