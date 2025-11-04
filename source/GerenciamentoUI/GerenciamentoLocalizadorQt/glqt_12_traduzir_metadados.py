from utils.LogManager import LogManager
logger = LogManager.get_logger()

def traduzir_metadados(self, valor, campo):
    try:
        if self.tradutor_metadados:
            return self.tradutor_metadados.traduzir_metadados(valor, campo)

        else:
            return valor

    except Exception as e:
        logger.error(f"Erro ao traduzir metadados: {e}", exc_info=True)
