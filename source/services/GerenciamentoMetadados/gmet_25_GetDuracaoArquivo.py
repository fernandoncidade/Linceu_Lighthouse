from .gmet_18_ExtrairMetadadosCompletos import get_metadados
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_duracao_arquivo(gerenciador, item):
    try:
        metadados = get_metadados(gerenciador, item)
        return metadados.get("duracao", "")

    except Exception as e:
        logger.error(f"Erro ao obter duração do arquivo {item.get('caminho', '')}: {e}", exc_info=True)
        return ""
