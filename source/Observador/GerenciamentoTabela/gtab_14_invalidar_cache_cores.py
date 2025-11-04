from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _invalidar_cache_cores(self):
    try:
        self._cache_cores.clear()
        self._cache_indices_colunas.clear()

    except Exception as e:
        logger.error(f"Erro ao invalidar cache de cores: {e}", exc_info=True)
