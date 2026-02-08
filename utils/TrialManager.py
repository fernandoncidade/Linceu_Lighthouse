import os
import json
import time
import winreg
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from utils.IconUtils import get_icon_path
from source.GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class TrialManager:
    CONFIG_FILE = "trial_info.json"
    DEFAULT_TRIAL = "days"  # Pode ser "minutes" ou "days"
    DEFAULT_TRIAL_VALUE = 7    # Valor inteiro para minutos ou dias
    PAID_VERSION_URL = "ms-windows-store://pdp/?productid=9NN8Z5Z700TM"
    LIBERAR_USO_DEFINITIVO = False  # Altere para True para liberar uso definitivo
    REG_PATH = r"SOFTWARE\LinceuLighthouse"
    REG_KEY = "FirstRunTimestamp"

    @classmethod
    def get_config_path(cls):
        try:
            config_dir = obter_caminho_persistente()
            return os.path.join(config_dir, cls.CONFIG_FILE)

        except Exception as e:
            logger.error(f"Erro ao obter caminho de configuração: {e}")
            return None

    @classmethod
    def get_first_run_timestamp(cls):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, cls.REG_KEY)
                return int(value)

        except Exception as e:
            logger.error(f"Erro ao obter timestamp do registro: {e}")
            return None

    @classmethod
    def set_first_run_timestamp(cls, timestamp):
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH) as key:
                winreg.SetValueEx(key, cls.REG_KEY, 0, winreg.REG_SZ, str(timestamp))

        except Exception as e:
            logger.error(f"Erro ao definir timestamp no registro: {e}")

    @classmethod
    def delete_first_run_timestamp(cls):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, cls.REG_KEY)

        except FileNotFoundError:
            logger.error("Timestamp não encontrado no registro.")

        except Exception as e:
            logger.error(f"Erro ao remover timestamp: {e}")

    @classmethod
    def get_trial_info(cls):
        try:
            path = cls.get_config_path()
            first_run = cls.get_first_run_timestamp()

            if path and os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        info = json.load(f)
                        if first_run is not None:
                            info["first_run"] = first_run

                        else:
                            cls.set_first_run_timestamp(info.get("first_run", int(time.time())))

                        return info

                except Exception as e:
                    logger.error(f"Erro ao ler arquivo de configuração: {e}")

            timestamp = first_run if first_run is not None else int(time.time())
            info = {"first_run": timestamp}
            if path:
                try:
                    with open(path, "w") as f:
                        json.dump(info, f)

                except Exception as e:
                    logger.error(f"Erro ao criar arquivo de configuração: {e}")

            if first_run is None:
                cls.set_first_run_timestamp(timestamp)

            return info

        except Exception as e:
            logger.error(f"Erro geral em get_trial_info: {e}")
            return {"first_run": int(time.time())}

    @classmethod
    def is_trial_expired(cls):
        try:
            info = cls.get_trial_info()
            first_run = info.get("first_run", int(time.time()))
            now = int(time.time())
            if cls.DEFAULT_TRIAL == "minutes":
                trial_seconds = cls.DEFAULT_TRIAL_VALUE * 60

            elif cls.DEFAULT_TRIAL == "days":
                trial_seconds = cls.DEFAULT_TRIAL_VALUE * 24 * 3600

            else:
                trial_seconds = 0

            return (now - first_run) > trial_seconds

        except Exception as e:
            logger.error(f"Erro ao verificar expiração do trial: {e}")
            return False

    @classmethod
    def enforce_trial(cls, parent=None):
        try:
            if cls.LIBERAR_USO_DEFINITIVO:
                return

            if cls.is_trial_expired():
                loc = LocalizadorQt()
                msg = QMessageBox(parent)
                icon_file = get_icon_path("file_manager4.ico")
                msg.setWindowIcon(QIcon(icon_file))
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle(loc.get_text("trial_expired_title"))
                msg.setTextFormat(Qt.TextFormat.RichText)
                msg.setText(
                    f"{loc.get_text('trial_expired_message')}<br>"
                    f"{loc.get_text('trial_buy_message')}<br><br>"
                    f"{loc.get_text('trial_uninstall_message')}<br><br>"
                    f'<a href="{cls.PAID_VERSION_URL}">{loc.get_text("trial_paid_link")}</a>'
                )
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                os._exit(0)

        except Exception as e:
            logger.error(f"Erro ao aplicar restrição do trial: {e}")

