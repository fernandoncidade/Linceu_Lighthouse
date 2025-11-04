from utils.LogManager import LogManager

logger = LogManager.get_logger()

def ocultar_cores(self):
    try:
        self.cores_visiveis = False
        self.atualizar_cores_colunas(aplicar_em_massa=True)

    except Exception as e:
        logger.error(f"Erro ao ocultar cores: {e}", exc_info=True)
