from source.Observador.GerenciamentoMetadados import identificar_tipo_arquivo as _identificar
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def identificar_tipo_arquivo(gc, caminho):
    try:
        return _identificar(caminho, gc.loc)

    except Exception as e:
        logger.error(f"Erro ao identificar tipo de arquivo: {e}", exc_info=True)
