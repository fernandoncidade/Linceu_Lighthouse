from PySide6.QtCore import QThread, Signal


class WorkerThread(QThread):
    finished = Signal(object)

    def __init__(self, dados, processamento_pesado):
        super().__init__()
        self.dados = dados
        self.processamento_pesado = processamento_pesado

    def run(self):
        resultado = self.processamento_pesado(self.dados)
        self.finished.emit(resultado)
