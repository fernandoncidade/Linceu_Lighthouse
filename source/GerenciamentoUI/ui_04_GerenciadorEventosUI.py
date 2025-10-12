from utils.LogManager import LogManager
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_01_alternar_filtro import alternar_filtro
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_02_alternar_visibilidade_coluna import alternar_visibilidade_coluna
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_03_resetar_colunas import resetar_colunas
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_04_resetar_cores import resetar_cores
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_05_redefinir_todas_colunas_cores import redefinir_todas_colunas_cores
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_06_alterar_idioma import alterar_idioma
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_07_confirmar_mudanca_idioma import _confirmar_mudanca_idioma
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_08_limpar_dados_monitorados import _limpar_dados_monitorados
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_09_limpar_dados_interface import _limpar_dados_interface
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_10_reiniciar_aplicativo import _reiniciar_aplicativo
from source.GerenciamentoUI.GerenciamentoEventosUI.geve_11_atualizar_interface import atualizar_interface
logger = LogManager.get_logger()


class GerenciadorEventosUI:
    def __init__(self, interface_principal):
        try:
            self.interface = interface_principal
            self.loc = interface_principal.loc

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorEventosUI: {e}", exc_info=True)

    alternar_filtro = alternar_filtro
    alternar_visibilidade_coluna = alternar_visibilidade_coluna
    resetar_colunas = resetar_colunas
    resetar_cores = resetar_cores
    redefinir_todas_colunas_cores = redefinir_todas_colunas_cores
    alterar_idioma = alterar_idioma
    confirmar_mudanca_idioma = _confirmar_mudanca_idioma
    limpar_dados_monitorados = _limpar_dados_monitorados
    limpar_dados_interface = _limpar_dados_interface
    reiniciar_aplicativo = _reiniciar_aplicativo
    atualizar_interface = atualizar_interface
