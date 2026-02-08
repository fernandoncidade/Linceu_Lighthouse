from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def stop(self):
    try:
        if self.timer.isActive():
            self.timer.stop()

        for dlg in self.detached_dialogs:
            try:
                if dlg and dlg.isVisible():
                    dlg.close()

            except Exception:
                pass

        try:
            if self._monitor_tema:
                self._monitor_tema.parar_monitoramento()

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao parar GerenciadorDesempenho: {e}", exc_info=True)
