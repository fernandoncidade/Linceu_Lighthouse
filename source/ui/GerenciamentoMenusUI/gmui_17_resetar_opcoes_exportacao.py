from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _resetar_opcoes_exportacao(self):
    try:
        self.acao_exportar_colunas_ativas.setChecked(False)
        self.acao_exportar_filtros_ativos.setChecked(False)
        self.acao_exportar_selecao.setChecked(False)
        mensagem_sucesso = self.loc.get_text("export_options_reset_success")
        QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem_sucesso)

    except Exception as e:
        logger.error(f"Erro ao restaurar opções de exportação: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
