from PySide6.QtGui import QAction, QActionGroup
from source.GerenciamentoUI.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from utils.LogManager import LogManager
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

    except Exception as e:
        logger.error(f"Erro ao configurar menu configurações: {e}", exc_info=True)
