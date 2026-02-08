from source.services.GerenciamentoEventoMovido.gevmov_02_verificar_movimentacao import verificar_movimentacao
from source.services.GerenciamentoEventoMovido.gevmov_06_inicializar_sistema_evento import _inicializar_sistema_evento
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def adicionar_evento(interfaceMonitor, evento):
    try:
        if not evento or "tipo_operacao" not in evento or "nome" not in evento:
            logger.warning("Evento inválido recebido: %s", evento)
            return

        _inicializar_sistema_evento(interfaceMonitor)

        evento_processado = verificar_movimentacao(interfaceMonitor, evento)

        if evento_processado is not None:
            interfaceMonitor.processador_evento.evento_processado.emit(evento_processado)

    except Exception as e:
        logger.error(f"Erro em adicionar_evento: {e}", exc_info=True)
