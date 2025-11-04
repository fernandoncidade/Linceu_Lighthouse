from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def handle_scan_error(self, error_msg):
    logger.error(f"Erro durante escaneamento: {error_msg}")
    self.ativo = False
    if hasattr(self, 'interface'):
        self.interface.rotulo_resultado.setText(f"Erro: {error_msg}")
