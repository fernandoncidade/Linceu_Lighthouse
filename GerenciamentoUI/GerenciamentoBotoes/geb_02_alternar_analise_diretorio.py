from PySide6.QtWidgets import QMessageBox
from Observador.ob_01_Observador import Observador
from utils.LogManager import LogManager
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

def alternar_analise_diretorio(self):
    try:
        if not self.interface.diretorio_atual:
            QMessageBox.warning(self.interface, self.loc.get_text("warning"), self.loc.get_text("select_first"))
            return

        if not self.interface.observador:
            self.interface.observador = Observador(self.interface.diretorio_atual, self.interface.adicionar_evento)
            self.interface.observador.interface = self.interface

        if hasattr(self.interface.observador, 'thread_scan'):
            if _is_thread_valid_and_running(self.interface.observador.thread_scan):
                try:
                    self.interface.observador.parar_scan()
                    self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_stopped"))
                    return

                except Exception as e:
                    logger.error(f"Erro ao parar escaneamento: {e}", exc_info=True)

            if self.interface.observador.thread_scan:
                try:
                    _ = self.interface.observador.thread_scan.objectName()

                except RuntimeError:
                    self.interface.observador.thread_scan = None
                    if hasattr(self.interface.observador, 'scan_worker'):
                        self.interface.observador.scan_worker = None

        if not self.interface.observador.ativo:
            self.interface.observador.iniciar()
            self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_started"))

        else:
            self.interface.observador.parar()
            self.interface.rotulo_resultado.setText(self.loc.get_text("monitoring_stopped"))

    except Exception as e:
        logger.error(f"Erro ao alternar análise: {e}", exc_info=True)
