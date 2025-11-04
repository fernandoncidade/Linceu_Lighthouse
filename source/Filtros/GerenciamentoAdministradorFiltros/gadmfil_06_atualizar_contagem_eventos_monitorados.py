from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_contagem_eventos_monitorados(self):
    try:
        main_loc = self.parent.loc if hasattr(self.parent, 'loc') else None

        if main_loc is None:
            from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
            main_loc = LocalizadorQt()

        if self.parent and hasattr(self.parent, 'tabela_dados'):
            try:
                total = self.parent.tabela_dados.rowCount()
                return f"{main_loc.get_text('events_monitored')}: {total}"

            except RuntimeError:
                logger.error("Tabela de dados não está mais disponível", exc_info=True)

        from PySide6.QtWidgets import QApplication

        for widget in QApplication.topLevelWidgets():
            if hasattr(widget, 'tabela_dados'):
                try:
                    total = widget.tabela_dados.rowCount()
                    return f"{main_loc.get_text('events_monitored')}: {total}"

                except RuntimeError:
                    logger.error("Tabela de dados da janela principal não está disponível", exc_info=True)
                    break

        return f"{main_loc.get_text('events_monitored')}: 0"

    except Exception as e:
        logger.error(f"Erro ao atualizar contagem eventos monitorados: {e}", exc_info=True)
        return "Eventos monitorados: 0"
