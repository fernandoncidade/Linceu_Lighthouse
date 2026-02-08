from PySide6.QtGui import QAction
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_acao_toggle_desempenho(self, menu_configuracoes):
    try:
        try:
            label = self.loc.get_text("performance_charts")
            if not label or label == "performance_charts":
                label = "Gráficos de desempenho"

        except Exception:
            label = "Gráficos de desempenho"

        acao = getattr(self, "acao_toggle_desempenho", None)

        if acao is None:
            acao = QAction(label, self.interface)
            acao.setCheckable(True)
            acao.triggered.connect(self.interface.alternar_graficos_desempenho)
            self.acao_toggle_desempenho = acao

        else:
            acao.setText(label)

        acao.setChecked(getattr(self.interface, "desempenho_ativo", False))

        try:
            acao.setShortcut("Ctrl+T")

        except Exception:
            pass

        menu_configuracoes.addAction(acao)

    except Exception as e:
        logger.error(f"Erro ao criar ação toggle desempenho: {e}", exc_info=True)
