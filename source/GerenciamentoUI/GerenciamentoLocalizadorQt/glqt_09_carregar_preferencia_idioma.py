import os
import json
from source.utils.LogManager import LogManager
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
logger = LogManager.get_logger()

def carregar_preferencia_idioma(self):
    try:
        config_path = os.path.join(obter_caminho_persistente(), "language_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                idioma = config.get("idioma", self.system_locale)

                if idioma not in self.idiomas_suportados:
                    idioma = "pt_BR"

                return idioma

        else:
            idioma = "pt_BR" if self.system_locale not in self.idiomas_suportados else self.system_locale
            self.salvar_preferencia_idioma(idioma)
            return idioma

    except Exception as e:
        logger.error(f"Erro ao carregar preferência de idioma: {e}", exc_info=True)
        return "pt_BR"
