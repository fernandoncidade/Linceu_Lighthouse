from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _obter_estados_checkboxes(self):
    try:
        estados = {}
        for titulo, data in self.checkboxes_graficos.items():
            estados[data['grafico_data']['func']] = data['checkbox'].isChecked()

        return estados

    except Exception as e:
        logger.error(f"Erro ao obter estados dos checkboxes: {e}", exc_info=True)
