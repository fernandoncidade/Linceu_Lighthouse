import time
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def processar_buffer_eventos(self):
    INTERVALO_MAXIMO = 0.1
    ULTIMO_PROCESSAMENTO = [time.time()]
    while self.ativo:
        try:
            if not self._pause_event.is_set():
                time.sleep(0.1)
                continue

            processar_agora = False
            with self.evento_lock:
                buffer_len = len(self.buffer_eventos)
                tempo_atual = time.time()
                if buffer_len >= 1:
                    processar_agora = True

                elif buffer_len > 0 and (tempo_atual - ULTIMO_PROCESSAMENTO[0]) >= INTERVALO_MAXIMO:
                    processar_agora = True

                if processar_agora:
                    eventos_para_processar = []
                    for _ in range(min(1, buffer_len)):
                        if self.buffer_eventos:
                            eventos_para_processar.append(self.buffer_eventos.popleft())

                    ULTIMO_PROCESSAMENTO[0] = tempo_atual

                else:
                    eventos_para_processar = []

            for acao, nome_arquivo, tempo_evento in eventos_para_processar:
                if not self._pause_event.is_set() or self.pausado:
                    with self.evento_lock:
                        self.buffer_eventos.appendleft((acao, nome_arquivo, tempo_evento))

                    break

                self._processar_evento_interno(acao, nome_arquivo, tempo_evento)

            if not eventos_para_processar:
                time.sleep(0.01)

            else:
                time.sleep(0.001)

        except Exception as e:
            logger.error(f"Erro ao processar buffer de eventos: {e}", exc_info=True)
            time.sleep(0.1)
