from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_traducoes(self):
    try:
        if self.tipo_operacao:
            titulo = f"{self.loc.get_text('select_color_for')} {self.loc.get_text(self.tipo_operacao)}"

        else:
            titulo = self.loc.get_text('select_color')

        self.setWindowTitle(titulo)

        try:
            self.label_atual.setText(f"{self.loc.get_text('current')}:")
            self.label_novo.setText(f"{self.loc.get_text('new')}:")

        except Exception:
            pass

        try:
            self.tab_widget.setTabText(0, self.loc.get_text("basics"))
            self.tab_widget.setTabText(1, self.loc.get_text("pastels"))
            self.tab_widget.setTabText(2, self.loc.get_text("vibrant"))

        except Exception:
            pass

        try:
            self.btn_avancado.setText(self.loc.get_text("advanced_color_picker"))
            self.btn_ok.setText(self.loc.get_text("ok"))
            self.btn_cancelar.setText(self.loc.get_text("cancel"))

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao atualizar traduções do diálogo de cores: {e}", exc_info=True)
