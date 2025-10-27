import os
import json
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def carregar_configuracoes(gc):
    try:
        if os.path.exists(gc.config_path):
            with open(gc.config_path, 'r') as f:
                config = json.load(f)

            for k, v in config.items():
                if k in gc.COLUNAS_DISPONIVEIS:
                    gc.COLUNAS_DISPONIVEIS[k]["visivel"] = v["visivel"]
                    gc.COLUNAS_DISPONIVEIS[k]["ordem"] = v["ordem"]

    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {e}", exc_info=True)
