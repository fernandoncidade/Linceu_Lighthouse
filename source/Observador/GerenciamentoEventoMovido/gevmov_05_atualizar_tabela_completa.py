from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_tabela_completa(interfaceMonitor):
    try:
        if hasattr(interfaceMonitor, 'gerenciador_tabela'):
            sorting_enabled = interfaceMonitor.tabela_dados.isSortingEnabled()
            interfaceMonitor.tabela_dados.setSortingEnabled(False)
            interfaceMonitor.gerenciador_tabela.atualizar_dados_tabela(interfaceMonitor.tabela_dados)
            interfaceMonitor.atualizar_status()
            interfaceMonitor.tabela_dados.setSortingEnabled(sorting_enabled)
            interfaceMonitor.tabela_dados.viewport().update()

    except Exception as e:
        logger.error(f"Erro ao atualizar tabela completa: {e}", exc_info=True)
