import winreg
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def detectar_tema_windows(self):
    try:
        if hasattr(self, '_monitor_tema') and self._monitor_tema:
            return self._monitor_tema.obter_tema_atual()

        chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        valor, _ = winreg.QueryValueEx(chave, "AppsUseLightTheme")
        winreg.CloseKey(chave)
        return "claro" if valor == 1 else "escuro"

    except Exception as e:
        logger.error(f"Erro ao detectar tema do Windows: {e}", exc_info=True)
        return "claro"
