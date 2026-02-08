from PySide6.QtWidgets import QFileDialog
from source.Observador.ob_01_Observador import Observador
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def selecionar_diretorio(self):
    try:
        dir_selecionado = QFileDialog.getExistingDirectory(self.interface, self.loc.get_text("select_dir"))
        if dir_selecionado:
            self.interface.diretorio_atual = dir_selecionado
            self.interface.rotulo_diretorio.setText(self.loc.get_text("dir_selected").format(self.interface.diretorio_atual))
            if hasattr(self.interface, 'reiniciar_sistema_monitoramento'):
                self.interface.reiniciar_sistema_monitoramento()

            if not self.interface.observador:
                self.interface.observador = Observador(self.interface.diretorio_atual, self.interface.adicionar_evento)
                self.interface.observador.interface = self.interface

            else:
                self.interface.observador.diretorio = self.interface.diretorio_atual

    except Exception as e:
        logger.error(f"Erro ao selecionar diretório: {e}", exc_info=True)
