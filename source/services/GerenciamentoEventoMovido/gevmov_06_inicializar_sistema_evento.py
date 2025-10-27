from PySide6.QtCore import QTimer
from source.services.GerenciamentoEventoMovido.gevmov_07_processar_exclusoes_pendentes import _processar_exclusoes_pendentes
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _inicializar_sistema_evento(interfaceMonitor):
    try:
        from source.services.ob_08_EventoMovido import EventoMovido, EventoBuffer
        if not hasattr(interfaceMonitor, 'processador_evento'):
            interfaceMonitor.processador_evento = EventoMovido()
            if not hasattr(interfaceMonitor, 'evento_buffer'):
                interfaceMonitor.evento_buffer = EventoBuffer(interfaceMonitor)

            if not hasattr(interfaceMonitor, 'movimentacao_worker'):
                from source.services.GerenciamentoEventoMovido.gevmov_01_MovimentacaoWorker import MovimentacaoWorker
                interfaceMonitor.movimentacao_worker = MovimentacaoWorker(interfaceMonitor)
                interfaceMonitor.movimentacao_worker.processamento_concluido.connect(lambda: interfaceMonitor.gerenciador_tabela.atualizar_linha_mais_recente(interfaceMonitor.tabela_dados))

            interfaceMonitor.processador_evento.evento_processado.connect(lambda evento: interfaceMonitor.evento_buffer.adicionar_evento(evento))
            interfaceMonitor.processador_evento.eventos_em_lote_processados.connect(lambda eventos: interfaceMonitor.evento_buffer.adicionar_eventos_lote(eventos))

        if not hasattr(interfaceMonitor, 'contador_eventos'):
            interfaceMonitor.contador_eventos = 0

        if not hasattr(interfaceMonitor, 'refresh_timer'):
            interfaceMonitor.refresh_timer = QTimer()
            interfaceMonitor.refresh_timer.timeout.connect(lambda: interfaceMonitor.atualizar_status())
            interfaceMonitor.refresh_timer.start(1000)

        if not hasattr(interfaceMonitor, 'exclusao_timer'):
            interfaceMonitor.exclusao_timer = QTimer()
            interfaceMonitor.exclusao_timer.timeout.connect(lambda: _processar_exclusoes_pendentes(interfaceMonitor))
            interfaceMonitor.exclusao_timer.start(1000)

    except Exception as e:
        logger.error(f"Erro ao inicializar sistema de eventos: {e}", exc_info=True)
