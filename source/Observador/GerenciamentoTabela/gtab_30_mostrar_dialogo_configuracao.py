from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction, QCursor
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def mostrar_dialogo_configuracao(self, pos=None):
    try:
        menu = QMenu()
        menu.setToolTipsVisible(True)
        titulo = QAction(self.loc.get_text("configure_columns"), menu)
        titulo.setEnabled(False)
        menu.addAction(titulo)
        menu.addSeparator()
        acoes = {}
        for key, coluna in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]):
            acao = QAction(coluna["nome"], menu)
            acao.setCheckable(True)
            acao.setChecked(coluna["visivel"])
            acao.setData(key)
            acao.setToolTip(f"Mostrar/ocultar coluna {coluna['nome']}")
            acoes[key] = acao
            menu.addAction(acao)

        acao_cores = QAction("Mostrar cores nas colunas", menu)
        acao_cores.setCheckable(True)
        acao_cores.setChecked(self.cores_visiveis)
        acao_cores.setToolTip("Ativa ou oculta a exibição das cores nas colunas coloridas")
        menu.addAction(acao_cores)
        menu.aboutToShow.connect(lambda: menu.move(QCursor.pos()))
        pos = pos or QCursor.pos()
        resultado = menu.exec(pos)
        if resultado:
            mudancas = False
            for key, acao in acoes.items():
                novo_estado = acao.isChecked()
                if self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[key]["visivel"] != novo_estado:
                    self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[key]["visivel"] = novo_estado
                    mudancas = True

            if acao_cores.isChecked() != self.cores_visiveis:
                if acao_cores.isChecked():
                    self.ativar_cores()

                else:
                    self.ocultar_cores()

            if mudancas:
                self.interface.gerenciador_colunas.salvar_configuracoes()
                self.atualizar_visibilidade_colunas()
                if hasattr(self.interface, 'atualizar_status'):
                    self.interface.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao mostrar diálogo de configuração: {e}", exc_info=True)
        raise
