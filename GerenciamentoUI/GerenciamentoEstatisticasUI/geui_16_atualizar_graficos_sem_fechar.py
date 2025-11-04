from utils.LogManager import LogManager
logger = LogManager.get_logger()

try:
    from shiboken6 import isValid as _shiboken_is_valid

except Exception:
    _shiboken_is_valid = None

def _close_widget_safe(widget):
    try:
        if not widget:
            return

        if _shiboken_is_valid and not _shiboken_is_valid(widget):
            return

        try:
            widget.close()

        except RuntimeError:
            try:
                widget.deleteLater()

            except Exception:
                pass

    except Exception:
        pass

def _atualizar_graficos_sem_fechar(self):
    if getattr(self, '_atualizando_idioma', False):
        return

    try:
        if not self.dialog_estatisticas or not self.dialog_estatisticas.isVisible():
            return

        self.dialog_estatisticas.setWindowTitle(self.loc.get_text("statistics"))

        if self.gerador_atual and self.tab_widget:
            self.gerador_atual.atualizar_textos_traduzidos()

            graficos_atualizados = self._criar_lista_graficos(self.gerador_atual)
            estados_checkboxes = self._obter_estados_checkboxes()
            mapeamento_funcoes = self._criar_mapeamento_funcoes(graficos_atualizados)

            if hasattr(self, 'progress_regeneracao') and self.progress_regeneracao:
                _close_widget_safe(self.progress_regeneracao)
                self.progress_regeneracao = None

            self._regenerar_graficos_existentes(graficos_atualizados, mapeamento_funcoes)
            self._atualizar_checkboxes_graficos(graficos_atualizados, estados_checkboxes, mapeamento_funcoes)

    except Exception as e:
        logger.error(f"Erro ao atualizar gráficos sem fechar: {e}", exc_info=True)
