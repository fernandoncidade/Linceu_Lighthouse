import win32file
import win32con
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def is_directory(self, path):
    try:
        attrs = win32file.GetFileAttributes(path)
        return attrs & win32con.FILE_ATTRIBUTE_DIRECTORY == win32con.FILE_ATTRIBUTE_DIRECTORY

    except Exception as e:
        logger.error(f"Erro ao verificar se é diretório: {e}", exc_info=True)
        return False
