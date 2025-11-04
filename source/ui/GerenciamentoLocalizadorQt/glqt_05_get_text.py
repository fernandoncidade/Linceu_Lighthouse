from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(self, key: str, *args) -> str:
    try:
        candidates = [key, key.lower(), key.upper(), key.capitalize()]
        seen = set()
        result = None

        for cand in candidates:
            if cand in seen:
                continue

            seen.add(cand)

            texto = QCoreApplication.translate("LinceuLighthouse", cand)
            if texto:
                if texto != cand or cand == key:
                    result = texto
                    break

            try:
                fallback = self._get_fallback_text(cand)

            except Exception:
                fallback = cand

            if fallback != cand:
                result = fallback
                break

        if result is None:
            logger.warning(f"Tradução não encontrada para chave: '{key}'")
            result = key

        if args:
            for i, arg in enumerate(args, 1):
                result = result.replace(f"%{i}", str(arg))

        return result

    except Exception as e:
        logger.error(f"Erro ao obter tradução para '{key}': {e}", exc_info=True)
        return key
