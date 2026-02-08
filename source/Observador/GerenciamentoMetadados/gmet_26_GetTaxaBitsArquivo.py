from .gmet_18_ExtrairMetadadosCompletos import get_metadados
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_taxa_bits_arquivo(gerenciador, item):
    try:
        metadados = get_metadados(gerenciador, item)
        return metadados.get("taxa_bits", "")

    except Exception as e:
        logger.error(f"Erro ao obter taxa de bits do arquivo {item.get('caminho', '')}: {e}", exc_info=True)
        return ""
