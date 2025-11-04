from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_mapa_compatibilidade(self):
    try:
        return {
            idioma: {
                "select_all_columns": "select_all_columns",
                "deselect_all_columns": "deselect_all_columns",
            }
            for idioma in self.idiomas_suportados.keys()
        }

    except Exception as e:
        logger.error(f"Erro ao criar mapa de compatibilidade: {e}", exc_info=True)
