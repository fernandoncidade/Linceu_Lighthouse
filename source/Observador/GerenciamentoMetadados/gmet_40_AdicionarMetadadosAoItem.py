from utils.LogManager import LogManager
logger = LogManager.get_logger()

def adicionar_metadados_ao_item(gc, item):
    try:
        metadados = gc.get_metadados(item)
        if metadados:
            for campo, valor in metadados.items():
                if campo not in item or not item[campo]:
                    item[campo] = valor

        return item

    except Exception as e:
        logger.error(f"Erro ao adicionar metadados ao item: {e}", exc_info=True)
        return item
