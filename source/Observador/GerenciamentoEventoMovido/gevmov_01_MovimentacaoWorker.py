import threading
from PySide6.QtCore import QObject, Signal
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class MovimentacaoWorker(QObject):
    processamento_concluido = Signal()
    atualizacao_progresso = Signal(int, int)

    def __init__(self, interface, parent=None):
        super().__init__(parent)
        self.interface = interface
        self.evento_base = interface.evento_base
        self.mutex = threading.Lock()

    def adicionar_evento(self, evento):
        try:
            with self.mutex:
                threading.Thread(target=self._processar_evento_individual, args=(evento,), daemon=True).start()

        except Exception as e:
            logger.error(f"Erro em MovimentacaoWorker.adicionar_evento: {e}", exc_info=True)

    def _processar_evento_individual(self, evento):
        try:
            self.atualizacao_progresso.emit(0, 1)
            self.evento_base.processar_eventos_movimentacao([evento], self._concluir_processamento)
            self.atualizacao_progresso.emit(1, 1)

        except Exception as e:
            logger.error(f"Erro ao processar evento individual: {e}", exc_info=True)
            self._concluir_processamento()

    def _concluir_processamento(self):
        try:
            self.processamento_concluido.emit()
            if hasattr(self.interface, 'gerenciador_tabela'):
                self.interface.gerenciador_tabela.atualizacao_pendente = True

        except Exception as e:
            logger.error(f"Erro em MovimentacaoWorker._concluir_processamento: {e}", exc_info=True)
