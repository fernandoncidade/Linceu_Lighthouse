from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _obter_chave_traducao_reversa(self, valor):
    try:
        for chave in ["op_moved", "op_renamed", "op_added", "op_deleted", "op_modified", "op_scanned"]:
            traducao_atual = self.loc.get_text(chave).lower().strip()
            if traducao_atual == valor:
                return chave

        return None

    except Exception as e:
        logger.error(f"Erro ao obter chave de tradução reversa para valor '{valor}': {e}", exc_info=True)
        return None
