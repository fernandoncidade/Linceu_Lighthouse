from utils.LogManager import LogManager

logger = LogManager.get_logger()

def _processar_evento_interno(self, acao, nome_arquivo, tempo_evento):
    try:
        if self.pausado or not self._pause_event.is_set():
            with self.evento_lock:
                self.buffer_eventos.appendleft((acao, nome_arquivo, tempo_evento))

            return

        self.total_eventos_processados += 1
        self.processar_evento(acao, nome_arquivo, tempo_evento)

    except Exception as e:
        logger.error(f"Erro ao processar evento interno: {e}", exc_info=True)
