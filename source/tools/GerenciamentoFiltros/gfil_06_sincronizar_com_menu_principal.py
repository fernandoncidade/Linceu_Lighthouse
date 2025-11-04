from PySide6.QtGui import QAction
from source.tools.fil_03_AdministradorFiltros import AdministradorFiltros
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def sincronizar_com_menu_principal(self):
    try:
        from PySide6.QtWidgets import QApplication
        main_window = None

        parent_widget = self.parent()
        while parent_widget:
            if hasattr(parent_widget, 'gerenciador_menus_ui'):
                main_window = parent_widget
                break

            parent_widget = parent_widget.parent()

        if not main_window:
            for widget in QApplication.topLevelWidgets():
                if hasattr(widget, 'gerenciador_menus_ui'):
                    main_window = widget
                    break

        if not main_window:
            from PySide6.QtWidgets import QMainWindow
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QMainWindow) and widget.menuBar():
                    main_window = widget
                    break

        if main_window:
            menu_bar = main_window.menuBar()
            menu_configuracoes = None
            submenu_filtros = None

            for action in menu_bar.actions():
                if action.text() == self.loc.get_text("settings"):
                    menu_configuracoes = action.menu()
                    break

            if menu_configuracoes:
                for action in menu_configuracoes.actions():
                    if action.text() == self.loc.get_text("filters"):
                        submenu_filtros = action.menu()
                        break

            if submenu_filtros:
                for acao in submenu_filtros.actions():
                    if hasattr(acao, 'data') and callable(acao.data):
                        filtro = acao.data()
                        if isinstance(filtro, str) and filtro in self.checkboxes_operacao:
                            self.checkboxes_operacao[filtro].blockSignals(True)
                            self.checkboxes_operacao[filtro].setChecked(acao.isChecked())
                            self.checkboxes_operacao[filtro].blockSignals(False)

            else:
                for acao in main_window.findChildren(QAction):
                    if hasattr(acao, 'data') and callable(acao.data):
                        filtro = acao.data()
                        if isinstance(filtro, str) and filtro in self.checkboxes_operacao:
                            self.checkboxes_operacao[filtro].blockSignals(True)
                            self.checkboxes_operacao[filtro].setChecked(acao.isChecked())
                            self.checkboxes_operacao[filtro].blockSignals(False)

        else:
            logger.warning("Janela principal não encontrada para sincronização de filtros")

            for op, checkbox in self.checkboxes_operacao.items():
                if op == "op_moved":
                    checkbox.setChecked(not AdministradorFiltros.filtros_estado.get("ignorar_mover", True))

                elif op == "op_renamed":
                    checkbox.setChecked(not AdministradorFiltros.filtros_estado.get("ignorar_renomeados", True))

                elif op == "op_added":
                    checkbox.setChecked(not AdministradorFiltros.filtros_estado.get("ignorar_adicionados", True))

                elif op == "op_deleted":
                    checkbox.setChecked(not AdministradorFiltros.filtros_estado.get("ignorar_excluidos", True))

                elif op == "op_modified":
                    checkbox.setChecked(not AdministradorFiltros.filtros_estado.get("ignorar_data_modificados", True))

                elif op == "op_scanned":
                    checkbox.setChecked(not AdministradorFiltros.filtros_estado.get("ignorar_escaneados", True))

    except Exception as e:
        logger.error(f"Erro ao sincronizar filtros com menu principal: {e}", exc_info=True)
