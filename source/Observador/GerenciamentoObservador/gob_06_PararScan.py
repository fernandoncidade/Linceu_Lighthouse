from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def parar_scan(self):
    try:
        if self.thread_scan:
            try:
                if self.thread_scan.isRunning():
                    self.desligando = True
                    self.ativo = False
                    try:
                        self.pausado = False
                        self._pause_event.set()
                        if hasattr(self, 'scan_worker') and hasattr(self.scan_worker, 'scanner'):
                            scanner = self.scan_worker.scanner
                            scanner.pausado = False
                            scanner._pause_event.set()

                    except Exception:
                        pass

                    self.thread_scan.requestInterruption()
                    self.thread_scan.quit()
                    self.thread_scan.wait(5000)

            except Exception as e:
                logger.error(f"Erro ao parar thread de escaneamento: {e}", exc_info=True)

            finally:
                self.thread_scan = None
                self.scan_worker = None

            try:
                if hasattr(self, 'interface') and self.interface:
                    try:
                        self.interface.rotulo_resultado.setText(self.interface.loc.get_text("monitoring_stopped"))

                    except Exception:
                        pass

                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            self.interface.barra_progresso.hide()
                            self.interface.barra_progresso.setValue(0)

                        except Exception:
                            pass

                    QApplication.processEvents()

            except Exception:
                pass

    except Exception as e:
        logger.error(f"Erro ao parar escaneamento: {e}", exc_info=True)
