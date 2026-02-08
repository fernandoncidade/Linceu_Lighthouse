from utils.LogManager import LogManager
logger = LogManager.get_logger()

def verificar_filtro_operacao(self, tipo_operacao_traduzido):
    try:
        operacao_para_checkbox = {
            self.parent.loc.get_text("op_moved"): "op_moved",
            self.parent.loc.get_text("op_renamed"): "op_renamed",
            self.parent.loc.get_text("op_added"): "op_added",
            self.parent.loc.get_text("op_deleted"): "op_deleted",
            self.parent.loc.get_text("op_modified"): "op_modified",
            self.parent.loc.get_text("op_scanned"): "op_scanned"
        }

        checkbox_key = operacao_para_checkbox.get(tipo_operacao_traduzido)
        resultado = not checkbox_key or self.parent.checkboxes_operacao[checkbox_key].isChecked()
        return resultado

    except Exception as e:
        logger.error(f"Erro ao verificar filtro de operação '{tipo_operacao_traduzido}': {e}", exc_info=True)
        return True
