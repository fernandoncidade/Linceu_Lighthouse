from PySide6.QtCore import QDateTime
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_filtros(self):
    try:
        for cb in self.parent.checkboxes_operacao.values():
            cb.setChecked(True)

        self.parent.campo_busca.clear()
        self.parent.campo_extensao.clear()
        self.parent.data_inicial.setDateTime(QDateTime.currentDateTime().addDays(-30))
        self.parent.data_final.setDateTime(QDateTime.currentDateTime())

        if hasattr(self.parent, 'ignorar_mover'):
            self.parent.ignorar_mover.setChecked(True)
            self.__class__.filtros_estado["ignorar_mover"] = True

        if hasattr(self.parent, 'ignorar_renomeados'):
            self.parent.ignorar_renomeados.setChecked(True)
            self.__class__.filtros_estado["ignorar_renomeados"] = True

        if hasattr(self.parent, 'ignorar_adicionados'):
            self.parent.ignorar_adicionados.setChecked(True)
            self.__class__.filtros_estado["ignorar_adicionados"] = True

        if hasattr(self.parent, 'ignorar_excluidos'):
            self.parent.ignorar_excluidos.setChecked(True)
            self.__class__.filtros_estado["ignorar_excluidos"] = True

        if hasattr(self.parent, 'ignorar_data_modificados'):
            self.parent.ignorar_data_modificados.setChecked(True)
            self.__class__.filtros_estado["ignorar_data_modificados"] = True

        if hasattr(self.parent, 'ignorar_escaneados'):
            self.parent.ignorar_escaneados.setChecked(True)
            self.__class__.filtros_estado["ignorar_escaneados"] = True

        for row in range(self.parent.tabela_dados.rowCount()):
            self.parent.tabela_dados.setRowHidden(row, False)

        self.sincronizar_menu_principal_com_filtros()
        self.parent.filtroAplicado.emit()

    except Exception as e:
        logger.error(f"Erro ao limpar filtros: {e}", exc_info=True)
