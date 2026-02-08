from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_graficos_apos_mudanca_idioma(self, novo_idioma):
    try:
        if self.dialog_estatisticas and self.dialog_estatisticas.isVisible():
            self._atualizando_idioma = True
            try:
                self.dialog_estatisticas.setWindowTitle(self.loc.get_text("statistics"))
                if hasattr(self, 'btn_toggle_painel'):
                    if self.painel_recolhido:
                        texto_expandir = self.loc.get_text("expand_selection_panel")
                        self.btn_toggle_painel.setText(texto_expandir)

                    else:
                        texto_ocultar = self.loc.get_text("hide_selection_panel")
                        self.btn_toggle_painel.setText(texto_ocultar)

                    self._atualizar_layout_apos_mudanca_botao()

                self._atualizar_textos_painel_selecao()
                self._ajustar_largura_painel_selecao()
                self._atualizar_graficos_sem_fechar()

            finally:
                self._atualizando_idioma = False

    except Exception as e:
        logger.error(f"Erro ao atualizar gráficos após mudança de idioma: {e}", exc_info=True)
