import time
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def detectar_operacao_massiva(self):
    try:
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_reset_contador >= 1.0:
            if self.contador_eventos_segundo > 100:
                self.operacao_massiva_detectada = True

            elif self.contador_eventos_segundo < 10:
                self.operacao_massiva_detectada = False

            self.contador_eventos_segundo = 0
            self.ultimo_reset_contador = tempo_atual

        self.contador_eventos_segundo += 1

    except Exception as e:
        logger.error(f"Erro ao detectar operação massiva: {e}", exc_info=True)
