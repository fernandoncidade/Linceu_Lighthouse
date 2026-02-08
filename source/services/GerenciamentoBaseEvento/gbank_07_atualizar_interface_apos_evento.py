from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_interface_apos_evento(self, evento):
    try:
        interface = None
        if self.callback and hasattr(self.callback, '__self__'):
            interface = self.callback.__self__

        elif hasattr(self.observador, 'interface'):
            interface = self.observador.interface

        if interface:
            try:
                QMetaObject.invokeMethod(interface, "inserir_evento_streaming", Qt.ConnectionType.QueuedConnection, Q_ARG(dict, evento))

            except Exception:
                if hasattr(interface, 'gerenciador_tabela'):
                    interface.gerenciador_tabela.atualizar_linha_mais_recente(interface.tabela_dados, evento=evento)

                interface.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao atualizar interface após evento: {e}", exc_info=True)
