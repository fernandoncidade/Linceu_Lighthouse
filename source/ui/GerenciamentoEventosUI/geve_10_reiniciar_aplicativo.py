import sys
import subprocess
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _reiniciar_aplicativo(self):
    try:
        if hasattr(self.interface, 'rotulo_resultado'):
            self.interface.rotulo_resultado.setText(
                self.loc.get_text("language_change_confirm").split('?')[0] + "..."
            )
        from PySide6.QtCore import QCoreApplication, QTimer
        QCoreApplication.processEvents()
        self._limpar_dados_monitorados()
        def executar_reinicio():
            try:
                python = sys.executable
                script_path = sys.argv[0]
                args = sys.argv[1:]
                subprocess.Popen([python, script_path] + args)
                sys.exit(0)

            except Exception as e:
                logger.error(f"Erro no timer de reinício: {e}", exc_info=True)

        QTimer.singleShot(500, executar_reinicio)

    except Exception as e:
        logger.error(f"Erro ao reiniciar aplicativo: {e}", exc_info=True)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self.interface, self.loc.get_text("error"), self.loc.get_text("restart_error").format(str(e)))
