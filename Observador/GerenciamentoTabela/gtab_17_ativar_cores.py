from utils.LogManager import LogManager

logger = LogManager.get_logger()

def ativar_cores(self):
    try:
        self.cores_visiveis = True
        self.atualizar_cores_colunas(aplicar_em_massa=True)

    except Exception as e:
        logger.error(f"Erro ao ativar cores: {e}", exc_info=True)
