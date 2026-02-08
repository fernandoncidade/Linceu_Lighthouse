import os
import json
from utils.LogManager import LogManager
from utils.CaminhoPersistenteUtils import obter_caminho_persistente

logger = LogManager.get_logger()

def salvar_configuracoes_cores(self):
    try:
        config_path = os.path.join(obter_caminho_persistente(), "colunas_coloridas.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"colunas_para_colorir": list(self.colunas_para_colorir)}, f)

        logger.info(f"Configuração de colunas coloridas salva em: {config_path}")

    except Exception as e:
        logger.error(f"Erro ao salvar configuração de colunas coloridas: {e}")
