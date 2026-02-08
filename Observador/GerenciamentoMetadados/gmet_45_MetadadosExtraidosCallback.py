from PySide6.QtCore import QMetaObject, Qt

def _metadados_extraidos_callback(gc, futuro):
    metadados = futuro.result()
    QMetaObject.invokeMethod(gc.interface, "atualizar_colunas_tabela", Qt.QueuedConnection)
