from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def limpar_estado(self):
    try:
        self.eventos_pendentes.clear()
        self.registros_anteriores.clear()
        self.eventos_ignorados.clear()
        self.arquivos_recem_adicionados.clear()
        self.arquivos_recem_excluidos.clear()
        self.ultima_modificacao.clear()

    except Exception as e:
        logger.error(f"Erro ao limpar estado: {e}", exc_info=True)
