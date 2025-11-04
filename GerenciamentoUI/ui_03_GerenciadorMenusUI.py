import os
from utils.LogManager import LogManager
from PySide6.QtGui import QAction, QActionGroup, QColor, QIcon, QPixmap, QPainter
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QTranslator
from GerenciamentoUI.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from GerenciamentoUI.GerenciamentoMenusUI.gmui_02_GerenciadorCores import GerenciadorCores
from GerenciamentoUI.GerenciamentoMenusUI.gmui_03_SobreDialog import SobreDialog
from GerenciamentoUI.ui_11_DialogoCores import DialogoPaletaCores
from GerenciamentoUI.ui_14_OpcoesSobre import (
    LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US, LICENSE_TEXT_ES_ES,
    LICENSE_TEXT_FR_FR, LICENSE_TEXT_IT_IT, LICENSE_TEXT_DE_DE,
    SITE_LICENSES, NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US,
    NOTICE_TEXT_ES_ES, NOTICE_TEXT_FR_FR, NOTICE_TEXT_IT_IT,
    NOTICE_TEXT_DE_DE, ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US,
    ABOUT_TEXT_ES_ES, ABOUT_TEXT_FR_FR, ABOUT_TEXT_IT_IT,
    ABOUT_TEXT_DE_DE, Privacy_Policy_pt_BR, Privacy_Policy_en_US,
    Privacy_Policy_es_ES, Privacy_Policy_fr_FR, Privacy_Policy_it_IT,
    Privacy_Policy_de_DE, History_APP_pt_BR, History_APP_en_US,
    History_APP_es_ES, History_APP_fr_FR, History_APP_it_IT,
    History_APP_de_DE, RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US, RELEASE_NOTES_es_ES,
    RELEASE_NOTES_fr_FR, RELEASE_NOTES_it_IT, RELEASE_NOTES_de_DE
)

logger = LogManager.get_logger()


