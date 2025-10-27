from PySide6.QtWidgets import QCalendarWidget
from PySide6.QtCore import Qt, QDateTime, QLocale
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class AdministradorCalendario:
    def __init__(self, parent):
        self.parent = parent

    def mostrar_calendario(self, campo_data):
        try:
            calendario = QCalendarWidget(self.parent)
            calendario.setWindowFlags(Qt.Popup)

            try:
                idioma = getattr(self.parent, "loc", None).idioma_atual if hasattr(self.parent, "loc") else None

            except Exception:
                idioma = None

            locale_qt = QLocale(idioma) if idioma else QLocale()
            calendario.setLocale(locale_qt)
            calendario.setFirstDayOfWeek(locale_qt.firstDayOfWeek())
            calendario.clicked.connect(lambda date: self.selecionar_data(date, campo_data, calendario))
            calendario.setSelectedDate(campo_data.date())
            pos = campo_data.mapToGlobal(campo_data.rect().bottomLeft())
            calendario.move(pos)
            calendario.show()

        except Exception as e:
            logger.error(f"Erro ao exibir calendário: {e}", exc_info=True)

    def selecionar_data(self, data, campo_data, calendario):
        try:
            data_antiga = campo_data.dateTime().toString()
            dt = QDateTime(data, campo_data.dateTime().time())
            campo_data.setDateTime(dt)
            calendario.close()
            self.parent.administrador_filtros.aplicar_filtros()

        except Exception as e:
            logger.error(f"Erro ao selecionar data no calendário: {e}", exc_info=True)
            calendario.close()
