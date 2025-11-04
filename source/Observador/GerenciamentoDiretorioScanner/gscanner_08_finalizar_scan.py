from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _finalizar_scan(self):
    try:
        if hasattr(self.observador, 'interface') and hasattr(self.observador.interface, 'barra_progresso'):
            self.observador.interface.barra_progresso.hide()
            self.observador.interface.barra_progresso.setValue(0)

            if hasattr(self.observador.interface, 'gerenciador_tabela'):
                self.observador.interface.gerenciador_tabela.atualizar_dados_tabela(self.observador.interface.tabela_dados)

                self.observador.interface.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao finalizar scan: {e}", exc_info=True)
