from utils.LogManager import LogManager
logger = LogManager.get_logger()

def shutdown_executors(gt):
    try:
        if hasattr(gt, '_monitor_tema') and gt._monitor_tema:
            gt._monitor_tema.parar_monitoramento()
            logger.debug("Monitor de tema parado com sucesso")

        if hasattr(gt, '_selection_executor') and gt._selection_executor:
            gt._selection_executor.shutdown(wait=True)
            logger.debug("Selection executor encerrado com sucesso")

        if hasattr(gt, 'executor') and gt.executor:
            gt.executor.shutdown(wait=True)
            logger.debug("Main executor encerrado com sucesso")

    except Exception as e:
        logger.error(f"Erro ao encerrar executors: {e}", exc_info=True)
