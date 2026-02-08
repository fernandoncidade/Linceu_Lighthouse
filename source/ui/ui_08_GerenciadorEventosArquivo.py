from source.utils.LogManager import LogManager
from source.services.ob_08_EventoMovido import verificar_movimentacao, adicionar_evento
logger = LogManager.get_logger()


class GerenciadorEventosArquivo:
    def __init__(self, interface_principal):
        try:
            self.interface = interface_principal

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorEventosArquivo: {e}", exc_info=True)

    def verificar_movimentacao(self, evento):
        try:
            return verificar_movimentacao(self.interface, evento)

        except Exception as e:
            logger.error(f"Erro ao verificar movimentação: {e}", exc_info=True)
            return None

    def adicionar_evento(self, evento):
        try:
            adicionar_evento(self.interface, evento)

        except Exception as e:
            logger.error(f"Erro ao adicionar evento: {e}", exc_info=True)

    def limpar_eventos(self):
        try:
            if hasattr(self.interface, 'evento_base'):
                self.interface.evento_base.limpar_registros()

        except Exception as e:
            logger.error(f"Erro ao limpar eventos: {e}", exc_info=True)
