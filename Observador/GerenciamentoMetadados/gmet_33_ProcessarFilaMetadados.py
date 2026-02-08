import os
import time
import queue
from PySide6.QtCore import QMetaObject, Qt
from Observador.GerenciamentoMetadados import identificar_tipo_arquivo
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def processar_fila_metadados(gc):
    while True:
        try:
            item = gc.fila_metadados.get(timeout=1)
            caminho = item.get("dir_atual") or item.get("dir_anterior")
            if not caminho or not os.path.exists(caminho):
                tipo = identificar_tipo_arquivo(caminho, gc.loc, item.get("nome"))
                metadados = {"tipo": tipo}
                return metadados

            time.sleep(0.1)
            if os.path.exists(caminho):
                metadados = gc.get_metadados(item)
                if metadados:
                    with gc.lock_cache:
                        gc.cache_metadados[caminho] = metadados

                    QMetaObject.invokeMethod(gc.interface, "atualizar_colunas_tabela", Qt.QueuedConnection)

        except queue.Empty:
            continue

        except Exception as e:
            logger.error(f"Erro no processamento de metadados: {e}", exc_info=True)
