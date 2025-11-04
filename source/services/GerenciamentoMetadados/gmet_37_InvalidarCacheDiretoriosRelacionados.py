import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def invalidar_cache_diretorios_relacionados(gc, caminho: str):
    try:
        chaves_tamanho = {
            "tamanho_dir", 
            "tamanho", 
            "tamanho_dir_bytes",
            "tamanho_dir_mtime", 
            "tamanho_dir_cached_at"
        }
        with gc.lock_cache:
            if os.path.isfile(caminho):
                dir_pai = os.path.dirname(caminho)
                if dir_pai in gc.cache_metadados:
                    for k in list(chaves_tamanho):
                        if k in gc.cache_metadados[dir_pai]:
                            gc.cache_metadados[dir_pai].pop(k, None)
                            print(f"Cache invalidado para diretório pai: {dir_pai}")

                    if not gc.cache_metadados[dir_pai]:
                        gc.cache_metadados.pop(dir_pai, None)

            dir_atual = os.path.dirname(caminho) if os.path.isfile(caminho) else caminho
            while True:
                if dir_atual in gc.cache_metadados:
                    for k in list(chaves_tamanho):
                        if k in gc.cache_metadados[dir_atual]:
                            gc.cache_metadados[dir_atual].pop(k, None)

                    if not gc.cache_metadados[dir_atual]:
                        gc.cache_metadados.pop(dir_atual, None)

                pai = os.path.dirname(dir_atual)
                if not pai or pai == dir_atual:
                    break

                dir_atual = pai

            if os.path.isdir(caminho):
                for root, dirs, files in os.walk(caminho):
                    if root in gc.cache_metadados:
                        for k in list(chaves_tamanho):
                            if k in gc.cache_metadados[root]:
                                gc.cache_metadados[root].pop(k, None)

                        if not gc.cache_metadados[root]:
                            gc.cache_metadados.pop(root, None)

    except Exception as e:
        logger.error(f"Erro ao invalidar cache de diretórios: {e}", exc_info=True)
