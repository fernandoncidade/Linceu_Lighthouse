from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def shutdown_executors(gt):
    try:
        if hasattr(gt, '_monitor_tema') and gt._monitor_tema:
            gt._monitor_tema.parar_monitoramento()

        if hasattr(gt, '_selection_executor') and gt._selection_executor:
            gt._selection_executor.shutdown(wait=True)

        if hasattr(gt, 'executor') and gt.executor:
            gt.executor.shutdown(wait=True)

    except Exception as e:
        logger.error(f"Erro ao encerrar executors: {e}", exc_info=True)
