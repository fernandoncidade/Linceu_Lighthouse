import time
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def processar_buffer_eventos(self):
    while self.ativo:
        try:
            if not self._pause_event.is_set():
                time.sleep(0.01)
                continue

            eventos_para_processar = []
            with self.evento_lock:
                while self.buffer_eventos:
                    eventos_para_processar.append(self.buffer_eventos.popleft())

            if not eventos_para_processar:
                time.sleep(0.001)
                continue

            for acao, nome_arquivo, tempo_evento in eventos_para_processar:
                if not self._pause_event.is_set() or self.pausado or not self.ativo:
                    break

                try:
                    self._processar_evento_interno(acao, nome_arquivo, tempo_evento)

                except Exception as e:
                    logger.error(f"Erro ao processar evento {nome_arquivo}: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro crítico ao processar buffer de eventos: {e}", exc_info=True)
            time.sleep(0.1)
