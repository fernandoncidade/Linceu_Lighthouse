import queue
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_fila(self):
    while True:
        try:
            item, caminho, tipo = self.fila_processamento.get(timeout=1)
            self._processar_item(item, caminho, tipo)
            self.fila_processamento.task_done()
            self.contador_processados += 1

        except queue.Empty:
            break

        except Exception as e:
            logger.error(f"Erro no processamento: {e}", exc_info=True)
            self.fila_processamento.task_done()
