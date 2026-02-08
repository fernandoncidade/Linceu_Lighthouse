from PySide6.QtGui import QAction
from source.ui.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_submenu_colunas_coloridas(self, menu_configuracoes):
    try:
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

        try:
            acao_selecionar_todas.setShortcut("Ctrl+Shift+A")

        except Exception:
            pass

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

    except Exception as e:
        logger.error(f"Erro ao criar submenu colunas coloridas: {e}", exc_info=True)
