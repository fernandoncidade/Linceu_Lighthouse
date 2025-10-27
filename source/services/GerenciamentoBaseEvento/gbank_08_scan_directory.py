from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def scan_directory(self, directory):
    try:
        from source.services.ob_03_DiretorioScanner import DiretorioScanner
        scanner = DiretorioScanner(self.observador)
        scanner.scan_directory(directory)

    except Exception as e:
        logger.error(f"Erro ao escanear diretório: {e}", exc_info=True)