# import os
# import json
# import time
# import winreg
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon
# from PySide6.QtWidgets import QMessageBox
# from utils.CaminhoPersistenteUtils import obter_caminho_persistente
# from utils.IconUtils import get_icon_path
# from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt


# class TrialManager:
#     CONFIG_FILE = "trial_info.json"
#     DEFAULT_TRIAL = "days"  # Pode ser "minutes" ou "days"
#     DEFAULT_TRIAL_VALUE = 7    # Valor inteiro para minutos ou dias
#     PAID_VERSION_URL = "ms-windows-store://pdp/?productid=9NN8Z5Z700TM"
#     LIBERAR_USO_DEFINITIVO = False  # Altere para True para liberar uso definitivo
#     REG_PATH = r"SOFTWARE\LinceuLighthouse"
#     REG_KEY = "FirstRunTimestamp"

#     @classmethod
#     def get_config_path(cls):
#         config_dir = obter_caminho_persistente()
#         return os.path.join(config_dir, cls.CONFIG_FILE)

#     @classmethod
#     def get_first_run_timestamp(cls):
#         try:
#             with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, winreg.KEY_READ) as key:
#                 value, _ = winreg.QueryValueEx(key, cls.REG_KEY)
#                 return int(value)

#         except Exception:
#             return None

#     @classmethod
#     def set_first_run_timestamp(cls, timestamp):
#         try:
#             with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH) as key:
#                 winreg.SetValueEx(key, cls.REG_KEY, 0, winreg.REG_SZ, str(timestamp))

#         except Exception:
#             pass

#     @classmethod
#     def delete_first_run_timestamp(cls):
#         try:
#             with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
#                 winreg.DeleteValue(key, cls.REG_KEY)
#                 print("Timestamp removido do registro do Windows.")

#         except FileNotFoundError:
#             print("Timestamp não encontrado no registro.")

#         except Exception as e:
#             print(f"Erro ao remover timestamp: {e}")

#     @classmethod
#     def get_trial_info(cls):
#         path = cls.get_config_path()
#         first_run = cls.get_first_run_timestamp()
#         if os.path.exists(path):
#             try:
#                 with open(path, "r") as f:
#                     info = json.load(f)
#                     if first_run is not None:
#                         info["first_run"] = first_run

#                     else:
#                         cls.set_first_run_timestamp(info.get("first_run", int(time.time())))

#                     return info

#             except Exception:
#                 pass

#         timestamp = first_run if first_run is not None else int(time.time())
#         info = {"first_run": timestamp}
#         with open(path, "w") as f:
#             json.dump(info, f)

#         if first_run is None:
#             cls.set_first_run_timestamp(timestamp)

#         return info

#     @classmethod
#     def is_trial_expired(cls):
#         info = cls.get_trial_info()
#         first_run = info.get("first_run", int(time.time()))
#         now = int(time.time())

#         if cls.DEFAULT_TRIAL == "minutes":
#             trial_seconds = cls.DEFAULT_TRIAL_VALUE * 60

#         elif cls.DEFAULT_TRIAL == "days":
#             trial_seconds = cls.DEFAULT_TRIAL_VALUE * 24 * 3600

#         else:
#             trial_seconds = 0

#         return (now - first_run) > trial_seconds

#     @classmethod
#     def enforce_trial(cls, parent=None):
#         if cls.LIBERAR_USO_DEFINITIVO:
#             return

