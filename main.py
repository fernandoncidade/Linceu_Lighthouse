import sys
from source.src_01_InicializadorMain import iniciar_aplicacao

if __name__ == '__main__':
    sys.exit(iniciar_aplicacao())

# import os
# import sys

# if getattr(sys, 'frozen', False):
#     os.chdir(os.path.dirname(sys.executable))

# else:
#     os.chdir(os.path.dirname(os.path.abspath(__file__)))

# from PySide6.QtWidgets import QApplication
# from PySide6.QtGui import QIcon
# from source.InterfaceCore.ic_01_InterfaceMonitor import InterfaceMonitor
# from source.InterfaceCore.ic_08_Internacionalizador import Internacionalizador
# from source.utils.LogManager import LogManager
# from source.utils.IconUtils import get_icon_path
# # from source.utils.TrialManager import TrialManager

# logger = LogManager.get_logger()

# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)

#         if sys.platform.startswith("win"):
#             try:
#                 import ctypes
#                 ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("LinceuLighthouse.App")

#             except Exception as e:
#                 logger.warning(f"Falha ao definir AppUserModelID: {e}", exc_info=True)

#         try:
#             app_icon_path = get_icon_path("file_manager4.ico")
#             if app_icon_path and os.path.exists(app_icon_path):
#                 app.setWindowIcon(QIcon(app_icon_path))

#             else:
#                 logger.warning(f"Ícone do app não encontrado: {app_icon_path}")

#         except Exception as e:
#             logger.warning(f"Falha ao definir ícone do aplicativo: {e}", exc_info=True)

#         # TrialManager.enforce_trial()  # Descomente esta linha para forçar o uso da versão de avaliação
#         # TrialManager.delete_first_run_timestamp()  # Use esta linha para testes, removendo o timestamp de primeiro uso
#         Internacionalizador.inicializar_sistema_traducao(app)
#         window = InterfaceMonitor()

#         try:
#             if app_icon_path and os.path.exists(app_icon_path):
#                 window.setWindowIcon(QIcon(app_icon_path))

#         except Exception:
#             pass

#         window.show()
#         exit_code = app.exec()
#         logger.debug(f"Aplicação encerrada com código de saída: {exit_code}")
#         sys.exit(exit_code)

#     except Exception as e:
#         logger.critical(f"Erro fatal ao iniciar aplicação: {e}", exc_info=True)
#         sys.exit(1)
