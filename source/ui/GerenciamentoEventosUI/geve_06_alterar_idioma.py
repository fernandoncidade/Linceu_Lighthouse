from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def alterar_idioma(self):
    try:
        acao = self.interface.sender()
        if acao and isinstance(acao, QAction):
            novo_idioma = acao.data()
            if novo_idioma != self.loc.idioma_atual:
                resposta = self._confirmar_mudanca_idioma()
                if resposta == QMessageBox.Yes:
                    idioma_anterior = self.loc.idioma_atual
                    self.loc.set_idioma(novo_idioma)
                    self.interface.atualizar_interface()
                    if hasattr(self.interface, 'gerenciador_tabela') and hasattr(self.interface, 'tabela_dados'):
                        self.interface.gerenciador_tabela.atualizar_dados_tabela(self.interface.tabela_dados)

                    from PySide6.QtWidgets import QApplication, QDialog
                    for widget in QApplication.topLevelWidgets():
                        if isinstance(widget, QDialog) and widget.windowTitle() == self.loc.get_text("statistics"):
                            if hasattr(self.interface, 'gerenciador_estatisticas_ui'):
                                self.interface.gerenciador_estatisticas_ui._atualizar_graficos(widget)

                    QMessageBox.information(self.interface, self.loc.get_text("success"), self.loc.get_text("language_changed_success"))

                else:
                    for acao in self.interface.findChildren(QAction):
                        if hasattr(acao, 'data') and callable(acao.data) and acao.data() == self.loc.idioma_atual:
                            acao.setChecked(True)

    except Exception as e:
        logger.error(f"Erro ao alterar idioma: {e}", exc_info=True)
        QMessageBox.warning(self.interface, self.loc.get_text("error"), self.loc.get_text("language_change_error").format(str(e)))
