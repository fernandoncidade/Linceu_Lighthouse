from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, Qt
from source.utils.LogManager import LogManager
from source.ui.GerenciamentoDialogoCores.gdc_01_setup_ui import setup_ui
from source.ui.GerenciamentoDialogoCores.gdc_02_adicionar_grid_cores import _adicionar_grid_cores
from source.ui.GerenciamentoDialogoCores.gdc_03_selecionar_cor import _selecionar_cor
from source.ui.GerenciamentoDialogoCores.gdc_04_abrir_seletor_avancado import _abrir_seletor_avancado
from source.ui.GerenciamentoDialogoCores.gdc_05_accept import accept
from source.ui.GerenciamentoDialogoCores.gdc_06_traduzir_dialogo_cores import _traduzir_dialogo_cores
from source.ui.GerenciamentoDialogoCores.gdc_07_obter_cor import obter_cor
from source.ui.GerenciamentoDialogoCores.gdc_08_atualizar_traducoes import atualizar_traducoes
logger = LogManager.get_logger()


class DialogoPaletaCores(QDialog):
    corSelecionada = Signal(QColor)

    def __init__(self, cor_atual, interface_principal, titulo=None, parent=None, tipo_operacao=None):
        super().__init__(parent)
        try:
            self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
            self.setModal(False)

            self.interface = interface_principal
            self.tipo_operacao = tipo_operacao

            try:
                if hasattr(interface_principal, 'loc'):
                    self.loc = interface_principal.loc

                else:
                    from source.ui.ui_12_LocalizadorQt import LocalizadorQt
                    self.loc = LocalizadorQt()

            except Exception as e:
                logger.error(f"Erro ao obter localizador: {e}", exc_info=True)
                from source.ui.ui_12_LocalizadorQt import LocalizadorQt
                self.loc = LocalizadorQt()

            if titulo is None:
                titulo = self.loc.get_text("select_color")

            self.setWindowTitle(titulo)

            self.cor_atual = cor_atual
            self.cor_selecionada = None
            self.setup_ui()

            try:
                if hasattr(self.loc, "traducoes_carregadas"):
                    self.loc.traducoes_carregadas.connect(self.atualizar_traducoes)

            except Exception as e:
                logger.error(f"Não foi possível conectar sinal de traduções no DialogoPaletaCores: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao configurar diálogo de cores: {e}", exc_info=True)

    setup_ui = setup_ui
    _adicionar_grid_cores = _adicionar_grid_cores
    _selecionar_cor = _selecionar_cor
    _abrir_seletor_avancado = _abrir_seletor_avancado
    accept = accept
    _traduzir_dialogo_cores = _traduzir_dialogo_cores
    obter_cor = obter_cor
    atualizar_traducoes = atualizar_traducoes
