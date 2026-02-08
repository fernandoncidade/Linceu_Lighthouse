from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def traduzir_tipo_operacao(self, valor, idioma_origem=None):
    try:
        if self.tradutor_metadados:
            return self.tradutor_metadados.traduzir_tipo_operacao(valor, idioma_origem)

        else:
            return self._traduzir_tipo_operacao_fallback(valor)

    except Exception as e:
        logger.error(f"Erro ao traduzir tipo de operação: {e}", exc_info=True)
