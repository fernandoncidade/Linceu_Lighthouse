import os
import json
import locale
import concurrent.futures
from PySide6.QtCore import QObject, Signal
from utils.LogManager import LogManager
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from GerenciamentoUI.Localizacoes import todas_traducoes
from GerenciamentoUI.Localizacoes.tr_07_TradutorMetadados import traduzir_tipo_operacao, traduzir_metadados


class Localizador(QObject):
    idioma_alterado = Signal(str)
    traducoes_carregadas = Signal(dict)

    def __init__(self):
        super().__init__()
        logger = LogManager.get_logger()
        logger.debug("Inicializando Localizador")

        self.system_locale = locale.getdefaultlocale()[0]
        logger.debug(f"Locale do sistema detectado: {self.system_locale}")

        self.idioma_atual = self.carregar_preferencia_idioma()
        logger.info(f"Localizador inicializado com idioma: {self.idioma_atual}")

        self.traducoes = todas_traducoes
        logger.debug(f"Carregadas traduções para {len(self.traducoes)} idiomas")

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.traducoes_carregadas.connect(self._aplicar_traducoes_na_interface)

    def set_idioma(self, idioma: str):
        logger = LogManager.get_logger()
        if idioma in self.traducoes:
            logger.info(f"Alterando idioma de '{self.idioma_atual}' para '{idioma}'")
            future = self.executor.submit(self._carregar_traducoes_background, idioma)
            future.add_done_callback(lambda f: self.traducoes_carregadas.emit(f.result()))

        else:
            logger.warning(f"Tentativa de definir idioma não suportado: {idioma}")

    def _carregar_traducoes_background(self, idioma):
        import time
        time.sleep(0.1)
        return {"idioma": idioma, "traducoes": self.traducoes.get(idioma, {})}

    def _aplicar_traducoes_na_interface(self, resultado):
        from PySide6.QtWidgets import QApplication
        idioma = resultado["idioma"]
        self.idioma_atual = idioma
        self.salvar_preferencia_idioma(idioma)

        interface = getattr(self, 'interface_principal', None)
        if interface:
            if hasattr(interface, 'tabela_dados'):
                interface.tabela_dados.blockSignals(True)

            if hasattr(interface, 'painel_filtros'):
                interface.painel_filtros.blockSignals(True)

        self.idioma_alterado.emit(idioma)

        if interface:
            if hasattr(interface, 'tabela_dados'):
                interface.tabela_dados.blockSignals(False)
                interface.tabela_dados.viewport().update()

            if hasattr(interface, 'painel_filtros'):
                interface.painel_filtros.blockSignals(False)

        QApplication.processEvents()

    def salvar_preferencia_idioma(self, idioma: str):
        logger = LogManager.get_logger()
        try:
            config_path = os.path.join(obter_caminho_persistente(), "language_config.json")
            with open(config_path, 'w') as f:
                json.dump({"idioma": idioma}, f)

            logger.info(f"Preferência de idioma salva em: {config_path}")

        except Exception as e:
            logger.error(f"Erro ao salvar preferência de idioma: {e}", exc_info=True)

    def carregar_preferencia_idioma(self):
        logger = LogManager.get_logger()
        try:
            config_path = os.path.join(obter_caminho_persistente(), "language_config.json")

            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    idioma = config.get("idioma", self.system_locale)
                    logger.info(f"Preferência de idioma carregada: {idioma}")
                    return idioma

            else:
                with open(config_path, 'w') as f:
                    json.dump({"idioma": self.system_locale}, f)

                logger.info(f"Arquivo de configuração de idioma criado em: {config_path}")
                return self.system_locale

        except Exception as e:
            logger.error(f"Erro ao carregar/criar preferência de idioma: {e}", exc_info=True)
            return self.system_locale

    def verificar_traducoes_ausentes(self):
        logger = LogManager.get_logger()
        logger.debug("Verificando traduções ausentes")

        todas_chaves = set()
        for traducoes in self.traducoes.values():
            todas_chaves.update(traducoes.keys())

        total_ausentes = 0
        for idioma, traducoes in self.traducoes.items():
            ausentes = todas_chaves - set(traducoes.keys())
            if ausentes:
                logger.warning(f"Traduções ausentes para {idioma}: {len(ausentes)} chaves")
                for chave in sorted(ausentes):
                    logger.debug(f"  - Chave ausente em {idioma}: '{chave}'")

                total_ausentes += len(ausentes)

        if total_ausentes == 0:
            logger.info("Todas as traduções estão completas")

        else:
            logger.warning(f"Total de {total_ausentes} traduções ausentes em todos os idiomas")

    def get_text(self, key: str) -> str:
        try:
            texto = self.traducoes.get(self.idioma_atual, {}).get(key, key)
            if texto == key and key not in self.traducoes.get("en_US", {}):
                LogManager.get_logger().warning(f"Chave de tradução não encontrada: '{key}'")

            return texto

        except Exception as e:
            LogManager.get_logger().error(f"Erro ao obter tradução para chave '{key}': {e}", exc_info=True)
            return key

    def get_idiomas_disponiveis(self):
        LogManager.get_logger().debug(f"Obtendo lista de idiomas para o idioma atual: {self.idioma_atual}")

        if self.idioma_atual == "pt_BR":
            return {
                "pt_BR": "Português Brasileiro | Brazilian Portuguese",
                "en_US": "Inglês (EUA) | English (US)",
                "es_ES": "Espanhol | Español",
                "fr_FR": "Francês | Français",
                "it_IT": "Italiano | Italiano",
                "de_DE": "Alemão | Deutsch"
            }

        elif self.idioma_atual == "en_US":
            return {
                "pt_BR": "Brazilian Portuguese | Português Brasileiro",
                "en_US": "English (US) | Inglês (US)",
                "es_ES": "Spanish | Español",
                "fr_FR": "French | Français",
                "it_IT": "Italian | Italiano",
                "de_DE": "German | Deutsch"
            }

        elif self.idioma_atual == "es_ES":
            return {
                "pt_BR": "Portugués Brasileño | Português Brasileiro",
                "en_US": "Inglés (EEUU) | English (US)",
                "es_ES": "Español | Spanish",
                "fr_FR": "Francés | Français",
                "it_IT": "Italiano | Italiano",
                "de_DE": "Alemán | Deutsch"
            }

        elif self.idioma_atual == "fr_FR":
            return {
                "pt_BR": "Portugais Brésilien | Português Brasileiro",
                "en_US": "Anglais (États-Unis) | English (US)",
                "es_ES": "Espagnol | Español",
                "fr_FR": "Français | French",
                "it_IT": "Italien | Italiano",
                "de_DE": "Allemand | Deutsch"
            }

        elif self.idioma_atual == "it_IT":
            return {
                "pt_BR": "Portoghese Brasiliano | Português Brasileiro",
                "en_US": "Inglese (Stati Uniti) | English (US)",
                "es_ES": "Spagnolo | Español",
                "fr_FR": "Francese | Français",
                "it_IT": "Italiano | Italian",
                "de_DE": "Tedesco | Deutsch"
            }

        elif self.idioma_atual == "de_DE":
            return {
                "pt_BR": "Brasilianisches Portugiesisch | Português Brasileiro",
                "en_US": "Englisch (USA) | English (US)",
                "es_ES": "Spanisch | Español",
                "fr_FR": "Französisch | Français",
                "it_IT": "Italienisch | Italiano",
                "de_DE": "Deutsch | German"
            }

        else:
            LogManager.get_logger().warning(f"Idioma não reconhecido para lista de idiomas disponíveis: {self.idioma_atual}")
            return {
                "pt_BR": "Brazilian Portuguese | Português Brasileiro",
                "en_US": "English (US) | Inglês (US)",
                "es_ES": "Spanish | Español",
                "fr_FR": "French | Français",
                "it_IT": "Italian | Italiano",
                "de_DE": "German | Deutsch"
            }

    def traduzir_tipo_operacao(self, valor, idioma_origem=None):
        return traduzir_tipo_operacao(self, valor, idioma_origem)

    def traduzir_metadados(self, valor, campo):
        return traduzir_metadados(self, valor, campo)
