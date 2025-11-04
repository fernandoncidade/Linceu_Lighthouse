from PySide6.QtCore import Slot
from utils.LogManager import LogManager
logger = LogManager.get_logger()

@Slot(str)
def on_idioma_alterado(self, idioma: str):
    try:
        self.atualizar_interface(idioma)
        self.atualizar_status(idioma)

        from PySide6.QtCore import QLocale
        fmt = QLocale().dateTimeFormat(QLocale.ShortFormat)
        if hasattr(self, 'data_inicial'):
            self.data_inicial.setDisplayFormat(fmt)

        if hasattr(self, 'data_final'):
            self.data_final.setDisplayFormat(fmt)

        self.filtroAplicado.emit()

    except Exception as e:
        logger.error(f"Erro no slot de idioma_alterado: {e}", exc_info=True)
