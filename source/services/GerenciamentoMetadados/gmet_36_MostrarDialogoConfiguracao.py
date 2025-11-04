from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mostrar_dialogo_configuracao(gc, pos=None):
    try:
        gc.gerenciador_tabela.mostrar_dialogo_configuracao(pos)

    except Exception as e:
        logger.error(f"Erro ao mostrar diálogo de configuração: {e}", exc_info=True)
