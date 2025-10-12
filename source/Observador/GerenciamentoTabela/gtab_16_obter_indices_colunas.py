from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _obter_indices_colunas(self, tabela):
    try:
        if not self._cache_indices_colunas:
            for i in range(tabela.columnCount()):
                item = tabela.horizontalHeaderItem(i)
                if item:
                    self._cache_indices_colunas[item.text().replace('\n', ' ').strip()] = i

        return self._cache_indices_colunas

    except Exception as e:
        logger.error(f"Erro ao obter índices de colunas: {e}", exc_info=True)
        return {}
