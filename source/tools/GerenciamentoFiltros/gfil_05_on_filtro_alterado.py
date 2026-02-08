from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def on_filtro_alterado(self):
    try:
        self.administrador_filtros.aplicar_filtros()
        self.administrador_filtros.sincronizar_menu_principal_com_filtros()

    except Exception as e:
        logger.error(f"Erro ao processar alteração de filtro: {e}", exc_info=True)
