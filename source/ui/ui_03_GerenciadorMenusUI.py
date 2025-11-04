from source.utils.LogManager import LogManager
from source.ui.GerenciamentoMenusUI.gmui_02_GerenciadorCores import GerenciadorCores
from source.ui.GerenciamentoMenusUI.gmui_04_criar_menu_principal import criar_menu_principal
from source.ui.GerenciamentoMenusUI.gmui_05_configurar_menu_arquivo import _configurar_menu_arquivo
from source.ui.GerenciamentoMenusUI.gmui_06_configurar_menu_configuracoes import _configurar_menu_configuracoes
from source.ui.GerenciamentoMenusUI.gmui_07_configurar_menu_opcoes import _configurar_menu_opcoes
from source.ui.GerenciamentoMenusUI.gmui_08_criar_submenu_cores import _criar_submenu_cores
from source.ui.GerenciamentoMenusUI.gmui_09_criar_icone_cor import _criar_icone_cor
from source.ui.GerenciamentoMenusUI.gmui_10_abrir_dialogo_cor import _abrir_dialogo_cor
from source.ui.GerenciamentoMenusUI.gmui_11_criar_submenu_colunas import _criar_submenu_colunas
from source.ui.GerenciamentoMenusUI.gmui_12_alternar_ordenacao_linhas import _alternar_ordenacao_linhas
from source.ui.GerenciamentoMenusUI.gmui_13_criar_submenu_colunas_coloridas import _criar_submenu_colunas_coloridas
from source.ui.GerenciamentoMenusUI.gmui_14_selecionar_todas_colunas import selecionar_todas_colunas
from source.ui.GerenciamentoMenusUI.gmui_15_selecionar_todas_cores_colunas import selecionar_todas_cores_colunas
from source.ui.GerenciamentoMenusUI.gmui_16_criar_submenu_exportacao import _criar_submenu_exportacao
from source.ui.GerenciamentoMenusUI.gmui_17_resetar_opcoes_exportacao import _resetar_opcoes_exportacao
from source.ui.GerenciamentoMenusUI.gmui_18_criar_submenu_idiomas import _criar_submenu_idiomas
from source.ui.GerenciamentoMenusUI.gmui_19_get_texto_traduzido_para_idioma import _get_texto_traduzido_para_idioma
from source.ui.GerenciamentoMenusUI.gmui_20_confirmar_alteracao_idioma import _confirmar_alteracao_idioma
from source.ui.GerenciamentoMenusUI.gmui_21_on_traducoes_carregadas import _on_traducoes_carregadas
from source.ui.GerenciamentoMenusUI.gmui_22_exibir_sobre import _exibir_sobre
from source.ui.GerenciamentoMenusUI.gmui_23_toggle_desempenho import _criar_acao_toggle_desempenho
logger = LogManager.get_logger()


class GerenciadorMenusUI:
    def __init__(self, interface_principal):
        self.interface = interface_principal
        self.loc = interface_principal.loc
        self.acoes_colunas = {}
        self.gerenciador_cores = GerenciadorCores(interface_principal)
        self.interface._ordenacao_linhas_habilitada = False
        self._acoes_idioma = {}
        self._trocando_idioma = False
        self._aguardando_conclusao_traducao = False
        try:
            if hasattr(self.interface, "loc") and hasattr(self.interface.loc, "traducoes_carregadas"):
                self.interface.loc.traducoes_carregadas.connect(self._on_traducoes_carregadas)

        except Exception as e:
            logger.error(f"Falha ao conectar sinal de traduções: {e}")

    criar_menu_principal = criar_menu_principal
    _configurar_menu_arquivo = _configurar_menu_arquivo
    _configurar_menu_configuracoes = _configurar_menu_configuracoes
    _configurar_menu_opcoes = _configurar_menu_opcoes
    _criar_submenu_cores = _criar_submenu_cores
    _criar_icone_cor = _criar_icone_cor
    _abrir_dialogo_cor = _abrir_dialogo_cor
    _criar_submenu_colunas = _criar_submenu_colunas
    _alternar_ordenacao_linhas = _alternar_ordenacao_linhas
    _criar_submenu_colunas_coloridas = _criar_submenu_colunas_coloridas
    selecionar_todas_colunas = selecionar_todas_colunas
    selecionar_todas_cores_colunas = selecionar_todas_cores_colunas
    _criar_submenu_exportacao = _criar_submenu_exportacao
    _resetar_opcoes_exportacao = _resetar_opcoes_exportacao
    _criar_submenu_idiomas = _criar_submenu_idiomas
    _get_texto_traduzido_para_idioma = _get_texto_traduzido_para_idioma
    _confirmar_alteracao_idioma = _confirmar_alteracao_idioma
    _on_traducoes_carregadas = _on_traducoes_carregadas
    _exibir_sobre = _exibir_sobre
    _criar_acao_toggle_desempenho = _criar_acao_toggle_desempenho
