import os
import queue
from PySide6.QtCore import QMetaObject, Qt
from source.services.GerenciamentoMetadados import identificar_tipo_arquivo
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def processar_fila_metadados(gc):
    update_em_fila = False
    max_batch = 64
    while True:
        try:
            item = gc.fila_metadados.get(timeout=0.5)
            lote = [item]
            while len(lote) < max_batch:
                try:
                    lote.append(gc.fila_metadados.get_nowait())

                except queue.Empty:
                    break

            houve_mudanca = False
            for item_lote in lote:
                caminho = item_lote.get("dir_atual") or item_lote.get("dir_anterior")
                if not caminho or not os.path.exists(caminho):
                    tipo = identificar_tipo_arquivo(caminho, gc.loc, item_lote.get("nome"))
                    if tipo:
                        with gc.lock_cache:
                            cache_item = gc.cache_metadados.setdefault(caminho or item_lote.get("nome", ""), {})
                            if cache_item.get("tipo") != tipo:
                                cache_item["tipo"] = tipo
                                houve_mudanca = True

                    continue

                metadados = gc.get_metadados(item_lote)
                if metadados:
                    with gc.lock_cache:
                        antigo = gc.cache_metadados.get(caminho)
                        if antigo != metadados:
                            gc.cache_metadados[caminho] = metadados
                            houve_mudanca = True

            if houve_mudanca and not update_em_fila:
                update_em_fila = True
                QMetaObject.invokeMethod(gc.interface, "atualizar_status", Qt.QueuedConnection)
                update_em_fila = False

        except queue.Empty:
            continue

        except Exception as e:
            logger.error(f"Erro no processamento de metadados: {e}", exc_info=True)
