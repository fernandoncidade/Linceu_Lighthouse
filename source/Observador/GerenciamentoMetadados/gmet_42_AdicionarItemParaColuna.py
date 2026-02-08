from utils.LogManager import LogManager
logger = LogManager.get_logger()

def adicionar_item_para_coluna(gc, coluna_key, item):
    try:
        if coluna_key in gc.filas_colunas:
            gc.filas_colunas[coluna_key].put(item)

    except Exception as e:
        logger.error(f"Erro ao adicionar item para a coluna '{coluna_key}': {e}", exc_info=True)
