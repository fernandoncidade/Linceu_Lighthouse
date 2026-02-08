from utils.LogManager import LogManager
from PySide6.QtCore import QTimer
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

                if self.gerador_atual:
                    self.gerador_atual.atualizar_textos_traduzidos()

                def executar_atualizacao():
                    try:
                        if self.gerador_atual and self.tab_widget:
                            graficos_atualizados = self._criar_lista_graficos(self.gerador_atual)
                            mapeamento_funcoes = self._criar_mapeamento_funcoes(graficos_atualizados)
                            self._atualizar_dados_graficos_com_novos_titulos(graficos_atualizados, mapeamento_funcoes)
                            self._regenerar_graficos_existentes(graficos_atualizados, mapeamento_funcoes)
                            estados_checkboxes = self._obter_estados_checkboxes()
                            self._atualizar_checkboxes_graficos(graficos_atualizados, estados_checkboxes, mapeamento_funcoes)
                            _atualizar_abas_graficos_fallback(self, graficos_atualizados, mapeamento_funcoes)

                    except Exception as e:
                        logger.error(f"Erro na execução da atualização de gráficos por idioma: {e}", exc_info=True)

                    finally:
                        self._atualizando_idioma = False

                QTimer.singleShot(100, executar_atualizacao)

            except Exception as e:
                logger.error(f"Erro durante atualização inicial de idioma: {e}", exc_info=True)
                self._atualizando_idioma = False

    except Exception as e:
        logger.error(f"Erro ao atualizar gráficos após mudança de idioma: {e}", exc_info=True)

def _atualizar_abas_graficos_fallback(self, graficos_atualizados, mapeamento_funcoes):
    try:
        if not self.tab_widget or self.tab_widget.count() == 0:
            return

        for i in range(self.tab_widget.count()):
            titulo_atual = self.tab_widget.tabText(i)
            func_correspondente = None
            for titulo_antigo, data in self.checkboxes_graficos.items():
                if titulo_antigo == titulo_atual:
                    func_correspondente = data['grafico_data']['func']
                    break

                elif titulo_atual in self.graficos_dados:
                    grafico_data = self.graficos_dados[titulo_atual]
                    if grafico_data.get('func'):
                        func_correspondente = grafico_data['func']
                        break

            if func_correspondente:
                novo_titulo = None
                for grafico in graficos_atualizados:
                    if grafico['func'] == func_correspondente:
                        novo_titulo = grafico['titulo']
                        break

                if novo_titulo and novo_titulo != titulo_atual:
                    self.tab_widget.setTabText(i, novo_titulo)
                    logger.debug(f"Aba atualizada de '{titulo_atual}' para '{novo_titulo}'")

    except Exception as e:
        logger.error(f"Erro ao atualizar abas dos gráficos (fallback): {e}", exc_info=True)
