from PySide6.QtGui import QAction
from source.GerenciamentoUI.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_submenu_exportacao(self, menu_configuracoes):
    try:
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

    except Exception as e:
        logger.error(f"Erro ao criar submenu de exportação: {e}", exc_info=True)
