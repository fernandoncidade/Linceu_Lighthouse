from PySide6.QtGui import QColor
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def _obter_cores_operacao(self):
    try:
        if not self._cache_cores:
            if hasattr(self.interface, 'gerenciador_menus_ui') and hasattr(self.interface.gerenciador_menus_ui, 'gerenciador_cores'):
                gerenciador_cores = self.interface.gerenciador_menus_ui.gerenciador_cores
                self._cache_cores = {
                    self.interface.loc.get_text("op_renamed"): gerenciador_cores.obter_cor_qcolor("op_renamed"),
                    self.interface.loc.get_text("op_added"): gerenciador_cores.obter_cor_qcolor("op_added"), 
                    self.interface.loc.get_text("op_deleted"): gerenciador_cores.obter_cor_qcolor("op_deleted"),
                    self.interface.loc.get_text("op_modified"): gerenciador_cores.obter_cor_qcolor("op_modified"),
                    self.interface.loc.get_text("op_moved"): gerenciador_cores.obter_cor_qcolor("op_moved"),
                    self.interface.loc.get_text("op_scanned"): gerenciador_cores.obter_cor_qcolor("op_scanned")
                }

            else:
                self._cache_cores = {
                    self.interface.loc.get_text("op_renamed"): QColor(0, 255, 0),
                    self.interface.loc.get_text("op_added"): QColor(0, 0, 255),
                    self.interface.loc.get_text("op_deleted"): QColor(255, 0, 0),
                    self.interface.loc.get_text("op_modified"): QColor(255, 98, 0),
                    self.interface.loc.get_text("op_moved"): QColor(255, 0, 255),
                    self.interface.loc.get_text("op_scanned"): QColor(128, 128, 128)
                }

        return self._cache_cores

    except Exception as e:
        logger.error(f"Erro ao obter cores de operação: {e}", exc_info=True)
        raise
