from PySide6.QtGui import QAction, QActionGroup
from source.ui.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_submenu_colunas(self, menu_configuracoes):
    try:
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

        try:
            acao_selecionar_todas.setShortcut("Ctrl+A")

        except Exception:
            pass

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

        try:
            self.acao_ordenar_linhas.setShortcut("Ctrl+O")

        except Exception:
            pass

        submenu_colunas.addAction(self.acao_ordenar_linhas)

    except Exception as e:
        logger.error(f"Erro ao criar submenu colunas: {e}", exc_info=True)
