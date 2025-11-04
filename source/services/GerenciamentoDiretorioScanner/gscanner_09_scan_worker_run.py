from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def run(self):
    try:
        self.scanner.scan_directory(self.directory)
        self.finished.emit()

    except Exception as e:
        logger.error(f"Erro no scan do diretório {self.directory}: {e}", exc_info=True)
        self.error.emit(str(e))
