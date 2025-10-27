from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_status(self, status_map):
    self.status_map = status_map
    self._customize_icons()
