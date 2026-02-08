import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from source.InterfaceCore.ic_01_InterfaceMonitor import InterfaceMonitor
from source.InterfaceCore.ic_08_Internacionalizador import Internacionalizador
from source.GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
from utils.LogManager import LogManager
# from utils.TrialManager import TrialManager

logger = LogManager.get_logger()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # TrialManager.enforce_trial()  # Descomente esta linha para forçar o uso da versão de avaliação
        # TrialManager.delete_first_run_timestamp()  # Use esta linha para testes, removendo o timestamp de primeiro uso
        Internacionalizador.inicializar_sistema_traducao(app)
        loc_temp = LocalizadorQt()
        idioma = loc_temp.idioma_atual
        window = InterfaceMonitor()
        window.show()
        exit_code = app.exec()
        logger.debug(f"Aplicação encerrada com código de saída: {exit_code}")
        sys.exit(exit_code)

    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar aplicação: {e}", exc_info=True)
        sys.exit(1)
