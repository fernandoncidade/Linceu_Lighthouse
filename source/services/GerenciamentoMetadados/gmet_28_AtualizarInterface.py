from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_interface(gc, idioma: str):
    try:
        for key, coluna in gc.COLUNAS_DISPONIVEIS.items():
            tk = coluna.get("translation_key", key)
            gc.COLUNAS_DISPONIVEIS[key]["nome"] = gc.loc.get_text(tk)

        with gc.lock_cache:
            gc.cache_metadados.clear()

        if hasattr(gc.interface, 'gerenciador_tabela'):
            gc.interface.gerenciador_tabela.atualizar_dados_tabela(gc.interface.tabela_dados)

        else:
            gc.gerenciador_tabela.configurar_tabela(gc.interface.tabela_dados)

    except Exception as e:
        logger.error(f"Erro ao atualizar interface: {e}", exc_info=True)
