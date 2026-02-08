import os
import locale
from PySide6.QtCore import QObject, Signal, QTranslator
from utils.LogManager import LogManager
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_01_inicializar_tradutor_metadados import _inicializar_tradutor_metadados
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_02_criar_mapa_compatibilidade import _criar_mapa_compatibilidade
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_03_carregar_tradutor import carregar_tradutor
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_04_set_idioma import set_idioma
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_05_get_text import get_text
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_06_get_fallback_text import _get_fallback_text
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_07_tr import tr
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_08_salvar_preferencia_idioma import salvar_preferencia_idioma
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_09_carregar_preferencia_idioma import carregar_preferencia_idioma
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_10_get_idiomas_disponiveis import get_idiomas_disponiveis
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_11_traduzir_tipo_operacao import traduzir_tipo_operacao
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_12_traduzir_metadados import traduzir_metadados
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_13_traduzir_tipo_operacao_fallback import _traduzir_tipo_operacao_fallback
from source.GerenciamentoUI.GerenciamentoLocalizadorQt.glqt_14_criar_arquivos_traducao import criar_arquivos_traducao
logger = LogManager.get_logger()


class LocalizadorQt(QObject):
    idioma_alterado = Signal(str)
    traducoes_carregadas = Signal(str)

    def __init__(self):
        super().__init__()
        try:
            self.idiomas_suportados = {
                "pt_BR": "Português Brasileiro",
                "en_US": "English (US)", 
                "es_ES": "Español",
                "fr_FR": "Français",
                "it_IT": "Italiano",
                "de_DE": "Deutsch"
            }

            self.system_locale = locale.getdefaultlocale()[0]
            self.idioma_atual = self.carregar_preferencia_idioma()
            self.translator = QTranslator()
            self.qt_translator = QTranslator()
            self.translations_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "locale")
            self.traducoes = self._criar_mapa_compatibilidade()
            self._inicializar_tradutor_metadados()
            self.carregar_tradutor(self.idioma_atual)

        except Exception as e:
            logger.error(f"Erro ao inicializar LocalizadorQt: {e}", exc_info=True)

    _inicializar_tradutor_metadados = _inicializar_tradutor_metadados
    _criar_mapa_compatibilidade = _criar_mapa_compatibilidade
    carregar_tradutor = carregar_tradutor
    set_idioma = set_idioma
    get_text = get_text
    _get_fallback_text = _get_fallback_text
    tr = tr
    salvar_preferencia_idioma = salvar_preferencia_idioma
    carregar_preferencia_idioma = carregar_preferencia_idioma
    get_idiomas_disponiveis = get_idiomas_disponiveis
    traduzir_tipo_operacao = traduzir_tipo_operacao
    traduzir_metadados = traduzir_metadados
    _traduzir_tipo_operacao_fallback = _traduzir_tipo_operacao_fallback
    criar_arquivos_traducao = criar_arquivos_traducao
