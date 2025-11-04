from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def set_coluna_colorir(self, coluna_key, checked):
    try:
        if checked:
            self.colunas_para_colorir.add(coluna_key)
            self.salvar_configuracoes_cores()
            self._invalidar_cache_cores()
            self.aplicar_cores_todas_colunas()

        else:
            self.colunas_para_colorir.discard(coluna_key)
            self.salvar_configuracoes_cores()
            self._invalidar_cache_cores()
            self.remover_cor_coluna(coluna_key)

    except Exception as e:
        logger.error(f"Erro ao definir cor da coluna '{coluna_key}': {e}", exc_info=True)
