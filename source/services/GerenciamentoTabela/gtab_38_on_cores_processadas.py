from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_cores_processadas(gt, future):
    try:
        resultado = future.result()
        gt.cores_processadas.emit(resultado)

    except Exception as e:
        logger.error(f"Erro ao processar cores: {e}", exc_info=True)
