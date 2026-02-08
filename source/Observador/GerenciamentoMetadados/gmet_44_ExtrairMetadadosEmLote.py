from utils.LogManager import LogManager
logger = LogManager.get_logger()

def extrair_metadados_em_lote(gc, lista_itens):
    try:
        futuros = []
        for item in lista_itens:
            futuros.append(gc.executor_metadados.submit(gc.get_metadados, item))

        for futuro in futuros:
            futuro.add_done_callback(gc._metadados_extraidos_callback)

    except Exception as e:
        logger.error(f"Erro ao extrair metadados em lote: {e}", exc_info=True)
