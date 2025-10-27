from PySide6.QtWidgets import QApplication
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def pausar_monitoramento_ou_escaneamento(self):
    try:
        self.pausado = not self.pausado
        if self.pausado:
            self._pause_event.clear()

        else:
            self._pause_event.set()

        if self.scan_worker and hasattr(self.scan_worker, "scanner"):
            try:
                self.scan_worker.scanner.pausado = self.pausado
                if self.pausado:
                    self.scan_worker.scanner._pause_event.clear()

                else:
                    self.scan_worker.scanner._pause_event.set()

            except Exception:
                pass

        if hasattr(self, "scanner") and self.scanner:
            try:
                self.scanner.pausado = self.pausado
                if self.pausado:
                    self.scanner._pause_event.clear()

                else:
                    self.scanner._pause_event.set()

            except Exception:
                pass

        try:
            if not hasattr(self, 'interface') or not self.interface:
                return

            scan_running = False
            try:
                scan_running = bool(getattr(self, 'thread_scan', None) and self.thread_scan.isRunning())

            except Exception:
                scan_running = False

            if scan_running and self.scan_worker and hasattr(self.scan_worker, 'scanner'):
                scanner = self.scan_worker.scanner
                progresso = int(getattr(scanner, 'ultimo_progresso', 0))
                contador = int(getattr(scanner, 'contador_processados', 0))
                total = int(getattr(scanner, 'total_arquivos', 0))

                if self.pausado:
                    texto = f"{self.loc.get_text('paused')} {progresso}% ({contador}/{total})"
                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            if not self.interface.barra_progresso.isVisible():
                                self.interface.barra_progresso.show()

                            self.interface.barra_progresso.setValue(progresso)

                        except Exception:
                            pass

                else:
                    texto = f"{self.loc.get_text('scanning')} {progresso}% ({contador}/{total})"
                    if hasattr(self.interface, 'barra_progresso'):
                        try:
                            if not self.interface.barra_progresso.isVisible():
                                self.interface.barra_progresso.show()

                            self.interface.barra_progresso.setValue(progresso)

                        except Exception:
                            pass

                try:
                    self.interface.rotulo_resultado.setText(texto)

                except Exception:
                    pass

                QApplication.processEvents()
                return

            if self.pausado:
                try:
                    self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_paused"))

                except Exception:
                    pass

                if hasattr(self.interface, 'barra_progresso'):
                    try:
                        self.interface.barra_progresso.hide()
                        self.interface.barra_progresso.setValue(0)

                    except Exception:
                        pass

            else:
                try:
                    self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_started"))

                except Exception:
                    pass

                if hasattr(self.interface, 'barra_progresso'):
                    try:
                        self.interface.barra_progresso.hide()
                        self.interface.barra_progresso.setValue(0)

                    except Exception:
                        pass

            QApplication.processEvents()
            return

        except Exception as e:
            logger.error(f"Erro ao alternar pausa: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao atualizar interface: {e}", exc_info=True)
