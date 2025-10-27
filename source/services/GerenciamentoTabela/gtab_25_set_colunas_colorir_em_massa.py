from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def set_colunas_colorir_em_massa(self, novas_colunas):
    try:
        self.colunas_para_colorir = set(novas_colunas)
        self.salvar_configuracoes_cores()
        self._invalidar_cache_cores()
        self.atualizar_cores_colunas(aplicar_em_massa=True)

    except Exception as e:
        logger.error(f"Erro ao definir colunas para colorir em massa: {e}", exc_info=True)
