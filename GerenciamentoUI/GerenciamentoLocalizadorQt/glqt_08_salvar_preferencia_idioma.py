import os
import json
from utils.LogManager import LogManager
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
logger = LogManager.get_logger()

def salvar_preferencia_idioma(self, idioma: str):
    try:
        config_path = os.path.join(obter_caminho_persistente(), "language_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({"idioma": idioma}, f, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erro ao salvar preferência de idioma: {e}", exc_info=True)
