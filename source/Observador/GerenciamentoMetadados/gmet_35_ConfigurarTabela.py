from utils.LogManager import LogManager
logger = LogManager.get_logger()

def configurar_tabela(gc, tabela):
    try:
        gc.gerenciador_tabela.configurar_tabela(tabela)

    except Exception as e:
        logger.error(f"Erro ao configurar tabela: {e}", exc_info=True)
