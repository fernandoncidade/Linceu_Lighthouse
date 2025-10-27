from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_contagem_apos_idioma(self, idioma=None):
    try:
        if self.parent is None:
            return

        import shiboken6
        if not shiboken6.isValid(self.parent):
            return

        if hasattr(self.parent, 'filtroAplicado'):
            try:
                self.parent.filtroAplicado.emit()

            except RuntimeError as re:
                logger.error(f"Não foi possível emitir sinal filtroAplicado: {re}", exc_info=True)
                self.desconectar_sinais()
                return

        self.notificar_alteracao_idioma()

    except Exception as e:
        logger.error(f"Erro ao atualizar após mudança de idioma: {e}", exc_info=True)
