from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_tipo_operacao_fallback(self, valor):
    try:
        mapeamento = {
            "moved": "op_moved",
            "renamed": "op_renamed", 
            "added": "op_added",
            "deleted": "op_deleted",
            "modified": "op_modified",
            "scanned": "op_scanned",
            "movido": "op_moved",
            "renomeado": "op_renamed",
            "adicionado": "op_added", 
            "excluído": "op_deleted",
            "modificado": "op_modified",
            "escaneado": "op_scanned"
        }

        valor_lower = str(valor).lower().strip()
        chave = mapeamento.get(valor_lower, valor_lower)
        if chave.startswith("op_"):
            return self.get_text(chave)

        return valor

    except Exception as e:
        logger.error(f"Erro ao traduzir tipo de operação (fallback): {e}", exc_info=True)
