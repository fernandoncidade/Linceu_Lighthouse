from utils.LogManager import LogManager
logger = LogManager.get_logger()

def redimensionar_cabecalho(self, logicalIndex, oldSize, newSize):
    try:
        if getattr(self, "_suspender_quebra_cabecalho", False):
            return

        if hasattr(self.interface, 'tabela_dados'):
            self.aplicar_quebra_linha_cabecalho(self.interface.tabela_dados, logicalIndex)
            self.ajustar_altura_cabecalho(self.interface.tabela_dados)

    except Exception as e:
        logger.error(f"Erro ao redimensionar cabeçalho: {e}", exc_info=True)
