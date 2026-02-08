from PySide6.QtGui import QAction, QActionGroup
from source.ui.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configurar_menu_configuracoes(self, menu_configuracoes):
    try:
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
        self._criar_acao_toggle_desempenho(menu_configuracoes)

        acao_toggle_estrutura = QAction(self.loc.get_text("toggle_structure_view"), self.interface)
        acao_toggle_estrutura.setCheckable(True)
        acao_toggle_estrutura.setChecked(getattr(self.interface, "estrutura_ativa", False))
        acao_toggle_estrutura.triggered.connect(lambda checked: self.interface.alternar_estrutura_diretorios(checked))
        menu_configuracoes.addAction(acao_toggle_estrutura)
        self.acao_toggle_estrutura = acao_toggle_estrutura

    except Exception as e:
        logger.error(f"Erro ao configurar menu configurações: {e}", exc_info=True)