class GerenciadorMenusUI:
    def __init__(self, interface_principal):
        self.interface = interface_principal
        self.loc = interface_principal.loc
        self.acoes_colunas = {}
        self.gerenciador_cores = GerenciadorCores(interface_principal)
        self.interface._ordenacao_linhas_habilitada = False
        self._acoes_idioma = {}
        self._trocando_idioma = False
        self._aguardando_conclusao_traducao = False
        try:
            if hasattr(self.interface, "loc") and hasattr(self.interface.loc, "traducoes_carregadas"):
                self.interface.loc.traducoes_carregadas.connect(self._on_traducoes_carregadas)

        except Exception as e:
            logger.warning(f"Falha ao conectar sinal de traduções: {e}")

    def criar_menu_principal(self):
        menu_bar = self.interface.menuBar()
        menu_bar.clear()
        menu_arquivo = MenuPersistente(self.loc.get_text("file_menu"), self.interface)
        menu_configuracoes = MenuPersistente(self.loc.get_text("settings"), self.interface)
        menu_opcoes = MenuPersistente(self.loc.get_text("options_menu"), self.interface)
        menu_bar.addMenu(menu_arquivo)
        menu_bar.addMenu(menu_configuracoes)
        menu_bar.addMenu(menu_opcoes)
        self._configurar_menu_arquivo(menu_arquivo)
        self._configurar_menu_configuracoes(menu_configuracoes)
        self._configurar_menu_opcoes(menu_opcoes)

    def _configurar_menu_arquivo(self, menu_arquivo):
        acoes = [
            {"texto": "select_dir", "slot": self.interface.selecionar_diretorio},
            {"texto": "start_stop", "slot": self.interface.alternar_analise_diretorio},
            {"texto": "pause_analysis", "slot": self.interface.gerenciador_botoes.pausar_monitoramento_ou_escaneamento},
            {"texto": "save_as", "slot": self.interface.abrir_salvar_como},
            {"texto": "save", "slot": self.interface.salvar_dados},
            {"texto": "statistics", "slot": self.interface.mostrar_estatisticas},
            {"texto": "clear_data", "slot": self.interface.limpar_dados},
            {"texto": "exit", "slot": self.interface.sair_aplicacao}
        ]
        for acao in acoes:
            item_menu = QAction(self.loc.get_text(acao["texto"]), self.interface)
            item_menu.triggered.connect(acao["slot"])
            menu_arquivo.addAction(item_menu)

    def _configurar_menu_configuracoes(self, menu_configuracoes):
        submenu_filtros = MenuPersistente(self.loc.get_text("filters"), self.interface)
        menu_configuracoes.addMenu(submenu_filtros)
        grupo_filtros = QActionGroup(self.interface)
        grupo_filtros.setExclusive(False)
        for op in ["op_moved", "op_renamed", "op_added", "op_deleted", "op_modified", "op_scanned"]:
            acao_filtro = QAction(self.loc.get_text(op), self.interface)
            acao_filtro.setCheckable(True)
            acao_filtro.setChecked(True)
            acao_filtro.setData(op)
            acao_filtro.triggered.connect(self.interface.alternar_filtro)
            grupo_filtros.addAction(acao_filtro)
            submenu_filtros.addAction(acao_filtro)

        submenu_filtros.addSeparator()
        acao_filtros_avancados = QAction(self.loc.get_text("advanced_filters"), self.interface)
        acao_filtros_avancados.triggered.connect(self.interface.abrir_janela_filtros)
        submenu_filtros.addAction(acao_filtros_avancados)
        self._criar_submenu_colunas(menu_configuracoes)
        self._criar_submenu_colunas_coloridas(menu_configuracoes)
        self._criar_submenu_cores(menu_configuracoes)
        self._criar_submenu_exportacao(menu_configuracoes)

    def _configurar_menu_opcoes(self, menu_opcoes):
        self._criar_submenu_idiomas(menu_opcoes)
        menu_opcoes.addSeparator()
        acao_sobre = QAction(self.loc.get_text("about"), self.interface)
        acao_sobre.triggered.connect(self._exibir_sobre)
        menu_opcoes.addAction(acao_sobre)

    def _criar_submenu_cores(self, menu_configuracoes):
        submenu_cores = MenuPersistente(self.loc.get_text("configure_colors"), self.interface)
        menu_configuracoes.addMenu(submenu_cores)
        submenu_cores_operacoes = MenuPersistente(self.loc.get_text("operation_colors"), self.interface)
        submenu_cores.addMenu(submenu_cores_operacoes)
        tipos_operacoes = {
            "op_renamed": self.loc.get_text("op_renamed"),
            "op_added": self.loc.get_text("op_added"),
            "op_deleted": self.loc.get_text("op_deleted"),
            "op_modified": self.loc.get_text("op_modified"),
            "op_moved": self.loc.get_text("op_moved"),
            "op_scanned": self.loc.get_text("op_scanned")
        }
        for op_key, op_text in tipos_operacoes.items():
            acao_cor = QAction(op_text, self.interface)
            acao_cor.setData(op_key)
            cor_atual = self.gerenciador_cores.obter_cor_hex(op_key)
            icone = self._criar_icone_cor(cor_atual)
            acao_cor.setIcon(icone)
            acao_cor.triggered.connect(lambda checked, op=op_key: self._abrir_dialogo_cor(op))
            submenu_cores_operacoes.addAction(acao_cor)

        submenu_cores.addSeparator()
        acao_resetar_cores = QAction(self.loc.get_text("reset_colors"), self.interface)
        acao_resetar_cores.triggered.connect(
            lambda: self.interface.gerenciador_eventos_ui.resetar_cores(
                self.gerenciador_cores,
                self.acao_exportar_colunas_ativas,
                self.acao_exportar_filtros_ativos,
                self.acao_exportar_selecao,
                self.criar_menu_principal
            )
        )
        submenu_cores.addAction(acao_resetar_cores)

    def _criar_icone_cor(self, cor_hex):
        tamanho = 16
        pixmap = QPixmap(tamanho, tamanho)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(cor_hex))
        painter.drawRect(0, 0, tamanho, tamanho)
        painter.end()
        return QIcon(pixmap)

    def _abrir_dialogo_cor(self, tipo_operacao):
        try:
            cor_atual = QColor(self.gerenciador_cores.obter_cor_hex(tipo_operacao))
            nome_operacao = self.loc.get_text(tipo_operacao)
            titulo = f"{self.loc.get_text('select_color_for')} {nome_operacao}"
            dialogo = DialogoPaletaCores(cor_atual, self.interface, titulo)
            GerenciadorCores.aplicar_icone_paleta(dialogo, tipo="paleta")
            dialogo.show()
            def on_cor_selecionada(nova_cor):
                if nova_cor.isValid():
                    self.gerenciador_cores.definir_cor(tipo_operacao, nova_cor.name())
                    self.gerenciador_cores.salvar_cores()
                    self.gerenciador_cores.atualizar_cores_no_sistema()
                    if hasattr(self.interface, "gerenciador_tabela"):
                        self.interface.gerenciador_tabela.atualizar_cores_colunas(aplicar_em_massa=True)

                    exportar_colunas_ativas = self.acao_exportar_colunas_ativas.isChecked()
                    exportar_filtros_ativos = self.acao_exportar_filtros_ativos.isChecked()
                    exportar_selecao = self.acao_exportar_selecao.isChecked()
                    self.criar_menu_principal()
                    self.acao_exportar_colunas_ativas.setChecked(exportar_colunas_ativas)
                    self.acao_exportar_filtros_ativos.setChecked(exportar_filtros_ativos)
                    self.acao_exportar_selecao.setChecked(exportar_selecao)
                    mensagem = self.loc.get_text("color_changed_success")
                    QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem)
                    logger.info(f"Cor de {tipo_operacao} alterada para {nova_cor.name()}")
                    dialogo.close()

            dialogo.corSelecionada.connect(on_cor_selecionada)

        except Exception as e:
            logger.error(f"Erro ao abrir diálogo de cor: {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")

    def _criar_submenu_colunas(self, menu_configuracoes):
        submenu_colunas = MenuPersistente(self.loc.get_text("configure_columns"), self.interface)
        menu_configuracoes.addMenu(submenu_colunas)
        submenu_colunas_interno = MenuPersistente(self.loc.get_text("columns"), self.interface)
        submenu_colunas.addMenu(submenu_colunas_interno)
        grupo_colunas = QActionGroup(self.interface)
        grupo_colunas.setExclusive(False)
        self.acoes_colunas.clear()
        for key, coluna in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]):
            acao_coluna = QAction(coluna["nome"], self.interface)
            acao_coluna.setCheckable(True)
            acao_coluna.setChecked(coluna["visivel"])
            acao_coluna.setData(key)
            acao_coluna.triggered.connect(self.interface.alternar_visibilidade_coluna)
            grupo_colunas.addAction(acao_coluna)
            submenu_colunas_interno.addAction(acao_coluna)
            self.acoes_colunas[key] = acao_coluna

        submenu_colunas.addSeparator()
        acao_selecionar_todas = QAction(self.loc.get_text("select_all_columns"), self.interface)
        acao_selecionar_todas.triggered.connect(self.selecionar_todas_colunas)
        submenu_colunas.addAction(acao_selecionar_todas)
        acao_resetar_colunas = QAction(self.loc.get_text("reset_columns"), self.interface)
        acao_resetar_colunas.triggered.connect(self.interface.resetar_colunas)
        submenu_colunas.addAction(acao_resetar_colunas)
        submenu_colunas.addSeparator()
        self.acao_ordenar_linhas = QAction(self.loc.get_text("sort_rows"), self.interface)
        self.acao_ordenar_linhas.setCheckable(True)
        self.acao_ordenar_linhas.setChecked(getattr(self.interface, '_ordenacao_linhas_habilitada', False))
        self.acao_ordenar_linhas.triggered.connect(self._alternar_ordenacao_linhas)
        submenu_colunas.addAction(self.acao_ordenar_linhas)

    def _alternar_ordenacao_linhas(self):
        try:
            self.interface._ordenacao_linhas_habilitada = self.acao_ordenar_linhas.isChecked()
            if hasattr(self.interface, 'tabela_dados') and self.interface.tabela_dados is not None:
                self.interface.tabela_dados.setSortingEnabled(self.interface._ordenacao_linhas_habilitada)
                estado = "habilitada" if self.interface._ordenacao_linhas_habilitada else "desabilitada"
                logger.info(f"Ordenação de linhas {estado}")
                estado_texto = self.loc.get_text("enabled") if self.interface._ordenacao_linhas_habilitada else self.loc.get_text("disabled")
                mensagem = f"{self.loc.get_text('sort_rows')} {estado_texto}"
                QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem)

        except Exception as e:
            logger.error(f"Erro ao alternar ordenação de linhas: {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")

    def _criar_submenu_colunas_coloridas(self, menu_configuracoes):
        submenu_colorir_colunas = MenuPersistente(self.loc.get_text("color_columns"), self.interface)
        menu_configuracoes.addMenu(submenu_colorir_colunas)
        submenu_colunas_interno = MenuPersistente(self.loc.get_text("columns"), self.interface)
        submenu_colorir_colunas.addMenu(submenu_colunas_interno)
        colunas_coloridas = set()
        if hasattr(self.interface, 'gerenciador_tabela') and hasattr(self.interface.gerenciador_tabela, 'colunas_para_colorir'):
            colunas_coloridas = self.interface.gerenciador_tabela.colunas_para_colorir

        for key, coluna in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]):
            acao_col_color = QAction(coluna["nome"], self.interface)
            acao_col_color.setCheckable(True)
            if key == "tipo_operacao":
                acao_col_color.setChecked(True)

            else:
                acao_col_color.setChecked(key in colunas_coloridas)

            acao_col_color.setData(key)
            acao_col_color.triggered.connect(lambda checked, k=key: self.interface.gerenciador_tabela.set_coluna_colorir(k, checked))
            submenu_colunas_interno.addAction(acao_col_color)

        submenu_colorir_colunas.addSeparator()
        acao_selecionar_todas = QAction(self.loc.get_text("select_all_columns"), self.interface)
        acao_selecionar_todas.triggered.connect(self.selecionar_todas_cores_colunas)
        submenu_colorir_colunas.addAction(acao_selecionar_todas)
        acao_resetar_cores_tipo_operacao = QAction(self.loc.get_text("reset_column_colors"), self.interface)
        acao_resetar_cores_tipo_operacao.triggered.connect(
            lambda: self.interface.gerenciador_eventos_ui.redefinir_todas_colunas_cores(
                self.gerenciador_cores,
                self.acao_exportar_colunas_ativas,
                self.acao_exportar_filtros_ativos,
                self.acao_exportar_selecao,
                self.criar_menu_principal,
                self.interface.gerenciador_tabela
            )
        )
        submenu_colorir_colunas.addAction(acao_resetar_cores_tipo_operacao)

    def selecionar_todas_colunas(self):
        try:
            for key, acao in self.acoes_colunas.items():
                acao.setChecked(True)

            for key in self.acoes_colunas.keys():
                self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[key]["visivel"] = True

            self.interface.gerenciador_colunas.salvar_configuracoes()
            if hasattr(self.interface.gerenciador_tabela, 'atualizar_visibilidade_colunas'):
                self.interface.gerenciador_tabela.atualizar_visibilidade_colunas(atualizar_em_massa=True)

            else:
                self.interface.atualizar_visibilidade_colunas()

            logger.info("Todas as colunas foram selecionadas")
            msg_box = QMessageBox(self.interface)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle(self.loc.get_text("success"))
            msg_box.setText(self.loc.get_text("columns_select_success"))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

        except Exception as e:
            logger.error(f"Erro ao selecionar todas as colunas: {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")

    def selecionar_todas_cores_colunas(self):
        try:
            colunas_disponiveis = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS
            novas_colunas = list(colunas_disponiveis.keys())
            self.interface.gerenciador_tabela.set_colunas_colorir_em_massa(novas_colunas)
            exportar_colunas_ativas = self.acao_exportar_colunas_ativas.isChecked()
            exportar_filtros_ativos = self.acao_exportar_filtros_ativos.isChecked()
            exportar_selecao = self.acao_exportar_selecao.isChecked()
            self.criar_menu_principal()
            self.acao_exportar_colunas_ativas.setChecked(exportar_colunas_ativas)
            self.acao_exportar_filtros_ativos.setChecked(exportar_filtros_ativos)
            self.acao_exportar_selecao.setChecked(exportar_selecao)
            logger.info("Processo de coloração de todas as colunas iniciado")
            msg_box = QMessageBox(self.interface)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle(self.loc.get_text("success"))
            msg_box.setText(self.loc.get_text("colors_applied_success"))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

        except Exception as e:
            logger.error(f"Erro ao iniciar coloração de todas as colunas: {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")

    def _criar_submenu_exportacao(self, menu_configuracoes):
        submenu_exportacao = MenuPersistente(self.loc.get_text("export_options"), self.interface)
        menu_configuracoes.addMenu(submenu_exportacao)
        self.acao_exportar_colunas_ativas = QAction(self.loc.get_text("export_active_columns"), self.interface)
        self.acao_exportar_colunas_ativas.setCheckable(True)
        self.acao_exportar_colunas_ativas.setChecked(False)
        submenu_exportacao.addAction(self.acao_exportar_colunas_ativas)
        self.acao_exportar_filtros_ativos = QAction(self.loc.get_text("export_active_filters"), self.interface)
        self.acao_exportar_filtros_ativos.setCheckable(True)
        self.acao_exportar_filtros_ativos.setChecked(False)
        submenu_exportacao.addAction(self.acao_exportar_filtros_ativos)
        self.acao_exportar_selecao = QAction(self.loc.get_text("export_selected_data"), self.interface)
        self.acao_exportar_selecao.setCheckable(True)
        self.acao_exportar_selecao.setChecked(False)
        submenu_exportacao.addAction(self.acao_exportar_selecao)
        submenu_exportacao.addSeparator()
        acao_resetar_exportacao = QAction(self.loc.get_text("reset_export_options"), self.interface)
        acao_resetar_exportacao.triggered.connect(self._resetar_opcoes_exportacao)
        submenu_exportacao.addAction(acao_resetar_exportacao)

    def _resetar_opcoes_exportacao(self):
        try:
            self.acao_exportar_colunas_ativas.setChecked(False)
            self.acao_exportar_filtros_ativos.setChecked(False)
            self.acao_exportar_selecao.setChecked(False)
            mensagem_sucesso = self.loc.get_text("export_options_reset_success")
            QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem_sucesso)
            logger.info("Opções de exportação restauradas para valores padrão")

        except Exception as e:
            logger.error(f"Erro ao restaurar opções de exportação: {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")

    def _criar_submenu_idiomas(self, menu_opcoes):
        submenu_idiomas = MenuPersistente(self.loc.get_text("language"), self.interface)
        menu_opcoes.addMenu(submenu_idiomas)
        grupo_idiomas = QActionGroup(self.interface)
        self._acoes_idioma = {}
        for codigo, nome in self.loc.get_idiomas_disponiveis().items():
            acao_idioma = QAction(nome, self.interface)
            acao_idioma.setCheckable(True)
            acao_idioma.setChecked(codigo == self.loc.idioma_atual)
            acao_idioma.setData(codigo)
            acao_idioma.triggered.connect(lambda checked, c=codigo: self._confirmar_alteracao_idioma(c))
            grupo_idiomas.addAction(acao_idioma)
            submenu_idiomas.addAction(acao_idioma)
            self._acoes_idioma[codigo] = acao_idioma

    def _get_texto_traduzido_para_idioma(self, chave: str, idioma: str) -> str:
        try:
            translations_dir = getattr(self.loc, "translations_dir", None)
            if not translations_dir:
                return self.loc.get_text(chave)

            qm_path = os.path.join(translations_dir, f"linceu_{idioma}.qm")
            trans = QTranslator(self.interface)
            if trans.load(qm_path):
                txt = trans.translate("LinceuLighthouse", chave)
                if txt:
                    return txt

            return self.loc.get_text(chave)

        except Exception:
            return self.loc.get_text(chave)

    def _confirmar_alteracao_idioma(self, codigo_idioma: str):
        try:
            if not codigo_idioma or codigo_idioma == self.loc.idioma_atual:
                return

            titulo_atual = self.loc.get_text("warning")
            titulo_alvo = self._get_texto_traduzido_para_idioma("warning", codigo_idioma)
            titulo = f"{titulo_atual} / {titulo_alvo}" if titulo_alvo and titulo_alvo != titulo_atual else titulo_atual
            mensagem_atual = self.loc.get_text("language_change_performance_warning")
            mensagem_alvo = self._get_texto_traduzido_para_idioma("language_change_performance_warning", codigo_idioma)
            caixa = QMessageBox(self.interface)
            caixa.setIcon(QMessageBox.Warning)
            caixa.setWindowTitle(titulo)
            caixa.setText(mensagem_atual)
            if mensagem_alvo and mensagem_alvo != mensagem_atual:
                caixa.setInformativeText(mensagem_alvo)

            caixa.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            caixa.setDefaultButton(QMessageBox.No)
            yes_atual = self.loc.get_text("yes") or "Yes"
            yes_alvo = self._get_texto_traduzido_para_idioma("yes", codigo_idioma) or yes_atual
            no_atual = self.loc.get_text("no") or "No"
            no_alvo = self._get_texto_traduzido_para_idioma("no", codigo_idioma) or no_atual
            label_yes = yes_atual if yes_atual.lower() == yes_alvo.lower() else f"{yes_atual}/{yes_alvo}"
            label_no = no_atual if no_atual.lower() == no_alvo.lower() else f"{no_atual}/{no_alvo}"
            btn_yes = caixa.button(QMessageBox.Yes)
            btn_no = caixa.button(QMessageBox.No)
            if btn_yes:
                btn_yes.setText(label_yes)

            if btn_no:
                btn_no.setText(label_no)

            resposta = caixa.exec()
            acao = self._acoes_idioma.get(codigo_idioma)
            if resposta == QMessageBox.Yes:
                if acao is not None:
                    acao.setChecked(True)

                self._trocando_idioma = True
                self._aguardando_conclusao_traducao = True
                try:
                    if hasattr(self.interface, 'loc') and hasattr(self.interface.loc, 'set_idioma'):
                        self.interface.loc.set_idioma(codigo_idioma)

                    self.criar_menu_principal()

                finally:
                    self._trocando_idioma = False

            else:
                acao_atual = self._acoes_idioma.get(self.loc.idioma_atual)
                if acao_atual:
                    acao_atual.setChecked(True)

                if acao:
                    acao.setChecked(False)

        except Exception as e:
            logger.error(f"Erro ao confirmar alteração de idioma: {e}", exc_info=True)

    def _on_traducoes_carregadas(self, idioma: str):
        try:
            if getattr(self, "_aguardando_conclusao_traducao", False):
                self._aguardando_conclusao_traducao = False
                QMessageBox.information(
                    self.interface,
                    self.loc.get_text("success"),
                    self.loc.get_text("translation_complete")
                )

        except Exception as e:
            logger.error(f"Erro ao exibir confirmação de conclusão da tradução: {e}", exc_info=True)

    def _exibir_sobre(self):
        try:
            textos_sobre = {
                "pt_BR": ABOUT_TEXT_PT_BR,
                "en_US": ABOUT_TEXT_EN_US,
                "es_ES": ABOUT_TEXT_ES_ES,
                "fr_FR": ABOUT_TEXT_FR_FR,
                "it_IT": ABOUT_TEXT_IT_IT,
                "de_DE": ABOUT_TEXT_DE_DE
            }
            textos_licenca = {
                "pt_BR": LICENSE_TEXT_PT_BR,
                "en_US": LICENSE_TEXT_EN_US,
                "es_ES": LICENSE_TEXT_ES_ES,
                "fr_FR": LICENSE_TEXT_FR_FR,
                "it_IT": LICENSE_TEXT_IT_IT,
                "de_DE": LICENSE_TEXT_DE_DE
            }
            textos_aviso = {
                "pt_BR": NOTICE_TEXT_PT_BR,
                "en_US": NOTICE_TEXT_EN_US,
                "es_ES": NOTICE_TEXT_ES_ES,
                "fr_FR": NOTICE_TEXT_FR_FR,
                "it_IT": NOTICE_TEXT_IT_IT,
                "de_DE": NOTICE_TEXT_DE_DE
            }
            textos_privacidade = {
                "pt_BR": Privacy_Policy_pt_BR,
                "en_US": Privacy_Policy_en_US,
                "es_ES": Privacy_Policy_es_ES,
                "fr_FR": Privacy_Policy_fr_FR,
                "it_IT": Privacy_Policy_it_IT,
                "de_DE": Privacy_Policy_de_DE
            }
            history_texts = {
                "pt_BR": History_APP_pt_BR,
                "en_US": History_APP_en_US,
                "es_ES": History_APP_es_ES,
                "fr_FR": History_APP_fr_FR,
                "it_IT": History_APP_it_IT,
                "de_DE": History_APP_de_DE
            }
            release_notes_texts = {
                "pt_BR": RELEASE_NOTES_pt_BR,
                "en_US": RELEASE_NOTES_en_US,
                "es_ES": RELEASE_NOTES_es_ES,
                "fr_FR": RELEASE_NOTES_fr_FR,
                "it_IT": RELEASE_NOTES_it_IT,
                "de_DE": RELEASE_NOTES_de_DE
            }
            texto_sobre = textos_sobre.get(self.loc.idioma_atual, textos_sobre["en_US"])
            texto_licenca = textos_licenca.get(self.loc.idioma_atual, textos_licenca["en_US"])
            texto_aviso = textos_aviso.get(self.loc.idioma_atual, textos_aviso["en_US"])
            texto_privacidade = textos_privacidade.get(self.loc.idioma_atual, textos_privacidade["en_US"])
            texto_history = history_texts.get(self.loc.idioma_atual, history_texts["en_US"])
            texto_release_notes = release_notes_texts.get(self.loc.idioma_atual, release_notes_texts["en_US"])
            cabecalho_fixo = (
                "<h3>LINCEU LIGHTHOUSE</h3>"
                f"<p><b>{self.loc.get_text('version')}:</b> 0.0.5.0</p>"
                f"<p><b>{self.loc.get_text('authors')}:</b> Fernando Nillsson Cidade</p>"
                f"<p><b>{self.loc.get_text('description')}:</b> {self.loc.get_text('description_text')}</p>"
            )
            show_history_text = self.loc.get_text("show_history") or "Justificativa do Nome"
            dialog = SobreDialog(
                self.interface,
                titulo=f"{self.loc.get_text('about')} - LINCEU LIGHTHOUSE",
                texto_fixo=cabecalho_fixo,
                texto_history=texto_history,
                detalhes=texto_sobre,
                licencas=texto_licenca,
                sites_licencas=SITE_LICENSES,
                show_history_text=show_history_text,
                show_details_text=self.loc.get_text("show_details"),
                hide_details_text=self.loc.get_text("hide_details"),
                show_licenses_text=self.loc.get_text("show_licenses"),
                hide_licenses_text=self.loc.get_text("hide_licenses"),
                ok_text=self.loc.get_text("ok"),
                site_oficial_text=self.loc.get_text("site_oficial"),
                avisos=texto_aviso,
                show_notices_text=self.loc.get_text("show_notices"),
                hide_notices_text=self.loc.get_text("hide_notices"),
                Privacy_Policy=texto_privacidade,
                show_privacy_policy_text=self.loc.get_text("show_privacy_policy"),
                hide_privacy_policy_text=self.loc.get_text("hide_privacy_policy"),
                info_not_available_text=self.loc.get_text("information_not_available"),
                release_notes=texto_release_notes,
                show_release_notes_text=self.loc.get_text("show_release_notes") or "Release Notes"
            )
            tamanho_base_largura = 900
            tamanho_base_altura = 500
            largura_dialog = int(tamanho_base_largura * 1)
            altura_dialog = int(tamanho_base_altura * 1.8)
            dialog.resize(largura_dialog, altura_dialog)
            dialog.show()
            logger.info("Diálogo 'Sobre' exibido com sucesso")

        except Exception as e:
            logger.error(f"Erro ao exibir o diálogo 'Sobre': {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
