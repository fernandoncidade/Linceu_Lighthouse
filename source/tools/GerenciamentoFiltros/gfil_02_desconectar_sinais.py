from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _desconectar_sinais(self):
    try:
        self.loc.idioma_alterado.disconnect(self.on_idioma_alterado)

    except Exception as e:
        logger.error(f"Erro ao desconectar sinais: {e}", exc_info=True)
