from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from GerenciamentoUI.ui_02_GerenciadorBotoesUI import GerenciadorBotoesUI
from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
from .fil_02_AdministradorCalendario import AdministradorCalendario
from .fil_03_AdministradorFiltros import AdministradorFiltros
from Filtros.GerenciamentoFiltros.gfil_01_on_idioma_alterado import on_idioma_alterado
from Filtros.GerenciamentoFiltros.gfil_02_desconectar_sinais import _desconectar_sinais
from Filtros.GerenciamentoFiltros.gfil_03_atualizar_status import atualizar_status
from Filtros.GerenciamentoFiltros.gfil_04_setup_ui import setup_ui
from Filtros.GerenciamentoFiltros.gfil_05_on_filtro_alterado import on_filtro_alterado
from Filtros.GerenciamentoFiltros.gfil_06_sincronizar_com_menu_principal import sincronizar_com_menu_principal
from Filtros.GerenciamentoFiltros.gfil_07_verificar_filtro_operacao import verificar_filtro_operacao
from Filtros.GerenciamentoFiltros.gfil_08_atualizar_contagem import atualizar_contagem
from Filtros.GerenciamentoFiltros.gfil_09_atualizar_interface import atualizar_interface
from Filtros.GerenciamentoFiltros.gfil_10_limpar_filtros import limpar_filtros
from utils.IconUtils import get_icon_path
from utils.LogManager import LogManager
logger = LogManager.get_logger()

class Filtros(QWidget):
    filtroAplicado = Signal()

    def __init__(self, tabela_dados, loc=None):
        super().__init__()
        try:
            self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
            self.setAttribute(Qt.WA_DeleteOnClose, False)
            self.setWindowModality(Qt.NonModal)
            self.loc = loc if loc is not None else LocalizadorQt()
            self.setWindowTitle(self.loc.get_text("advanced_filters"))
            self.setWindowIcon(QIcon(get_icon_path("filtro.ico")))
            self.tabela_dados = tabela_dados
            self.gerenciador_botoes = GerenciadorBotoesUI(self)
            self.administrador_calendario = AdministradorCalendario(self)
            self.administrador_filtros = AdministradorFiltros(self)
            self.loc.idioma_alterado.connect(self.on_idioma_alterado)
            self.destroyed.connect(self._desconectar_sinais)
            self.setup_ui()

        except Exception as e:
            logger.error(f"Erro ao inicializar filtros: {e}", exc_info=True)

    on_idioma_alterado = on_idioma_alterado
    _desconectar_sinais = _desconectar_sinais
    atualizar_status = atualizar_status
    setup_ui = setup_ui
    on_filtro_alterado = on_filtro_alterado
    sincronizar_com_menu_principal = sincronizar_com_menu_principal
    verificar_filtro_operacao = verificar_filtro_operacao
    atualizar_contagem = atualizar_contagem
    atualizar_interface = atualizar_interface
    limpar_filtros = limpar_filtros
