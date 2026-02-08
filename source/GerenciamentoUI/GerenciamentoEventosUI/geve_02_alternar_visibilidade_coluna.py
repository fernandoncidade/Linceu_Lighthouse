from PySide6.QtGui import QAction
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def alternar_visibilidade_coluna(self):
    try:
        acao = self.interface.sender()
        if acao and isinstance(acao, QAction):
            chave_coluna = acao.data()
            if chave_coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS:
                visivel = acao.isChecked()
                self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[chave_coluna]["visivel"] = visivel
                self.interface.gerenciador_colunas.salvar_configuracoes()
                self.interface.atualizar_visibilidade_colunas()

    except Exception as e:
        logger.error(f"Erro ao alternar visibilidade da coluna: {e}", exc_info=True)
