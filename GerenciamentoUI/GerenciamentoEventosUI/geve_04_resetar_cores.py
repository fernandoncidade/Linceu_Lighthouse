from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def resetar_cores(self, gerenciador_cores, acao_exportar_colunas_ativas, acao_exportar_filtros_ativos, acao_exportar_selecao, criar_menu_principal):
    try:
        cores_padrao = {
            "op_renamed": "#00ff00",
            "op_added": "#0000ff",
            "op_deleted": "#ff0000",
            "op_modified": "#ff6200",
            "op_moved": "#ff00ff",
            "op_scanned": "#808080"
        }

        mensagem = self.loc.get_text("reset_colors_confirm")
        resposta = QMessageBox.question(self.interface, self.loc.get_text("confirm"), mensagem, QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            exportar_colunas_ativas = acao_exportar_colunas_ativas.isChecked()
            exportar_filtros_ativos = acao_exportar_filtros_ativos.isChecked()
            exportar_selecao = acao_exportar_selecao.isChecked()
            for tipo, cor in cores_padrao.items():
                gerenciador_cores.definir_cor(tipo, cor)

            gerenciador_cores.salvar_cores()
            gerenciador_cores.atualizar_cores_no_sistema()
            criar_menu_principal()
            acao_exportar_colunas_ativas.setChecked(exportar_colunas_ativas)
            acao_exportar_filtros_ativos.setChecked(exportar_filtros_ativos)
            acao_exportar_selecao.setChecked(exportar_selecao)
            if hasattr(self.interface, "gerenciador_tabela"):
                self.interface.gerenciador_tabela.atualizar_cores_colunas(aplicar_em_massa=True)

            mensagem_sucesso = self.loc.get_text("colors_reset_success")
            QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem_sucesso)

    except Exception as e:
        logger.error(f"Erro ao restaurar cores padrão: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
