from PySide6.QtGui import QAction
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def sincronizar_menu_principal_com_filtros(self):
    try:
        from PySide6.QtWidgets import QApplication
        main_window = None

        for widget in QApplication.topLevelWidgets():
            if hasattr(widget, 'gerenciador_menus_ui'):
                main_window = widget
                break

        if main_window:
            menu_bar = main_window.menuBar()
            menu_configuracoes = None
            submenu_filtros = None

            for action in menu_bar.actions():
                if action.text() == main_window.loc.get_text("settings"):
                    menu_configuracoes = action.menu()
                    break

            if menu_configuracoes:
                for action in menu_configuracoes.actions():
                    if action.text() == main_window.loc.get_text("filters"):
                        submenu_filtros = action.menu()
                        break

            if submenu_filtros:
                for acao in submenu_filtros.actions():
                    if hasattr(acao, 'data') and callable(acao.data):
                        filtro = acao.data()
                        if (isinstance(filtro, str) and 
                            filtro in self.parent.checkboxes_operacao):
                            esta_marcado = self.parent.checkboxes_operacao[filtro].isChecked()
                            acao.blockSignals(True)
                            acao.setChecked(esta_marcado)
                            acao.blockSignals(False)

            else:
                for acao in main_window.findChildren(QAction):
                    if hasattr(acao, 'data') and callable(acao.data):
                        filtro = acao.data()
                        if (isinstance(filtro, str) and 
                            filtro in self.parent.checkboxes_operacao):
                            esta_marcado = self.parent.checkboxes_operacao[filtro].isChecked()
                            acao.blockSignals(True)
                            acao.setChecked(esta_marcado)
                            acao.blockSignals(False)

    except Exception as e:
        logger.error(f"Erro ao sincronizar menu principal com filtros: {e}", exc_info=True)
