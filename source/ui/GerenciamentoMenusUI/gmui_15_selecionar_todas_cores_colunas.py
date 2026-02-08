from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def selecionar_todas_cores_colunas(self):
    try:
        colunas_disponiveis = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS
        novas_colunas = list(colunas_disponiveis.keys())
        self.interface.gerenciador_tabela.set_colunas_colorir_em_massa(novas_colunas)
        exportar_colunas_ativas = self.acao_exportar_colunas_ativas.isChecked()
        exportar_filtros_ativos = self.acao_exportar_filtros_ativos.isChecked()
        exportar_selecao = self.acao_exportar_selecao.isChecked()
        self.criar_menu_principal()
        self.acao_exportar_colunas_ativas.setChecked(exportar_colunas_ativas)
        self.acao_exportar_filtros_ativos.setChecked(exportar_filtros_ativos)
        self.acao_exportar_selecao.setChecked(exportar_selecao)
        msg_box = QMessageBox(self.interface)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(self.loc.get_text("success"))
        msg_box.setText(self.loc.get_text("colors_applied_success"))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    except Exception as e:
        logger.error(f"Erro ao iniciar coloração de todas as colunas: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
