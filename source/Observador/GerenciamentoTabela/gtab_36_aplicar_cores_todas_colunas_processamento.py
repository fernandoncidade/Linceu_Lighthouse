from utils.LogManager import LogManager
logger = LogManager.get_logger()

def aplicar_cores_todas_colunas_processamento(gt, dados):
    try:
        future = gt.executor.submit(gt._processar_cores_em_background, dados)
        future.add_done_callback(gt._on_cores_processadas)

    except Exception as e:
        logger.error(f"Erro ao aplicar cores a todas as colunas: {e}", exc_info=True)
