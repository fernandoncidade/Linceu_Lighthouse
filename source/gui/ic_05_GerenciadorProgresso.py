from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class GerenciadorProgresso:
    @staticmethod
    @Slot()
    def criar_barra_progresso(interface):
        try:
            interface.gerenciador_progresso_ui.criar_barra_progresso()

        except Exception as e:
            logger.error(f"Erro ao criar barra de progresso: {e}", exc_info=True)

    @staticmethod
    @Slot(int, int, int)
    def atualizar_progresso_scan(interface, progresso, contador, total):
        try:
            if not (hasattr(interface, 'observador') and interface.observador and interface.observador.ativo):
                if hasattr(interface, 'barra_progresso'):
                    interface.barra_progresso.hide()
                    interface.barra_progresso.setValue(0)

                if hasattr(interface, 'rotulo_resultado') and hasattr(interface, 'loc'):
                    interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_stopped"))

                QApplication.processEvents()
                return

        except Exception as e:
            logger.error(f"Erro ao atualizar progresso (monitoramento parado): {e}", exc_info=True)

        try:
            obs = getattr(interface, 'observador', None)
            scan_worker = getattr(obs, 'scan_worker', None) if obs else None
            scanner = getattr(scan_worker, 'scanner', None) if scan_worker else None

            if scanner and getattr(scanner, 'pausado', False):
                if hasattr(interface, 'barra_progresso'):
                    if not interface.barra_progresso.isVisible():
                        interface.barra_progresso.show()

                    interface.barra_progresso.setValue(progresso)

                if hasattr(interface, 'rotulo_resultado'):
                    texto = f"{interface.loc.get_text('paused')} {progresso}% ({contador}/{total})"
                    interface.rotulo_resultado.setText(texto)

                QApplication.processEvents()
                return

            if obs and getattr(obs, 'pausado', False) and not (scanner and getattr(scanner, 'pausado', False)):
                if hasattr(interface, 'barra_progresso'):
                    interface.barra_progresso.hide()
                    interface.barra_progresso.setValue(0)

                if hasattr(interface, 'rotulo_resultado'):
                    interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_paused"))

                QApplication.processEvents()
                return

        except Exception as e:
            logger.error(f"Erro ao atualizar progresso (pausado): {e}", exc_info=True)

        try:
            interface.gerenciador_progresso_ui.atualizar_progresso_scan(progresso, contador, total)

        except Exception as e:
            logger.error(f"Erro ao atualizar barra de progresso: {e}", exc_info=True)

        try:
            if progresso >= 100:
                def _post_scan_to_monitoring():
                    try:
                        if hasattr(interface, 'observador') and interface.observador and interface.observador.ativo:
                            interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_started"))
                            QApplication.processEvents()

                    except Exception as e:
                        logger.error(f"Erro ao finalizar pós-scan: {e}", exc_info=True)

                QTimer.singleShot(800, _post_scan_to_monitoring)

        except Exception as e:
            logger.error(f"Erro ao agendar pós-scan: {e}", exc_info=True)

    @staticmethod
    def esconder_barra_progresso(interface):
        try:
            if hasattr(interface, 'barra_progresso'):
                QTimer.singleShot(1000, interface.barra_progresso.hide)
                interface.barra_progresso.setValue(0)

        except Exception as e:
            logger.error(f"Erro ao esconder barra de progresso: {e}", exc_info=True)
