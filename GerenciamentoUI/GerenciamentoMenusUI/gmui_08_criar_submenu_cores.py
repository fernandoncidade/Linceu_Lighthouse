from PySide6.QtGui import QAction
from GerenciamentoUI.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_submenu_cores(self, menu_configuracoes):
    try:
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

    except Exception as e:
        logger.error(f"Erro ao criar submenu cores: {e}", exc_info=True)
