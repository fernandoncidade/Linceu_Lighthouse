from PySide6.QtGui import QAction
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configurar_menu_opcoes(self, menu_opcoes):
    try:
        self._criar_submenu_idiomas(menu_opcoes)
        menu_opcoes.addSeparator()

        try:
            acao_manual = QAction(self.loc.get_text("manual"), self.interface)

        except Exception:
            acao_manual = QAction("Manual", self.interface)

        try:
            acao_manual.setShortcut("Ctrl+M")

        except Exception:
            pass

        acao_manual.triggered.connect(self._exibir_manual)
        menu_opcoes.addAction(acao_manual)
        menu_opcoes.addSeparator()
        acao_sobre = QAction(self.loc.get_text("about"), self.interface)

        try:
            acao_sobre.setShortcut("Ctrl+I")

        except Exception:
            pass

        acao_sobre.triggered.connect(self._exibir_sobre)
        menu_opcoes.addAction(acao_sobre)

        try:
            texto_ajuda = self.loc.get_text("help") if hasattr(self.loc, 'get_text') else None

        except Exception:
            texto_ajuda = None

        if not texto_ajuda:
            texto_ajuda = "Ajuda"

        acao_ajuda = QAction(texto_ajuda, self.interface)

        try:
            acao_ajuda.setShortcut("F1")

        except Exception:
            pass

        acao_ajuda.triggered.connect(self._exibir_ajuda)
        menu_opcoes.addAction(acao_ajuda)

    except Exception as e:
        logger.error(f"Erro ao configurar menu opções: {e}", exc_info=True)
