from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def notificar_alteracao_idioma(self):
    try:
        from PySide6.QtWidgets import QApplication
        import shiboken6
        import inspect

        def _safe_call(func, *args, **kwargs):
            try:
                return func(*args, **kwargs)

            except TypeError as e:
                try:
                    sig = inspect.signature(func)
                    params = list(sig.parameters.keys())
                    if 'status_map' in params:
                        return func({})

                except Exception:
                    pass

                try:
                    return func()

                except Exception as inner:
                    logger.error(f"Falha ao chamar {func}: {inner}", exc_info=True)
                    return None

        for widget in QApplication.topLevelWidgets():
            if not shiboken6.isValid(widget):
                continue

            if hasattr(widget, 'atualizar_status'):
                try:
                    _safe_call(widget.atualizar_status)

                except Exception as e:
                    logger.error(f"Erro ao chamar atualizar_status no widget {widget}: {e}", exc_info=True)

            if hasattr(widget, 'atualizar_interface'):
                try:
                    _safe_call(widget.atualizar_interface)

                except Exception as e:
                    logger.error(f"Erro ao chamar atualizar_interface no widget {widget}: {e}", exc_info=True)

            if hasattr(widget, 'gerenciador_eventos_ui'):
                try:
                    if hasattr(widget.gerenciador_eventos_ui, 'atualizar_interface'):
                        _safe_call(widget.gerenciador_eventos_ui.atualizar_interface)

                except Exception as e:
                    logger.error(f"Erro ao atualizar interface do gerenciador de eventos: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao notificar alteração de idioma: {e}", exc_info=True)
