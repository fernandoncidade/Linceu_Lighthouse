from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def verificar_filtro_operacao(self, tipo_operacao_traduzido):
    try:
        resultado = self.administrador_filtros.verificar_filtro_operacao(tipo_operacao_traduzido)
        return resultado

    except Exception as e:
        logger.error(f"Erro ao verificar filtro de operação: {e}", exc_info=True)
        return True
