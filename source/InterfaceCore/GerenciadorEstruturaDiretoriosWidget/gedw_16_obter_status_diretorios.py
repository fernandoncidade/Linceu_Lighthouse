import os
import time
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_status_diretorios(root_path):
    status_map = {}
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for name in filenames:
                path = os.path.join(dirpath, name)
                try:
                    mtime = os.path.getmtime(path)
                    if time.time() - mtime < 2 * 24 * 3600:
                        status_map[path] = 'modificado'

                    else:
                        status_map[path] = 'normal'

                except Exception:
                    status_map[path] = 'excluido'

            for name in dirnames:
                path = os.path.join(dirpath, name)
                if not os.path.exists(path):
                    status_map[path] = 'excluido'

                else:
                    status_map[path] = 'normal'

    except Exception as e:
        logger.error(f"Erro ao obter status dos diretórios: {e}")

    return status_map
