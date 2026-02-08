import os
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def carregar_tradutor(self, idioma: str):
    try:
        app = QApplication.instance()
        if not app:
            logger.error("QApplication não está disponível")
            return False

        app.removeTranslator(self.translator)
        app.removeTranslator(self.qt_translator)
        translation_file = os.path.join(self.translations_dir, f"linceu_{idioma}.qm")
        if os.path.exists(translation_file):
            success = self.translator.load(translation_file)
            if success:
                app.installTranslator(self.translator)

            else:
                logger.warning(f"Falha ao carregar tradutor da aplicação para {idioma}")

        else:
            logger.warning(f"Arquivo de tradução não encontrado: {translation_file}")
            os.makedirs(self.translations_dir, exist_ok=True)

        qt_locale = QLocale(idioma)
        QLocale.setDefault(qt_locale)
        qt_translations_path = os.path.join(self.translations_dir, "qt")
        if os.path.exists(qt_translations_path):
            qt_success = self.qt_translator.load(qt_locale, "qtbase", "_", qt_translations_path)
            if qt_success:
                app.installTranslator(self.qt_translator)

        return True

    except Exception as e:
        logger.error(f"Erro ao carregar tradutor para {idioma}: {e}", exc_info=True)
        return False
