from PySide6.QtGui import QAction
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configurar_menu_opcoes(self, menu_opcoes):
    try:
        self._criar_submenu_idiomas(menu_opcoes)
        menu_opcoes.addSeparator()
        acao_sobre = QAction(self.loc.get_text("about"), self.interface)
        acao_sobre.triggered.connect(self._exibir_sobre)
        menu_opcoes.addAction(acao_sobre)

    except Exception as e:
        logger.error(f"Erro ao configurar menu opções: {e}", exc_info=True)
