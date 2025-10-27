import os
import json
from source.utils.LogManager import LogManager
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
logger = LogManager.get_logger()

def _carregar_configuracoes_cores(self):
    try:
        if not hasattr(self.interface, "gerenciador_colunas"):
            return

        config_path = os.path.join(obter_caminho_persistente(), "colunas_coloridas.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.colunas_para_colorir = set(data.get("colunas_para_colorir", []))

        if hasattr(self.interface, "gerenciador_menus_ui") and hasattr(self.interface.gerenciador_menus_ui, "criar_menu_principal"):
            self.interface.gerenciador_menus_ui.criar_menu_principal()

        self._invalidar_cache_cores()
        self.aplicar_cores_todas_colunas()

    except Exception as e:
        logger.error(f"Erro ao carregar configuração de colunas coloridas: {e}", exc_info=True)
