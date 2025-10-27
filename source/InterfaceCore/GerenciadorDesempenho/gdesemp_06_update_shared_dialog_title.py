from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_shared_dialog_title(self):
    try:
        if not self._shared_dialog:
            return

        if hasattr(self.interface, "loc") and hasattr(self.interface.loc, "carregar_preferencia_idioma"):
            idioma_salvo = self.interface.loc.carregar_preferencia_idioma()
            if hasattr(self.interface.loc, "set_idioma"):
                self.interface.loc.set_idioma(idioma_salvo)

        try:
            if hasattr(self.interface, "loc"):
                labels_all = [
                    self.interface.loc.get_text("CPU_Porcentagem"),
                    self.interface.loc.get_text("Memoria_RAM_Porcentagem"),
                    self.interface.loc.get_text("Discos_Porcentagem")
                ]
                destacado = self.interface.loc.get_text("Destacado") or "Destacado"
                performance_charts = self.interface.loc.get_text("performance_charts") or "Gráficos de desempenho"

            else:
                labels_all = [
                    self.interface.get_text("CPU_Porcentagem"),
                    self.interface.get_text("Memoria_RAM_Porcentagem"),
                    self.interface.get_text("Discos_Porcentagem")
                ]
                destacado = "Destacado"
                performance_charts = "Gráficos de desempenho"

        except Exception:
            labels_all = ["CPU (%)", "Memória RAM (%)", "Discos (%)"]
            destacado = "Destacado"
            performance_charts = "Gráficos de desempenho"

        ativos = [labels_all[i] for i, d in enumerate(self.detached_dialogs) if d == self._shared_dialog]
        if ativos:
            self._shared_dialog.setWindowTitle(f"{destacado}: " + ", ".join(ativos))

        else:
            self._shared_dialog.setWindowTitle(performance_charts)

    except Exception as e:
        logger.error(f"Erro ao atualizar título do diálogo compartilhado: {e}", exc_info=True)
