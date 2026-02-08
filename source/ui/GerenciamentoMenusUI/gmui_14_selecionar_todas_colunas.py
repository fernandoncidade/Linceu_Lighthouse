from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def selecionar_todas_colunas(self):
    try:
        for key, acao in self.acoes_colunas.items():
            acao.setChecked(True)

        for key in self.acoes_colunas.keys():
            self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[key]["visivel"] = True

        self.interface.gerenciador_colunas.salvar_configuracoes()
        if hasattr(self.interface.gerenciador_tabela, 'atualizar_visibilidade_colunas'):
            self.interface.gerenciador_tabela.atualizar_visibilidade_colunas(atualizar_em_massa=True)

        else:
            self.interface.atualizar_visibilidade_colunas()

        msg_box = QMessageBox(self.interface)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(self.loc.get_text("success"))
        msg_box.setText(self.loc.get_text("columns_select_success"))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    except Exception as e:
        logger.error(f"Erro ao selecionar todas as colunas: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
