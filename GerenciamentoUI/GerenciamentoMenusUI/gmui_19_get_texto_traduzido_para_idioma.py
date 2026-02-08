import os
from PySide6.QtCore import QTranslator
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _get_texto_traduzido_para_idioma(self, chave: str, idioma: str) -> str:
    try:
        translations_dir = getattr(self.loc, "translations_dir", None)
        if not translations_dir:
            return self.loc.get_text(chave)

        qm_path = os.path.join(translations_dir, f"linceu_{idioma}.qm")
        trans = QTranslator(self.interface)
        if trans.load(qm_path):
            txt = trans.translate("LinceuLighthouse", chave)
            if txt:
                return txt

        return self.loc.get_text(chave)

    except Exception as e:
        logger.error(f"Erro ao obter texto traduzido para o idioma {idioma}: {e}", exc_info=True)
        return self.loc.get_text(chave)
