from PySide6.QtGui import QAction
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configurar_menu_arquivo(self, menu_arquivo):
    try:
        acoes = [
            {"texto": "select_dir", "slot": self.interface.selecionar_diretorio, "shortcut": "Ctrl+Shift+O"},
            {"texto": "start_stop", "slot": self.interface.alternar_analise_diretorio, "shortcut": "Ctrl+R"},
            {"texto": "pause_analysis", "slot": self.interface.gerenciador_botoes.pausar_monitoramento_ou_escaneamento, "shortcut": "Ctrl+P"},
            {"texto": "save_as", "slot": self.interface.abrir_salvar_como, "shortcut": "Ctrl+Shift+S"},
            {"texto": "save", "slot": self.interface.salvar_dados, "shortcut": "Ctrl+S"},
            {"texto": "statistics", "slot": self.interface.mostrar_estatisticas, "shortcut": "Ctrl+G"},
            {"texto": "clear_data", "slot": self.interface.limpar_dados, "shortcut": "Ctrl+L"},
            {"texto": "exit", "slot": self.interface.sair_aplicacao, "shortcut": "Ctrl+Q"}
        ]

        for acao in acoes:
            item_menu = QAction(self.loc.get_text(acao["texto"]), self.interface)

            try:
                shortcut = acao.get("shortcut")
                if shortcut:
                    item_menu.setShortcut(shortcut)

            except Exception:
                pass

            item_menu.triggered.connect(acao["slot"])
            menu_arquivo.addAction(item_menu)

    except Exception as e:
        logger.error(f"Erro ao configurar menu arquivo: {e}", exc_info=True)
