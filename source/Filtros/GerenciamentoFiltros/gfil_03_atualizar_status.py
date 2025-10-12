from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_status(self, *args):
    try:
        if hasattr(self.parent(), "atualizar_status"):
            self.parent().atualizar_status()

        else:
            if hasattr(self, "label_contagem"):
                self.label_contagem.setText(self.atualizar_contagem())

    except Exception as e:
        logger.error(f"Erro ao atualizar status dos filtros: {e}", exc_info=True)
