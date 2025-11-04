from source.GerenciamentoUI.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def criar_menu_principal(self):
    try:
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

    except Exception as e:
        logger.error(f"Erro ao criar menu principal: {e}", exc_info=True)
