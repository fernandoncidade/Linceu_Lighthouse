from utils.LogManager import LogManager
logger = LogManager.get_logger()

def notificar_alteracao_idioma(self):
    try:
        from PySide6.QtWidgets import QApplication
        import shiboken6

        for widget in QApplication.topLevelWidgets():
            if not shiboken6.isValid(widget):
                continue

            if hasattr(widget, 'atualizar_status'):
                widget.atualizar_status()

            if hasattr(widget, 'atualizar_interface'):
                widget.atualizar_interface()

            if hasattr(widget, 'gerenciador_eventos_ui'):
                try:
                    if hasattr(widget.gerenciador_eventos_ui, 'atualizar_interface'):
                        widget.gerenciador_eventos_ui.atualizar_interface()

                except Exception as e:
                    logger.error(f"Erro ao atualizar interface do gerenciador de eventos: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao notificar alteração de idioma: {e}", exc_info=True)
