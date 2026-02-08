from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox
from source.ui.GerenciamentoMenusUI.gmui_02_GerenciadorCores import GerenciadorCores
from source.ui.ui_11_DialogoCores import DialogoPaletaCores
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _abrir_dialogo_cor(self, tipo_operacao):
    try:
        cor_atual = QColor(self.gerenciador_cores.obter_cor_hex(tipo_operacao))
        nome_operacao = self.loc.get_text(tipo_operacao)
        titulo = f"{self.loc.get_text('select_color_for')} {nome_operacao}"
        dialogo = DialogoPaletaCores(cor_atual, self.interface, titulo, None, tipo_operacao=tipo_operacao)
        GerenciadorCores.aplicar_icone_paleta(dialogo, tipo="paleta")
        dialogo.show()
        def on_cor_selecionada(nova_cor):
            if nova_cor.isValid():
                self.gerenciador_cores.definir_cor(tipo_operacao, nova_cor.name())
                self.gerenciador_cores.salvar_cores()
                self.gerenciador_cores.atualizar_cores_no_sistema()
                if hasattr(self.interface, "gerenciador_tabela"):
                    self.interface.gerenciador_tabela.atualizar_cores_colunas(aplicar_em_massa=True)

                exportar_colunas_ativas = self.acao_exportar_colunas_ativas.isChecked()
                exportar_filtros_ativos = self.acao_exportar_filtros_ativos.isChecked()
                exportar_selecao = self.acao_exportar_selecao.isChecked()
                self.criar_menu_principal()
                self.acao_exportar_colunas_ativas.setChecked(exportar_colunas_ativas)
                self.acao_exportar_filtros_ativos.setChecked(exportar_filtros_ativos)
                self.acao_exportar_selecao.setChecked(exportar_selecao)
                mensagem = self.loc.get_text("color_changed_success")
                QMessageBox.information(self.interface, self.loc.get_text("success"), mensagem)
                dialogo.close()

        dialogo.corSelecionada.connect(on_cor_selecionada)

    except Exception as e:
        logger.error(f"Erro ao abrir diálogo de cor: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('error')}: {str(e)}")
