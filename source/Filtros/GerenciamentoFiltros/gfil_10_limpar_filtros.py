from utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_filtros(self):
    try:
        self.administrador_filtros.limpar_filtros()
        self.filtroAplicado.emit()

    except Exception as e:
        logger.error(f"Erro ao limpar filtros: {e}", exc_info=True)
