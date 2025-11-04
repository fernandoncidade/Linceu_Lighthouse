from utils.LogManager import LogManager
logger = LogManager.get_logger()

def cortar_selecionados(self):
    try:
        caminhos = self.obter_selecionados()
        if caminhos:
            self.clipboard_items = [(caminho, 'cut') for caminho in caminhos]
            logger.info(f"Cortados {len(caminhos)} itens para área de transferência")

    except Exception as e:
        logger.error(f"Erro ao cortar selecionados: {e}", exc_info=True)
