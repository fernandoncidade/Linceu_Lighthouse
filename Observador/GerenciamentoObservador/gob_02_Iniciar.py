from PySide6.QtCore import QThread
from Observador.ob_03_DiretorioScanner import ScanWorker
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def iniciar(self):
    try:
        with self._lock:
            if not self.ativo:
                self.ativo = True
                self.desligando = False
                self.pausado = False
                try:
                    self._pause_event.set()

                except Exception:
                    pass

                from Observador.ob_03_DiretorioScanner import DiretorioScanner
                self.scanner = DiretorioScanner(self)
                try:
                    self.scanner.pausado = False
                    self.scanner._pause_event.set()

                except Exception:
                    pass

                self.thread_scan = QThread()
                self.scan_worker = ScanWorker(self.scanner, self.diretorio)
                self.scan_worker.moveToThread(self.thread_scan)
                self.thread_scan.started.connect(self.scan_worker.run)
                self.scan_worker.finished.connect(self.iniciar_monitoramento)
                self.scan_worker.error.connect(self.handle_scan_error)
                self.scan_worker.finished.connect(self.thread_scan.quit)
                self.scan_worker.finished.connect(self.scan_worker.deleteLater)
                self.thread_scan.finished.connect(self.thread_scan.deleteLater)
                self.thread_scan.start()

    except Exception as e:
        logger.error(f"Erro ao iniciar Observador: {e}", exc_info=True)
