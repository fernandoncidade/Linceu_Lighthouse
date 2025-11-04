from utils.LogManager import LogManager
logger = LogManager.get_logger()

def copiar_selecionados(self):
    try:
        caminhos = self.obter_selecionados()
        if caminhos:
            self.clipboard_items = [(caminho, 'copy') for caminho in caminhos]
            logger.info(f"Copiados {len(caminhos)} itens para área de transferência")

    except Exception as e:
        logger.error(f"Erro ao copiar selecionados: {e}", exc_info=True)
