from PySide6.QtWidgets import QGroupBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_interface(self, idioma=None):
    try:
        grupo_operacao = self.findChild(QGroupBox, "grupo_operacao")
        if grupo_operacao:
            grupo_operacao.setTitle(self.loc.get_text("operation_filter"))
            for op, cb in self.checkboxes_operacao.items():
                cb.setText(self.loc.get_text(op))

        grupo_busca = self.findChild(QGroupBox, "grupo_busca")
        if grupo_busca:
            grupo_busca.setTitle(self.loc.get_text("search"))

        grupo_extensao = self.findChild(QGroupBox, "grupo_extensao")
        if grupo_extensao:
            grupo_extensao.setTitle(self.loc.get_text("extension_filter"))

        grupo_data = self.findChild(QGroupBox)
        if grupo_data and grupo_data.title() == self.loc.get_text("date_filter"):
            grupo_data.setTitle(self.loc.get_text("date_filter"))

        if hasattr(self, 'ignorar_mover'):
            self.ignorar_mover.setText(self.loc.get_text("ignore_move_filter"))

        if hasattr(self, 'ignorar_renomeados'):
            self.ignorar_renomeados.setText(self.loc.get_text("ignore_rename_filter"))

        if hasattr(self, 'ignorar_adicionados'):
            self.ignorar_adicionados.setText(self.loc.get_text("ignore_add_filter"))

        if hasattr(self, 'ignorar_excluidos'):
            self.ignorar_excluidos.setText(self.loc.get_text("ignore_delete_filter"))

        if hasattr(self, 'ignorar_data_modificados'):
            self.ignorar_data_modificados.setText(self.loc.get_text("ignore_modified_filter"))

        if hasattr(self, 'ignorar_escaneados'):
            self.ignorar_escaneados.setText(self.loc.get_text("ignore_scanned_filter"))

    except Exception as e:
        logger.error(f"Erro ao atualizar interface de filtros: {e}", exc_info=True)
