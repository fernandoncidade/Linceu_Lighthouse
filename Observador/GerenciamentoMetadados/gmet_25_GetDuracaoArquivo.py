from .gmet_18_GetMetadados import get_metadados

def get_duracao_arquivo(gerenciador, item):
    metadados = get_metadados(gerenciador, item)
    return metadados.get("duracao", "")
