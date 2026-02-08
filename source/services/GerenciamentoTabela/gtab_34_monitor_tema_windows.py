import winreg
from PySide6.QtCore import QObject, Signal, QTimer
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class MonitorTemaWindows(QObject):
    tema_alterado = Signal(str)

    def __init__(self):
        super().__init__()
        self._tema_atual = self._detectar_tema_atual()
        self._monitorando = False
        self._thread_monitor = None
        self._timer_verificacao = QTimer()
        self._timer_verificacao.timeout.connect(self._verificar_mudanca_tema)

    def _detectar_tema_atual(self):
        try:
            chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            valor, _ = winreg.QueryValueEx(chave, "AppsUseLightTheme")
            winreg.CloseKey(chave)
            return "claro" if valor == 1 else "escuro"

        except Exception:
            logger.error("Erro ao detectar tema do Windows", exc_info=True)
            return "claro"

    def iniciar_monitoramento(self):
        try:
            if not self._monitorando:
                self._monitorando = True
                self._timer_verificacao.start(1000)

        except Exception as e:
            logger.error(f"Erro ao iniciar monitoramento de tema: {e}", exc_info=True)

    def parar_monitoramento(self):
        try:
            if self._monitorando:
                self._monitorando = False
                self._timer_verificacao.stop()

        except Exception as e:
            logger.error(f"Erro ao parar monitoramento de tema: {e}", exc_info=True)

    def _verificar_mudanca_tema(self):
        try:
            tema_atual = self._detectar_tema_atual()
            if tema_atual != self._tema_atual:
                logger.info(f"Mudança de tema detectada: {self._tema_atual} -> {tema_atual}")
                self._tema_atual = tema_atual
                self.tema_alterado.emit(tema_atual)

        except Exception as e:
            logger.error(f"Erro ao verificar mudança de tema: {e}", exc_info=True)

    def obter_tema_atual(self):
        try:
            return self._tema_atual

        except Exception as e:
            logger.error(f"Erro ao obter tema atual: {e}", exc_info=True)
