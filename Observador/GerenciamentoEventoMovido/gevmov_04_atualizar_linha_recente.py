from Observador.GerenciamentoEventoMovido.gevmov_05_atualizar_tabela_completa import _atualizar_tabela_completa
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_linha_recente(interfaceMonitor):
    try:
        if hasattr(interfaceMonitor, 'gerenciador_tabela'):
            interfaceMonitor.gerenciador_tabela.atualizar_linha_mais_recente(interfaceMonitor.tabela_dados)
            interfaceMonitor.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao atualizar linha recente: {e}", exc_info=True)
        _atualizar_tabela_completa(interfaceMonitor)
