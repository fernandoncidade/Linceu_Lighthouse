import os
import json
import locale
from PySide6.QtCore import QObject, Signal, QCoreApplication, QTranslator, QLocale
from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
from utils.CaminhoPersistenteUtils import obter_caminho_persistente


class LocalizadorQt(QObject):
    idioma_alterado = Signal(str)
    traducoes_carregadas = Signal(str)

    def __init__(self):
        super().__init__()
        self.logger = LogManager.get_logger()
        self.logger.debug("Inicializando LocalizadorQt")
        self.idiomas_suportados = {
            "pt_BR": "Português Brasileiro",
            "en_US": "English (US)", 
            "es_ES": "Español",
            "fr_FR": "Français",
            "it_IT": "Italiano",
            "de_DE": "Deutsch"
        }

        self.system_locale = locale.getdefaultlocale()[0]
        self.logger.debug(f"Locale do sistema detectado: {self.system_locale}")
        self.idioma_atual = self.carregar_preferencia_idioma()
        self.translator = QTranslator()
        self.qt_translator = QTranslator()
        self.translations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations")
        self.traducoes = self._criar_mapa_compatibilidade()
        self._inicializar_tradutor_metadados()
        self.carregar_tradutor(self.idioma_atual)
        self.logger.info(f"LocalizadorQt inicializado com idioma: {self.idioma_atual}")

    def _inicializar_tradutor_metadados(self):
        try:
            from GerenciamentoUI.ui_13_TradutorMetadadosQt import TradutorMetadadosQt
            self.tradutor_metadados = TradutorMetadadosQt(self)
            self.logger.debug("Tradutor de metadados inicializado com sucesso")

        except ImportError as e:
            self.logger.error(f"Erro ao importar TradutorMetadadosQt: {e}")
            self.tradutor_metadados = None

    def _criar_mapa_compatibilidade(self):
        return {
            idioma: {
                "select_all_columns": "select_all_columns",
                "deselect_all_columns": "deselect_all_columns",
            }
            for idioma in self.idiomas_suportados.keys()
        }

    def carregar_tradutor(self, idioma: str):
        try:
            app = QApplication.instance()
            if not app:
                self.logger.error("QApplication não está disponível")
                return False

            app.removeTranslator(self.translator)
            app.removeTranslator(self.qt_translator)
            translation_file = os.path.join(self.translations_dir, f"linceu_{idioma}.qm")
            if os.path.exists(translation_file):
                success = self.translator.load(translation_file)
                if success:
                    app.installTranslator(self.translator)
                    self.logger.info(f"Tradutor da aplicação carregado para {idioma}")

                else:
                    self.logger.warning(f"Falha ao carregar tradutor da aplicação para {idioma}")

            else:
                self.logger.warning(f"Arquivo de tradução não encontrado: {translation_file}")
                os.makedirs(self.translations_dir, exist_ok=True)

            qt_locale = QLocale(idioma)
            QLocale.setDefault(qt_locale)
            self.logger.info(f"QLocale padrão definido para: {qt_locale.name()}")
            qt_translations_path = os.path.join(self.translations_dir, "qt")
            if os.path.exists(qt_translations_path):
                qt_success = self.qt_translator.load(qt_locale, "qtbase", "_", qt_translations_path)
                if qt_success:
                    app.installTranslator(self.qt_translator)
                    self.logger.info(f"Tradutor do Qt carregado para {idioma}")

            return True

        except Exception as e:
            self.logger.error(f"Erro ao carregar tradutor para {idioma}: {e}", exc_info=True)
            return False

    def set_idioma(self, idioma: str):
        if idioma not in self.idiomas_suportados:
            self.logger.warning(f"Idioma não suportado: {idioma}")
            return

        if idioma == self.idioma_atual:
            self.logger.debug(f"Idioma já está definido como {idioma}")
            return

        self.logger.info(f"Alterando idioma de '{self.idioma_atual}' para '{idioma}'")
        if hasattr(self, 'tradutor_metadados') and self.tradutor_metadados:
            self.tradutor_metadados._cache_traducoes_tipo_operacao.clear()
            self.tradutor_metadados._cache_traducoes_atributos.clear()
            self.tradutor_metadados._cache_traducoes_protegido.clear()
            self.logger.debug("Caches de traduções limpos")

        if self.carregar_tradutor(idioma):
            self.idioma_atual = idioma
            self.salvar_preferencia_idioma(idioma)
            self.idioma_alterado.emit(idioma)
            self.traducoes_carregadas.emit(idioma)
            QApplication.processEvents()

    def get_text(self, key: str, *args) -> str:
        try:
            texto = QCoreApplication.translate("LinceuLighthouse", key)
            if texto == key:
                self.logger.warning(f"Tradução não encontrada para chave: '{key}'")
                return self._get_fallback_text(key)

            if args:
                for i, arg in enumerate(args, 1):
                    texto = texto.replace(f"%{i}", str(arg))

            return texto

        except Exception as e:
            self.logger.error(f"Erro ao obter tradução para '{key}': {e}", exc_info=True)
            return key

    def _get_fallback_text(self, key: str) -> str:
        fallbacks = {
            "select_all_columns": "Select All Columns",
            "deselect_all_columns": "Deselect All Columns",
            "readonly": "Read Only",
            "hidden": "Hidden",
            "system": "System",
            "archive": "Archive",
            "encrypted": "Encrypted",
            "compressed": "Compressed",
            "yes": "Yes",
            "no": "No",
            "op_moved": "Moved",
            "op_renamed": "Renamed",
            "op_added": "Added",
            "op_deleted": "Deleted",
            "op_modified": "Modified",
            "op_scanned": "Scanned",
            "basic_colors": "Basic Colors",
            "custom_colors": "Custom Colors",
            "pick_screen_color": "Pick Screen Color",
            "add_to_custom_colors": "Add to Custom Colors",
            "hue": "Hue",
            "sat": "Saturation",
            "val": "Value",
            "red": "Red",
            "green": "Green",
            "blue": "Blue",
            "html": "HTML",
            "ok": "OK",
            "cancel": "Cancel",
            "advanced_filters": "Advanced Filters",
            "advanced_color_picker": "Advanced Color Picker",
            "select_color": "Select Color",
            "current": "Current",
            "new": "New",
            "basics": "Basic",
            "pastels": "Pastels",
            "vibrant": "Vibrant",
            "colors_applied_success": "Colors applied to all columns successfully!",
            "reset_column_color_confirm": "Do you want to restore column colors to default values?",
            "column_colors_reset_success": "Column colors restored successfully!",
            "reset_colors_confirm": "Do you want to restore all colors to default values?",
            "colors_reset_success": "Colors restored successfully!",
            "translating_table": "Aguarde, tradução em andamento...",
            "translation_complete": "Tradução concluída!",
            "language_change_performance_warning":
                "Warning: Changing the language will reload translations across the entire UI and may temporarily impact performance until completion. "
                "If monitoring is running, this operation can cause missed events or temporary freezes. It is strongly recommended to change the language "
                "before starting monitoring. Do you want to proceed?"
        }
        return fallbacks.get(key, key)

    def tr(self, text: str, *args) -> str:
        return self.get_text(text, *args)

    def salvar_preferencia_idioma(self, idioma: str):
        try:
            config_path = os.path.join(obter_caminho_persistente(), "language_config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({"idioma": idioma}, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Preferência de idioma salva: {idioma}")

        except Exception as e:
            self.logger.error(f"Erro ao salvar preferência de idioma: {e}", exc_info=True)

    def carregar_preferencia_idioma(self):
        try:
            config_path = os.path.join(obter_caminho_persistente(), "language_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    idioma = config.get("idioma", self.system_locale)

                    if idioma not in self.idiomas_suportados:
                        idioma = "pt_BR"

                    self.logger.info(f"Preferência de idioma carregada: {idioma}")
                    return idioma

            else:
                idioma = "pt_BR" if self.system_locale not in self.idiomas_suportados else self.system_locale
                self.salvar_preferencia_idioma(idioma)
                return idioma

        except Exception as e:
            self.logger.error(f"Erro ao carregar preferência de idioma: {e}", exc_info=True)
            return "pt_BR"

    def get_idiomas_disponiveis(self):
        self.logger.debug(f"Obtendo lista de idiomas para o idioma atual: {self.idioma_atual}")
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
            return self.idiomas_suportados.copy()

    def traduzir_tipo_operacao(self, valor, idioma_origem=None):
        if self.tradutor_metadados:
            return self.tradutor_metadados.traduzir_tipo_operacao(valor, idioma_origem)

        else:
            return self._traduzir_tipo_operacao_fallback(valor)

    def traduzir_metadados(self, valor, campo):
        if self.tradutor_metadados:
            return self.tradutor_metadados.traduzir_metadados(valor, campo)

        else:
            return valor

    def _traduzir_tipo_operacao_fallback(self, valor):
        mapeamento = {
            "moved": "op_moved",
            "renamed": "op_renamed", 
            "added": "op_added",
            "deleted": "op_deleted",
            "modified": "op_modified",
            "scanned": "op_scanned",
            "movido": "op_moved",
            "renomeado": "op_renamed",
            "adicionado": "op_added", 
            "excluído": "op_deleted",
            "modificado": "op_modified",
            "escaneado": "op_scanned"
        }

        valor_lower = str(valor).lower().strip()
        chave = mapeamento.get(valor_lower, valor_lower)
        if chave.startswith("op_"):
            return self.get_text(chave)

        return valor

    def criar_arquivos_traducao(self):
        try:
            os.makedirs(self.translations_dir, exist_ok=True)

            pro_content = f"""
SOURCES += ../InterfaceCore/*.py \\
          ../GerenciamentoUI/*.py \\
          ../Filtros/*.py \\
          ../Observador/*.py

TRANSLATIONS += {' '.join([f'linceu_{idioma}.ts' for idioma in self.idiomas_suportados.keys()])}

CODECFORTR = UTF-8
"""

            pro_file = os.path.join(self.translations_dir, "linceu.pro")
            with open(pro_file, 'w', encoding='utf-8') as f:
                f.write(pro_content)

            self.logger.info(f"Arquivo .pro criado em: {pro_file}")
            self.logger.info("Execute 'lupdate linceu.pro' no diretório translations para extrair strings")

        except Exception as e:
            self.logger.error(f"Erro ao criar arquivos de tradução: {e}", exc_info=True)
