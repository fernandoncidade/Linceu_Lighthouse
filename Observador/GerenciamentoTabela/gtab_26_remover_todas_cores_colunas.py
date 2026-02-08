from utils.LogManager import LogManager

logger = LogManager.get_logger()

def remover_todas_cores_colunas(self):
    try:
        self.colunas_para_colorir.clear()
        self.salvar_configuracoes_cores()
        self._invalidar_cache_cores()
        self.atualizar_cores_colunas(aplicar_em_massa=True)

    except Exception as e:
        logger.error(f"Erro ao remover todas as cores das colunas: {e}")
