from utils.LogManager import LogManager
logger = LogManager.get_logger()

def salvar_estado_checkboxes(self):
    try:
        if hasattr(self.parent, 'ignorar_mover'):
            self.__class__.filtros_estado["ignorar_mover"] = self.parent.ignorar_mover.isChecked()

        if hasattr(self.parent, 'ignorar_renomeados'):
            self.__class__.filtros_estado["ignorar_renomeados"] = self.parent.ignorar_renomeados.isChecked()

        if hasattr(self.parent, 'ignorar_adicionados'):
            self.__class__.filtros_estado["ignorar_adicionados"] = self.parent.ignorar_adicionados.isChecked()

        if hasattr(self.parent, 'ignorar_excluidos'):
            self.__class__.filtros_estado["ignorar_excluidos"] = self.parent.ignorar_excluidos.isChecked()

        if hasattr(self.parent, 'ignorar_data_modificados'):
            self.__class__.filtros_estado["ignorar_data_modificados"] = self.parent.ignorar_data_modificados.isChecked()

        if hasattr(self.parent, 'ignorar_escaneados'):
            self.__class__.filtros_estado["ignorar_escaneados"] = self.parent.ignorar_escaneados.isChecked()

    except Exception as e:
        logger.error(f"Erro ao salvar estado dos filtros: {e}", exc_info=True)
