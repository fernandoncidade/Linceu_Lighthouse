from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QDialog
from source.Filtros.fil_01_Filtros import Filtros
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def alternar_filtro(self):
    try:
        acao = self.interface.sender()
        if acao and isinstance(acao, QAction):
            filtro = acao.data()
            esta_marcado = acao.isChecked()
            if (hasattr(self.interface, 'painel_filtros') and 
                hasattr(self.interface.painel_filtros, 'checkboxes_operacao') and
                filtro in self.interface.painel_filtros.checkboxes_operacao):
                checkbox = self.interface.painel_filtros.checkboxes_operacao[filtro]
                checkbox.blockSignals(True)
                checkbox.setChecked(esta_marcado)
                checkbox.blockSignals(False)

            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QDialog) and hasattr(widget, 'findChild'):
                    for painel_filtro in widget.findChildren(Filtros):
                        if (hasattr(painel_filtro, 'checkboxes_operacao') and 
                            filtro in painel_filtro.checkboxes_operacao):
                            painel_filtro.checkboxes_operacao[filtro].blockSignals(True)
                            painel_filtro.checkboxes_operacao[filtro].setChecked(esta_marcado)
                            painel_filtro.checkboxes_operacao[filtro].blockSignals(False)
                            painel_filtro.administrador_filtros.aplicar_filtros()

            chave_para_operacao = {
                "op_moved": self.loc.get_text("op_moved"),
                "op_renamed": self.loc.get_text("op_renamed"),
                "op_added": self.loc.get_text("op_added"),
                "op_deleted": self.loc.get_text("op_deleted"),
                "op_modified": self.loc.get_text("op_modified"),
                "op_scanned": self.loc.get_text("op_scanned")
            }
            for row in range(self.interface.tabela_dados.rowCount()):
                tipo_op_cell = self.interface.tabela_dados.item(row, 0)
                if tipo_op_cell:
                    tipo_op_texto = tipo_op_cell.text()
                    if tipo_op_texto == chave_para_operacao.get(filtro):
                        self.interface.tabela_dados.setRowHidden(row, not esta_marcado)

            self.interface.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao alternar filtro: {e}", exc_info=True)
