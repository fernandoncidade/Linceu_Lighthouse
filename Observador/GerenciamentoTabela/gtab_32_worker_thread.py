from PySide6.QtCore import QThread, Signal
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class WorkerThread(QThread):
    finished = Signal(object)

    def __init__(self, dados, processamento_pesado):
        super().__init__()
        try:
            self.dados = dados
            self.processamento_pesado = processamento_pesado

        except Exception as e:
            logger.error(f"Erro ao inicializar WorkerThread: {e}", exc_info=True)

    def run(self):
        try:
            resultado = self.processamento_pesado(self.dados)
            self.finished.emit(resultado)

        except Exception as e:
            logger.error(f"Erro ao executar WorkerThread: {e}", exc_info=True)
