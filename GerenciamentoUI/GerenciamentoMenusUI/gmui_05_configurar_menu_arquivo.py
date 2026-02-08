from PySide6.QtGui import QAction
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _configurar_menu_arquivo(self, menu_arquivo):
    try:
        acoes = [
            {"texto": "select_dir", "slot": self.interface.selecionar_diretorio},
            {"texto": "start_stop", "slot": self.interface.alternar_analise_diretorio},
            {"texto": "pause_analysis", "slot": self.interface.gerenciador_botoes.pausar_monitoramento_ou_escaneamento},
            {"texto": "save_as", "slot": self.interface.abrir_salvar_como},
            {"texto": "save", "slot": self.interface.salvar_dados},
            {"texto": "statistics", "slot": self.interface.mostrar_estatisticas},
            {"texto": "clear_data", "slot": self.interface.limpar_dados},
            {"texto": "exit", "slot": self.interface.sair_aplicacao}
        ]
        for acao in acoes:
            item_menu = QAction(self.loc.get_text(acao["texto"]), self.interface)
            item_menu.triggered.connect(acao["slot"])
            menu_arquivo.addAction(item_menu)

    except Exception as e:
        logger.error(f"Erro ao configurar menu arquivo: {e}", exc_info=True)
