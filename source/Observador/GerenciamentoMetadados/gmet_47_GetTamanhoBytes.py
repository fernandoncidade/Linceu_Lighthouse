import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _get_tamanho_bytes(gc, item):
    try:
        caminho = item.get("dir_atual") or item.get("dir_anterior")
        if caminho and os.path.exists(caminho):
            if os.path.isfile(caminho):
                return os.path.getsize(caminho)

            elif os.path.isdir(caminho):
                total = 0
                for root, dirs, files in os.walk(caminho):
                    for f in files:
                        try:
                            total += os.path.getsize(os.path.join(root, f))

                        except Exception as e:
                            logger.error(f"Erro ao obter tamanho de arquivo: {e}", exc_info=True)

                return total

        return 0

    except Exception as e:
        logger.error(f"Erro ao obter tamanho: {e}", exc_info=True)
