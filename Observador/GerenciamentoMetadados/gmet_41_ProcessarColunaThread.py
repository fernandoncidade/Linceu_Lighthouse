import queue
from PySide6.QtCore import QMetaObject, Qt

def processar_coluna_thread(gc, coluna_key):
    while True:
        try:
            item = gc.filas_colunas[coluna_key].get(timeout=1)
            getter = gc.COLUNAS_DISPONIVEIS[coluna_key].get("getter")
            if getter:
                valor = getter(item)
                with gc.lock_resultados:
                    if coluna_key not in gc.resultados_colunas:
                        gc.resultados_colunas[coluna_key] = []

                    gc.resultados_colunas[coluna_key].append((item, valor))

                QMetaObject.invokeMethod(gc.interface, "atualizar_coluna_interface", Qt.QueuedConnection,)

        except queue.Empty:
            continue

        except Exception as e:
            print(f"Erro na thread da coluna '{coluna_key}': {e}")
