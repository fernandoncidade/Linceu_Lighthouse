import win32file
from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def parar(self):
    try:
        with self._lock:
            self.parar_scan()
            if not self.ativo:
                try:
                    self.pausado = False
                    self._pause_event.set()
                    if hasattr(self, 'scanner') and self.scanner:
                        self.scanner.pausado = False
                        self.scanner._pause_event.set()

                except Exception:
                    pass

                return

            self.desligando = True
            self.ativo = False
            if self.thread:
                try:
                    win32file.CancelIo(self.handle_dir)
                    self.thread.join(timeout=0.05)
                    if hasattr(self, 'handle_dir'):
                        win32file.CloseHandle(self.handle_dir)
                        del self.handle_dir

                except Exception as e:
                    logger.error(f"Erro ao parar a thread: {e}", exc_info=True)

            self.limpar_estado()
            self.desligando = False
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
        logger.error(f"Erro ao parar Observador: {e}", exc_info=True)
