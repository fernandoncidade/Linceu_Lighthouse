from source.utils.LogManager import LogManager
from source.ui.GerenciamentoBotoes.geb_01_selecionar_diretorio import selecionar_diretorio
from source.ui.GerenciamentoBotoes.geb_02_alternar_analise_diretorio import alternar_analise_diretorio
from source.ui.GerenciamentoBotoes.geb_03_exportar_dados import exportar_dados
from source.ui.GerenciamentoBotoes.geb_04_exportar_para_sqlite import _exportar_para_sqlite
from source.ui.GerenciamentoBotoes.geb_05_limpar_dados import limpar_dados
from source.ui.GerenciamentoBotoes.geb_06_pausar_monitoramento_ou_escaneamento import pausar_monitoramento_ou_escaneamento
logger = LogManager.get_logger()


class GerenciadorBotoes:
    def __init__(self, interface, loc):
        try:
            self.interface = interface
            self.loc = loc

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorBotoes: {e}", exc_info=True)
    
    selecionar_diretorio = selecionar_diretorio
    alternar_analise_diretorio = alternar_analise_diretorio
    exportar_dados = exportar_dados
    _exportar_para_sqlite = _exportar_para_sqlite
    limpar_dados = limpar_dados
    pausar_monitoramento_ou_escaneamento = pausar_monitoramento_ou_escaneamento
