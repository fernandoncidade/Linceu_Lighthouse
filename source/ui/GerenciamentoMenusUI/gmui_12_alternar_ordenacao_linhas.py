from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _alternar_ordenacao_linhas(self):
    try:
        self.interface._ordenacao_linhas_habilitada = self.acao_ordenar_linhas.isChecked()
        if hasattr(self.interface, 'tabela_dados') and self.interface.tabela_dados is not None:
            self.interface.tabela_dados.setSortingEnabled(self.interface._ordenacao_linhas_habilitada)
            estado_texto = self.loc.get_text("enabled") if self.interface._ordenacao_linhas_habilitada else self.loc.get_text("disabled")
            mensagem = f"{self.loc.get_text('sort_rows')} {estado_texto}"
            QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem)

    except Exception as e:
        logger.error(f"Erro ao alternar ordenação de linhas: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
