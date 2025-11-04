from utils.LogManager import LogManager
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_01_verificar_idioma_cache import _verificar_idioma_cache
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_02_traduzir_tipo_operacao import traduzir_tipo_operacao
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_03_obter_chave_traducao_reversa import _obter_chave_traducao_reversa
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_04_traduzir_metadados import traduzir_metadados
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_05_traduzir_tipo_arquivo import _traduzir_tipo_arquivo
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_06_traduzir_atributos import _traduzir_atributos
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_07_traduzir_autor import _traduzir_autor
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_08_traduzir_protegido import _traduzir_protegido
from GerenciamentoUI.GerenciamentoTradutorMetadadosQt.gtmqt_09_traduzir_dimensoes import _traduzir_dimensoes
logger = LogManager.get_logger()


class TradutorMetadadosQt:
    def __init__(self, localizador):
        try:
            self.loc = localizador
            self._cache_traducoes_tipo_operacao = {}
            self._cache_traducoes_tipo = {}
            self._cache_traducoes_atributos = {}
            self._cache_traducoes_protegido = {}
            self._idioma_cache = self.loc.idioma_atual

        except Exception as e:
            logger.error(f"Erro ao inicializar TradutorMetadadosQt: {e}", exc_info=True)

    _verificar_idioma_cache = _verificar_idioma_cache
    traduzir_tipo_operacao = traduzir_tipo_operacao
    _obter_chave_traducao_reversa = _obter_chave_traducao_reversa
    traduzir_metadados = traduzir_metadados
    _traduzir_tipo_arquivo = _traduzir_tipo_arquivo
    _traduzir_atributos = _traduzir_atributos
    _traduzir_autor = _traduzir_autor
    _traduzir_protegido = _traduzir_protegido
    _traduzir_dimensoes = _traduzir_dimensoes
