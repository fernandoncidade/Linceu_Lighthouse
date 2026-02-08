import os
import logging
from datetime import datetime


class LogManager:
    _instance = None
    _logger = None
    _log_file = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._configure_logging()

        return cls._logger

    @classmethod
    def get_log_file(cls):
        if cls._log_file is None:
            cls._configure_logging()

        return cls._log_file

    @classmethod
    def ensure_unicode(cls, message):
        if isinstance(message, bytes):
            return message.decode('utf-8', errors='replace')

        return str(message)

    @classmethod
    def _configure_logging(cls):
        try:
            log_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'LinceuLighthouse', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            cls._log_file = os.path.join(log_dir, f'file_monitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(cls._log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            cls._logger = logging.getLogger('FileManager')
            cls._logger.info(f"Sistema de logging configurado com sucesso em {log_dir}")

        except Exception as e:
            user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'File-Folder-Manager', 'logs')
            os.makedirs(user_data_dir, exist_ok=True)
            cls._log_file = os.path.join(user_data_dir, f'file_monitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(cls._log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            cls._logger = logging.getLogger('FileManager')
            cls._logger.info(f"Sistema de logging configurado com diretório alternativo: {user_data_dir}")
            cls._logger.error(f"Erro ao configurar logging no diretório padrão: {e}")

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(cls.ensure_unicode(message))

    @classmethod
    def info(cls, message):
        cls.get_logger().info(cls.ensure_unicode(message))

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(cls.ensure_unicode(message))

    @classmethod
    def error(cls, message, exc_info=False):
        cls.get_logger().error(cls.ensure_unicode(message), exc_info=exc_info)

    @classmethod
    def critical(cls, message, exc_info=True):
        cls.get_logger().critical(cls.ensure_unicode(message), exc_info=exc_info)

# fernandoncidade: 
# Com base no arquivo em anexo, é possível fazer um código que ao insirir sua chamada num módulo do projeto, ele reporte o erro e o local da linha do código que contém este erro?

# GitHub Copilot:
# Sim, é possível! O `LogManager` já suporta registrar exceções com informações detalhadas usando o parâmetro `exc_info=True` nos métodos `error` e `critical`.
# Para reportar o erro e o local da linha, basta chamar `LogManager.error` dentro de um bloco `except`, passando `exc_info=True`.
# O logger irá registrar a stack trace, incluindo o arquivo e a linha do erro.


# Exemplo de uso em outro módulo:

# ````python
# # ...existing code...

# from utils.LogManager import LogManager

# try:
#     # Código que pode gerar exceção
#     resultado = 10 / 0
# except Exception as e:
#     LogManager.error(f"Ocorreu um erro: {e}", exc_info=True)

# # ...existing code...
# ````

# Isso irá registrar no log o erro, a mensagem e o local exato (arquivo e linha) onde ocorreu a exceção.
