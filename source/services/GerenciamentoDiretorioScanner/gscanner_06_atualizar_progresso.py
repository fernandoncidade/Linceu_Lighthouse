from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_progresso(self):
    try:
        if hasattr(self.observador, 'interface'):
            progresso = (self.contador_processados / self.total_arquivos) * 100 if self.total_arquivos > 0 else 0
            if abs(progresso - self.ultimo_progresso) >= 1:
                self.ultimo_progresso = progresso
                self.progresso_atualizado.emit(int(progresso), self.contador_processados, self.total_arquivos)

    except Exception as e:
        logger.error(f"Erro ao atualizar progresso: {e}", exc_info=True)
