from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_contagem(self):
    try:
        resultado = self.administrador_filtros.atualizar_contagem()
        return resultado

    except Exception as e:
        logger.error(f"Erro ao atualizar contagem: {e}", exc_info=True)
        return self.loc.get_text("items_count").format(0, 0)
