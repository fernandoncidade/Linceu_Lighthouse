from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def redefinir_todas_colunas_cores(self, gerenciador_cores, acao_exportar_colunas_ativas, acao_exportar_filtros_ativos, acao_exportar_selecao, criar_menu_principal, gerenciador_tabela):
    try:
        mensagem = self.loc.get_text("reset_column_color_confirm")
        resposta = QMessageBox.question(self.interface, self.loc.get_text("confirm"), mensagem, QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            exportar_colunas_ativas = acao_exportar_colunas_ativas.isChecked()
            exportar_filtros_ativos = acao_exportar_filtros_ativos.isChecked()
            exportar_selecao = acao_exportar_selecao.isChecked()
            gerenciador_tabela.colunas_para_colorir.clear()
            gerenciador_tabela.colunas_para_colorir.add("tipo_operacao")
            gerenciador_tabela.salvar_configuracoes_cores()
            gerenciador_tabela.redefinir_cores_todas_colunas()
            criar_menu_principal()
            acao_exportar_colunas_ativas.setChecked(exportar_colunas_ativas)
            acao_exportar_filtros_ativos.setChecked(exportar_filtros_ativos)
            acao_exportar_selecao.setChecked(exportar_selecao)
            mensagem_sucesso = self.loc.get_text("column_colors_reset_success")
            QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem_sucesso)

    except Exception as e:
        logger.error(f"Erro ao redefinir cores das colunas: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
