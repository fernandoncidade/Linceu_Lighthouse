from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _confirmar_alteracao_idioma(self, codigo_idioma: str):
    try:
        if not codigo_idioma or codigo_idioma == self.loc.idioma_atual:
            return

        titulo_atual = self.loc.get_text("warning")
        titulo_alvo = self._get_texto_traduzido_para_idioma("warning", codigo_idioma)
        titulo = f"{titulo_atual} / {titulo_alvo}" if titulo_alvo and titulo_alvo != titulo_atual else titulo_atual
        mensagem_atual = self.loc.get_text("language_change_performance_warning")
        mensagem_alvo = self._get_texto_traduzido_para_idioma("language_change_performance_warning", codigo_idioma)
        caixa = QMessageBox(self.interface)
        caixa.setIcon(QMessageBox.Warning)
        caixa.setWindowTitle(titulo)
        caixa.setText(mensagem_atual)
        if mensagem_alvo and mensagem_alvo != mensagem_atual:
            caixa.setInformativeText(mensagem_alvo)

        caixa.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        caixa.setDefaultButton(QMessageBox.No)
        yes_atual = self.loc.get_text("yes") or "Yes"
        yes_alvo = self._get_texto_traduzido_para_idioma("yes", codigo_idioma) or yes_atual
        no_atual = self.loc.get_text("no") or "No"
        no_alvo = self._get_texto_traduzido_para_idioma("no", codigo_idioma) or no_atual
        label_yes = yes_atual if yes_atual.lower() == yes_alvo.lower() else f"{yes_atual}/{yes_alvo}"
        label_no = no_atual if no_atual.lower() == no_alvo.lower() else f"{no_atual}/{no_alvo}"
        btn_yes = caixa.button(QMessageBox.Yes)
        btn_no = caixa.button(QMessageBox.No)
        if btn_yes:
            btn_yes.setText(label_yes)

        if btn_no:
            btn_no.setText(label_no)

        resposta = caixa.exec()
        acao = self._acoes_idioma.get(codigo_idioma)
        if resposta == QMessageBox.Yes:
            if acao is not None:
                acao.setChecked(True)

            self._trocando_idioma = True
            self._aguardando_conclusao_traducao = True
            try:
                if hasattr(self.interface, 'loc') and hasattr(self.interface.loc, 'set_idioma'):
                    self.interface.loc.set_idioma(codigo_idioma)

                self.criar_menu_principal()

            finally:
                self._trocando_idioma = False

        else:
            acao_atual = self._acoes_idioma.get(self.loc.idioma_atual)
            if acao_atual:
                acao_atual.setChecked(True)

            if acao:
                acao.setChecked(False)

    except Exception as e:
        logger.error(f"Erro ao confirmar alteração de idioma: {e}", exc_info=True)
