from utils.LogManager import LogManager
from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QApplication


class GerenciadorProgresso:
    @staticmethod
    @Slot()
    def criar_barra_progresso(interface):
        logger = LogManager.get_logger()
        logger.debug("Criando barra de progresso")
        interface.gerenciador_progresso_ui.criar_barra_progresso()

    @staticmethod
    @Slot(int, int, int)
    def atualizar_progresso_scan(interface, progresso, contador, total):
        logger = LogManager.get_logger()
        logger.debug(f"Atualizando progresso: {progresso}% ({contador}/{total})")
        try:
            if not (hasattr(interface, 'observador') and interface.observador and interface.observador.ativo):
                if hasattr(interface, 'barra_progresso'):
                    interface.barra_progresso.hide()
                    interface.barra_progresso.setValue(0)

                if hasattr(interface, 'rotulo_resultado') and hasattr(interface, 'loc'):
                    interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_stopped"))

                QApplication.processEvents()
                return

        except Exception:
            pass

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

        except Exception:
            pass

        interface.gerenciador_progresso_ui.atualizar_progresso_scan(progresso, contador, total)

        try:
            if progresso >= 100:
                def _post_scan_to_monitoring():
                    try:
                        if hasattr(interface, 'observador') and interface.observador and interface.observador.ativo:
                            interface.rotulo_resultado.setText(interface.loc.get_text("monitoring_started"))
                            QApplication.processEvents()

                    except Exception:
                        pass

                QTimer.singleShot(800, _post_scan_to_monitoring)
        except Exception:
            pass

    @staticmethod
    def esconder_barra_progresso(interface):
        logger = LogManager.get_logger()
        logger.debug("Escondendo barra de progresso")
        if hasattr(interface, 'barra_progresso'):
            QTimer.singleShot(1000, interface.barra_progresso.hide)
            interface.barra_progresso.setValue(0)
            logger.debug("Barra de progresso ocultada")
