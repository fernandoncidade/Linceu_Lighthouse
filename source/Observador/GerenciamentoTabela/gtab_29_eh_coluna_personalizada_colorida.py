from utils.LogManager import LogManager
logger = LogManager.get_logger()

def eh_coluna_personalizada_colorida(self, key_coluna):
    try:
        if key_coluna is None:
            return False

        if key_coluna == "tipo_operacao":
            return True

        if key_coluna in self.colunas_para_colorir:
            return True

        if hasattr(self.interface, 'gerenciador_colunas'):
            coluna = self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.get(key_coluna)
            if coluna and coluna.get("colorida", False):
                return True

        return False

    except Exception as e:
        logger.error(f"Erro ao verificar se coluna é personalizada colorida: {e}", exc_info=True)
        return False
