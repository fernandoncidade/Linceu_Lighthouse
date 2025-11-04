from utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_cor(self):
    try:
        resultado = self.cor_selecionada if self.cor_selecionada else self.cor_atual
        return resultado

    except Exception as e:
        logger.error(f"Erro ao obter cor: {e}", exc_info=True)