#         if cls.is_trial_expired():
#             loc = LocalizadorQt()
#             msg = QMessageBox(parent)
#             icon_file = get_icon_path("file_manager4.ico")
#             msg.setWindowIcon(QIcon(icon_file))
#             msg.setIcon(QMessageBox.Critical)
#             msg.setWindowTitle(loc.get_text("trial_expired_title"))
#             msg.setTextFormat(Qt.TextFormat.RichText)
#             msg.setText(
#                 f"{loc.get_text('trial_expired_message')}<br>"
#                 f"{loc.get_text('trial_buy_message')}<br><br>"
#                 f"{loc.get_text('trial_uninstall_message')}<br><br>"
#                 f'<a href="{cls.PAID_VERSION_URL}">{loc.get_text("trial_paid_link")}</a>'
#             )
#             msg.setStandardButtons(QMessageBox.Ok)
#             msg.exec()
#             os._exit(0)



# import os
# import json
# import time
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon
# from PySide6.QtWidgets import QMessageBox
# from utils.CaminhoPersistenteUtils import obter_caminho_persistente
# from utils.IconUtils import get_icon_path
# from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt


# class TrialManager:
#     CONFIG_FILE = "trial_info.json"
#     DEFAULT_TRIAL = "minutes"  # Pode ser "minutes" ou "days"
#     DEFAULT_TRIAL_VALUE = 5    # Valor inteiro para minutos ou dias
#     PAID_VERSION_URL = "ms-windows-store://pdp/?productid=9NN8Z5Z700TM"
#     LIBERAR_USO_DEFINITIVO = False  # Altere para True para liberar uso definitivo

#     @classmethod
#     def get_config_path(cls):
#         config_dir = obter_caminho_persistente()
#         return os.path.join(config_dir, cls.CONFIG_FILE)

#     @classmethod
#     def get_trial_info(cls):
#         path = cls.get_config_path()
#         if os.path.exists(path):
#             try:
#                 with open(path, "r") as f:
#                     return json.load(f)

#             except Exception:
#                 pass

#         # Se não existe, cria com timestamp atual
#         info = {"first_run": int(time.time())}
#         with open(path, "w") as f:
#             json.dump(info, f)

#         return info

#     @classmethod
#     def is_trial_expired(cls):
#         info = cls.get_trial_info()
#         first_run = info.get("first_run", int(time.time()))
#         now = int(time.time())

#         if cls.DEFAULT_TRIAL == "minutes":
#             trial_seconds = cls.DEFAULT_TRIAL_VALUE * 60

#         elif cls.DEFAULT_TRIAL == "days":
#             trial_seconds = cls.DEFAULT_TRIAL_VALUE * 24 * 3600

#         else:
#             trial_seconds = 0  # Sem período de teste

#         return (now - first_run) > trial_seconds

#     @classmethod
#     def enforce_trial(cls, parent=None):
#         if cls.LIBERAR_USO_DEFINITIVO:
#             return

#         if cls.is_trial_expired():
#             loc = LocalizadorQt()
#             msg = QMessageBox(parent)
#             icon_file = get_icon_path("file_manager4.ico")
#             msg.setWindowIcon(QIcon(icon_file))
#             msg.setIcon(QMessageBox.Critical)
#             msg.setWindowTitle(loc.get_text("trial_expired_title"))
#             msg.setTextFormat(Qt.TextFormat.RichText)
#             msg.setText(
#                 f"{loc.get_text('trial_expired_message')}<br>"
#                 f"{loc.get_text('trial_buy_message')}<br><br>"
#                 f"{loc.get_text('trial_uninstall_message')}<br><br>"
#                 f'<a href="{cls.PAID_VERSION_URL}">{loc.get_text("trial_paid_link")}</a>'
#             )
#             msg.setStandardButtons(QMessageBox.Ok)
#             msg.exec()
#             os._exit(0)
