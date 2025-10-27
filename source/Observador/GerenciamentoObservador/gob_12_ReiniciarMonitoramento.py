import time
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def reiniciar_monitoramento(self):
    try:
        self.parar()
        time.sleep(2)
        self.falhas_consecutivas = 0
        self.iniciar()

    except Exception as e:
            logger.error(f"Erro ao reiniciar monitoramento: {e}", exc_info=True)
