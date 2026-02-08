from .gmet_18_GetMetadados import get_metadados

def get_taxa_bits_arquivo(gerenciador, item):
    metadados = get_metadados(gerenciador, item)
    return metadados.get("taxa_bits", "")
