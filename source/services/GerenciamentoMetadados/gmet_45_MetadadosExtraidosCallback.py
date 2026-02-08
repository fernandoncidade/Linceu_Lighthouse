from PySide6.QtCore import QMetaObject, Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _metadados_extraidos_callback(gc, futuro):
    try:
        metadados = futuro.result()
        QMetaObject.invokeMethod(gc.interface, "atualizar_colunas_tabela", Qt.QueuedConnection)

    except Exception as e:
        logger.error(f"Erro ao processar metadados extraídos: {e}", exc_info=True)
