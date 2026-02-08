from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _is_thread_valid_and_running(thread):
    if not thread:
        return False

    try:
        _ = thread.objectName()
        return thread.isRunning()

    except RuntimeError:
        return False

    except Exception:
        return False

def pausar_monitoramento_ou_escaneamento(self):
    try:
        if self.interface.observador:
            obs = self.interface.observador
            scan_running = False

            if hasattr(obs, 'thread_scan'):
                scan_running = _is_thread_valid_and_running(obs.thread_scan)

                if obs.thread_scan and not scan_running:
                    try:
                        _ = obs.thread_scan.objectName()

                    except RuntimeError:
                        obs.thread_scan = None
                        if hasattr(obs, 'scan_worker'):
                            obs.scan_worker = None

            if obs.ativo or scan_running:
                try:
                    obs.pausar_monitoramento_ou_escaneamento()

                except Exception as e:
                    logger.error(f"Erro ao pausar monitoramento ou escaneamento: {e}", exc_info=True)

                return

            try:
                titulo = self.loc.get_text("warning")

            except Exception as e:
                logger.error(f"Erro ao obter texto de título: {e}", exc_info=True)
                titulo = "Aviso"

            try:
                mensagem = self.loc.get_text("no_scan_or_monitor_to_pause")

            except Exception as e:
                logger.error(f"Erro ao obter texto de mensagem: {e}", exc_info=True)
                mensagem = "Não há escaneamento nem monitoramento em andamento para pausar."

            QMessageBox.information(self.interface, titulo, mensagem)
            return

        if hasattr(self.interface, "scanner") and self.interface.scanner:
            try:
                self.interface.scanner.pausar()
                return

            except Exception as e:
                logger.error(f"Erro ao pausar scanner: {e}", exc_info=True)

        try:
            titulo = self.loc.get_text("warning")

        except Exception as e:
            logger.error(f"Erro ao obter texto de título: {e}", exc_info=True)
            titulo = "Aviso"

        try:
            mensagem = self.loc.get_text("no_scan_or_monitor_to_pause")

        except Exception as e:
            logger.error(f"Erro ao obter texto de mensagem: {e}", exc_info=True)
            mensagem = "Não há escaneamento nem monitoramento em andamento para pausar."

        QMessageBox.information(self.interface, titulo, mensagem)

    except Exception as e:
        logger.error(f"Erro ao pausar: {e}", exc_info=True)
