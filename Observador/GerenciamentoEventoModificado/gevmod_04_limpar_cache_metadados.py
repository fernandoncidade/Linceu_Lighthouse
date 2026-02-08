from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _limpar_cache_metadados(self, caminho_completo, ext):
    try:
        if ext == '.txt' and hasattr(self.observador, 'gerenciador_colunas'):
            if hasattr(self.observador.gerenciador_colunas, 'cache_metadados'):
                with self.observador.gerenciador_colunas.lock_cache:
                    if caminho_completo in self.observador.gerenciador_colunas.cache_metadados:
                        del self.observador.gerenciador_colunas.cache_metadados[caminho_completo]

            if hasattr(self.observador.gerenciador_colunas, 'metadados_cache'):
                if caminho_completo in self.observador.gerenciador_colunas.metadados_cache:
                    del self.observador.gerenciador_colunas.metadados_cache[caminho_completo]

        if hasattr(self.observador, 'gerenciador_colunas'):
            if hasattr(self.observador.gerenciador_colunas, 'cache_metadados'):
                with self.observador.gerenciador_colunas.lock_cache:
                    if caminho_completo in self.observador.gerenciador_colunas.cache_metadados:
                        del self.observador.gerenciador_colunas.cache_metadados[caminho_completo]

            if hasattr(self.observador.gerenciador_colunas, 'metadados_cache'):
                if caminho_completo in self.observador.gerenciador_colunas.metadados_cache:
                    del self.observador.gerenciador_colunas.metadados_cache[caminho_completo]

    except Exception as e:
        logger.error(f"Erro ao limpar cache de metadados: {e}", exc_info=True)
