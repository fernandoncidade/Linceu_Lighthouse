from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class GerenciadorLimpeza:
    def __init__(self, interface_principal):
        self.interface = interface_principal
        
    def limpar_dados(self):
        try:
            msg_box = QMessageBox(self.interface)
            msg_box.setWindowTitle(self.interface.loc.get_text("confirm"))
            msg_box.setText(self.interface.loc.get_text("clear_confirm"))
            msg_box.setIcon(QMessageBox.Question)
            botao_sim = msg_box.addButton(self.interface.loc.get_text("yes"), QMessageBox.YesRole)
            botao_nao = msg_box.addButton(self.interface.loc.get_text("no"), QMessageBox.NoRole)
            msg_box.setDefaultButton(botao_nao)
            msg_box.exec()
            if msg_box.clickedButton() != botao_sim:
                return

            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                if hasattr(self.interface, 'observador') and self.interface.observador and self.interface.observador.ativo:
                    self.interface.gerenciador_botoes.alternar_analise_diretorio()

                self.interface.evento_base.limpar_registros()
                self.interface.tabela_dados.clearContents()
                self.interface.tabela_dados.setRowCount(0)
                self.interface.tabela_dados.viewport().update()
                self.interface.ultimo_salvamento = None
                if hasattr(self.interface.painel_filtros, 'administrador_filtros'):
                    self.interface.painel_filtros.administrador_filtros.limpar_filtros()

                else:
                    logger.warning("Não foi possível acessar o administrador de filtros")

                self.interface.atualizar_status()
                if (hasattr(self.interface, 'gerenciador_colunas') and 
                    hasattr(self.interface.gerenciador_colunas, 'cache_metadados')):
                    self.interface.gerenciador_colunas.cache_metadados.clear()

                self.interface.rotulo_resultado.setText(self.interface.loc.get_text("data_cleared"))
                self.interface.rotulo_contador_eventos.setText(f"{self.interface.loc.get_text('events_monitored')}: 0")
                if hasattr(self.interface, 'barra_progresso'):
                    self.interface.barra_progresso.hide()
                    self.interface.barra_progresso.setValue(0)

                self.interface.rotulo_resultado.setText(self.interface.loc.get_text("data_cleared"))
                QApplication.restoreOverrideCursor()
                QMessageBox.information(
                    self.interface, 
                    self.interface.loc.get_text("success"), 
                    self.interface.loc.get_text("clear_success")
                )

            finally:
                if QApplication.overrideCursor():
                    QApplication.restoreOverrideCursor()

                QApplication.processEvents()

        except Exception as e:
            if QApplication.overrideCursor():
                QApplication.restoreOverrideCursor()

            logger.error(f"Erro ao limpar dados: {e}", exc_info=True)
            QMessageBox.critical(
                self.interface, 
                self.interface.loc.get_text("error"), 
                self.interface.loc.get_text("clear_error").format(str(e))
            )
