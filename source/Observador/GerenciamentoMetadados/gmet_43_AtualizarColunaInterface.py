from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_coluna_interface(gc, coluna_key=None):
    try:
        with gc.lock_resultados:
            if coluna_key and coluna_key in gc.resultados_colunas:
                resultados = gc.resultados_colunas[coluna_key]
                for item, valor in resultados:
                    pass

                gc.resultados_colunas[coluna_key] = []

    except Exception as e:
        logger.error(f"Erro ao atualizar coluna da interface: {e}", exc_info=True)
