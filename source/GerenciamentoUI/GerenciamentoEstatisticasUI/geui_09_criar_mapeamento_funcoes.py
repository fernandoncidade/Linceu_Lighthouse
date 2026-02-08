from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_mapeamento_funcoes(self, graficos_atualizados):
    try:
        mapeamento = {}
        for grafico in graficos_atualizados:
            mapeamento[grafico['func']] = grafico['titulo']

        return mapeamento

    except Exception as e:
        logger.error(f"Erro ao criar mapeamento de funções: {e}", exc_info=True)
