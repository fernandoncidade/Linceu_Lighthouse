from PySide6.QtGui import QAction, QActionGroup
from GerenciamentoUI.GerenciamentoMenusUI.gmui_01_MenuPersistente import MenuPersistente
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_submenu_idiomas(self, menu_opcoes):
    try:
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

    except Exception as e:
        logger.error(f"Erro ao criar submenu de idiomas: {e}", exc_info=True)
