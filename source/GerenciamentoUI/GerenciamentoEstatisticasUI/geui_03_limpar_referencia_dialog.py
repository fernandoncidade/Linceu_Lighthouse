from utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_referencia_dialog(self):
    try:
        self.dialog_estatisticas = None
        self.checkboxes_graficos.clear()
        self.graficos_dados.clear()
        self.painel_selecao = None
        self.splitter = None

    except Exception as e:
        logger.error(f"Erro ao limpar referências do diálogo: {e}", exc_info=True)
