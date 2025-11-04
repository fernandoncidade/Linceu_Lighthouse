from PySide6.QtWidgets import QWidget
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def alternar_graficos_desempenho(interface, checked=None):
    try:
        from ..ic_09_GerenciadorDesempenho import GerenciadorDesempenho

    except Exception:
        GerenciadorDesempenho = None

    try:
        if checked is None:
            checked = not getattr(interface, "desempenho_ativo", False)

        if checked and not getattr(interface, "desempenho_ativo", False):
            try:
                if GerenciadorDesempenho:
                    interface.gerenciador_desempenho = GerenciadorDesempenho(interface)
                    novo = interface.gerenciador_desempenho.widget

                else:
                    novo = QWidget()

            except Exception:
                novo = QWidget()

            if hasattr(interface, "splitter_lateral"):
                antigo = interface.splitter_lateral.widget(0)
                if antigo:
                    antigo.setParent(None)

                interface.splitter_lateral.insertWidget(0, novo)

            interface.widget_desempenho = novo
            interface.desempenho_ativo = True

        elif not checked and getattr(interface, "desempenho_ativo", False):
            try:
                if getattr(interface, "gerenciador_desempenho", None):
                    interface.gerenciador_desempenho.stop()

            except Exception:
                pass

            interface.gerenciador_desempenho = None
            placeholder = QWidget()
            if hasattr(interface, "splitter_lateral"):
                antigo = interface.splitter_lateral.widget(0)
                if antigo:
                    antigo.setParent(None)

                interface.splitter_lateral.insertWidget(0, placeholder)

            interface.widget_desempenho = placeholder
            interface.desempenho_ativo = False

        if (hasattr(interface, "gerenciador_menus_ui") and
            hasattr(interface.gerenciador_menus_ui, "acao_toggle_desempenho")):
            interface.gerenciador_menus_ui.acao_toggle_desempenho.setChecked(interface.desempenho_ativo)

    except Exception as e:
        logger.error(f"Erro ao alternar gráficos de desempenho: {e}", exc_info=True)

    return getattr(interface, "desempenho_ativo", False)
