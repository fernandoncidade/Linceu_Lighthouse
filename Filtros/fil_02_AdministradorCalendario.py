from PySide6.QtWidgets import QCalendarWidget
from PySide6.QtCore import Qt, QDateTime, QLocale
from utils.LogManager import LogManager


class AdministradorCalendario:
    def __init__(self, parent):
        self.parent = parent
        LogManager.debug("AdministradorCalendario inicializado")

    def mostrar_calendario(self, campo_data):
        logger = LogManager.get_logger()
        try:
            logger.debug(f"Exibindo calendário para seleção de data (valor atual: {campo_data.dateTime().toString()})")

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

            logger.debug(f"Calendário exibido com sucesso com locale: {locale_qt.name()}")

        except Exception as e:
            logger.error(f"Erro ao exibir calendário: {e}", exc_info=True)

    def selecionar_data(self, data, campo_data, calendario):
        logger = LogManager.get_logger()
        try:
            data_antiga = campo_data.dateTime().toString()
            dt = QDateTime(data, campo_data.dateTime().time())
            campo_data.setDateTime(dt)
            calendario.close()

            logger.debug(f"Data selecionada: alterada de {data_antiga} para {dt.toString()}")

            self.parent.administrador_filtros.aplicar_filtros()
            logger.debug("Filtros reaplicados após seleção de data")

        except Exception as e:
            logger.error(f"Erro ao selecionar data no calendário: {e}", exc_info=True)
            calendario.close()
