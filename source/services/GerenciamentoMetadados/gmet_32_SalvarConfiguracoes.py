import json
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def salvar_configuracoes(gc):
    config = {k: {"visivel": v["visivel"], "ordem": v["ordem"]} for k, v in gc.COLUNAS_DISPONIVEIS.items()}
    try:
        with open(gc.config_path, 'w') as f:
            json.dump(config, f, indent=4)

    except Exception as e:
        logger.error(f"Erro ao salvar configurações: {e}", exc_info=True)
