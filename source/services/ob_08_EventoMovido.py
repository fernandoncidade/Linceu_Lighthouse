from PySide6.QtCore import QMutexLocker, QTimer, QObject, Signal, QMutex, QThreadPool
from PySide6.QtWidgets import QApplication
from source.services.GerenciamentoEventoMovido.gevmov_02_verificar_movimentacao import verificar_movimentacao
from source.services.GerenciamentoEventoMovido.gevmov_03_remover_exclusao import _remover_exclusao
from source.services.GerenciamentoEventoMovido.gevmov_04_atualizar_linha_recente import _atualizar_linha_recente
from source.services.GerenciamentoEventoMovido.gevmov_05_atualizar_tabela_completa import _atualizar_tabela_completa
from source.services.GerenciamentoEventoMovido.gevmov_06_inicializar_sistema_evento import _inicializar_sistema_evento
from source.services.GerenciamentoEventoMovido.gevmov_07_processar_exclusoes_pendentes import _processar_exclusoes_pendentes
from source.services.GerenciamentoEventoMovido.gevmov_08_adicionar_item_tabela import _adicionar_item_tabela
from source.services.GerenciamentoEventoMovido.gevmov_09_adicionar_evento import adicionar_evento
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class EventoRunnable(QObject):
    concluido = Signal(dict)

    def __init__(self, evento, func_processar):
        super().__init__()
        self.evento = evento
        self.func_processar = func_processar

    def run(self):
        try:
            resultado = self.func_processar(self.evento)
            if resultado:
                self.concluido.emit(resultado)

        except Exception as e:
            logger.error(f"Erro em EventoRunnable.run: {e}", exc_info=True)


class EventoMovido(QObject):
    evento_processado = Signal(dict)
    eventos_em_lote_processados = Signal(list)

    def __init__(self):
        super().__init__()
        self.eventos_pendentes = []
        self.eventos_lock = QMutex()
        self.processamento_timer = QTimer()
        self.processamento_timer.timeout.connect(self.processar_lote)
        self.processamento_timer.start(100)
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(10)

    def processar_evento(self, evento):
        try:
            self.evento_processado.emit(evento)

        except Exception as e:
            logger.error(f"Erro em EventoMovido.processar_evento: {e}", exc_info=True)

    def adicionar_evento_para_lote(self, evento):
        try:
            with QMutexLocker(self.eventos_lock):
                self.eventos_pendentes.append(evento)

        except Exception as e:
            logger.error(f"Erro em EventoMovido.adicionar_evento_para_lote: {e}", exc_info=True)

    def processar_lote(self):
        try:
            eventos_para_processar = []
            with QMutexLocker(self.eventos_lock):
                if self.eventos_pendentes:
                    eventos_para_processar = self.eventos_pendentes.copy()
                    self.eventos_pendentes.clear()

            if eventos_para_processar:
                self.eventos_em_lote_processados.emit(eventos_para_processar)

        except Exception as e:
            logger.error(f"Erro em EventoMovido.processar_lote: {e}", exc_info=True)

verificar_movimentacao = verificar_movimentacao
_remover_exclusao = _remover_exclusao
_atualizar_linha_recente = _atualizar_linha_recente
_atualizar_tabela_completa = _atualizar_tabela_completa
_inicializar_sistema_evento = _inicializar_sistema_evento
_processar_exclusoes_pendentes = _processar_exclusoes_pendentes
_adicionar_item_tabela = _adicionar_item_tabela
adicionar_evento = adicionar_evento


class EventoBuffer:
    def __init__(self, interface_monitor):
        self.interface = interface_monitor
        self.lock = QMutex()
        self.ultimo_update = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(250)
        self.eventos_pendentes = []

    def adicionar_evento(self, evento):
        try:
            with QMutexLocker(self.lock):
                self._processar_evento_imediato(evento)

        except Exception as e:
            logger.error(f"Erro em EventoBuffer.adicionar_evento: {e}", exc_info=True)

    def adicionar_eventos_lote(self, eventos):
        if not eventos:
            return

        try:
            with QMutexLocker(self.lock):
                self.interface.tabela_dados.blockSignals(True)
                ordenacao_habilitada = self.interface.tabela_dados.isSortingEnabled()
                self.interface.tabela_dados.setSortingEnabled(False)
                try:
                    for evento in eventos:
                        self._processar_evento_imediato(evento)

                    eventos_movidos = [e for e in eventos if e.get("tipo_operacao") == self.interface.loc.get_text("op_moved")]
                    if eventos_movidos and hasattr(self.interface, 'movimentacao_worker'):
                        for evento in eventos_movidos:
                            self.interface.movimentacao_worker.adicionar_evento(evento)

                finally:
                    self.interface.tabela_dados.setSortingEnabled(ordenacao_habilitada)
                    self.interface.tabela_dados.blockSignals(False)
                    self.interface.tabela_dados.viewport().update()
                    QApplication.processEvents()

        except Exception as e:
            logger.error(f"Erro em EventoBuffer.adicionar_eventos_lote: {e}", exc_info=True)

    def _adicionar_evento_lote(self, evento):
        try:
            tipo_operacao_traduzido = self.interface.loc.get_text(evento["tipo_operacao"])
            if not self.interface.painel_filtros.verificar_filtro_operacao(tipo_operacao_traduzido):
                return

            self.interface.tabela_dados.setUpdatesEnabled(False)
            _adicionar_item_tabela(self.interface, evento, atualizar_interface=False)
            self.interface.tabela_dados.setUpdatesEnabled(True)

        except Exception as e:
            logger.error(f"Erro ao adicionar evento em lote: {e}", exc_info=True)

    def _processar_evento_imediato(self, evento):
        ordenacao_habilitada = self.interface.tabela_dados.isSortingEnabled()
        self.interface.tabela_dados.setSortingEnabled(False)
        try:
            _adicionar_item_tabela(self.interface, evento, atualizar_interface=False)
            if evento.get("tipo_operacao") == self.interface.loc.get_text("op_moved") and hasattr(self.interface, 'movimentacao_worker'):
                self.interface.movimentacao_worker.adicionar_evento(evento)

        except Exception as e:
            logger.error(f"Erro em EventoBuffer._processar_evento_imediato: {e}", exc_info=True)

        finally:
            self.interface.tabela_dados.setSortingEnabled(ordenacao_habilitada)
            self.interface.tabela_dados.viewport().update()
            QApplication.processEvents()

    def atualizar_interface(self):
        try:
            self.interface.atualizar_status()
            if hasattr(self.interface, 'gerenciador_tabela'):
                self.interface.gerenciador_tabela.atualizacao_pendente = True

            self.interface.tabela_dados.viewport().update()

        except Exception as e:
            logger.error(f"Erro em EventoBuffer.atualizar_interface: {e}", exc_info=True)
