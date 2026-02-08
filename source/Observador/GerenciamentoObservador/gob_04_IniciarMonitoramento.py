import threading
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def iniciar_monitoramento(self):
    try:
        self.thread = threading.Thread(target=self.monitorar)
        self.thread.daemon = True
        self.thread.start()
        self.thread_buffer = threading.Thread(target=self.processar_buffer_eventos)
        self.thread_buffer.daemon = True
        self.thread_buffer.start()
        if hasattr(self, 'interface') and hasattr(self.interface, 'gerenciador_tabela'):
            self.interface.gerenciador_tabela.atualizar_dados_tabela(self.interface.tabela_dados)
            self.interface.atualizar_status()

        if hasattr(self, 'interface'):
            self.interface.rotulo_resultado.setText(self.interface.loc.get_text("monitoring_started"))
            self.interface.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao iniciar monitoramento: {e}", exc_info=True)
