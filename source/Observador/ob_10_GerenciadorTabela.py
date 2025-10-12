import concurrent.futures
import threading
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QAbstractItemView
from utils.LogManager import LogManager

from source.Observador.GerenciamentoTabela.gtab_01_detectar_tema_windows import detectar_tema_windows
from source.Observador.GerenciamentoTabela.gtab_02_calcular_cor_texto_ideal import calcular_cor_texto_ideal, _eh_cor_fundo_padrao
from source.Observador.GerenciamentoTabela.gtab_03_configurar_tabela import configurar_tabela
from source.Observador.GerenciamentoTabela.gtab_04_ajustar_larguras_colunas import ajustar_larguras_colunas
from source.Observador.GerenciamentoTabela.gtab_05_aplicar_quebra_linha_cabecalho import aplicar_quebra_linha_cabecalho
from source.Observador.GerenciamentoTabela.gtab_06_aplicar_quebra_linha_todos_cabecalhos import aplicar_quebra_linha_todos_cabecalhos
from source.Observador.GerenciamentoTabela.gtab_07_ajustar_altura_cabecalho import ajustar_altura_cabecalho
from source.Observador.GerenciamentoTabela.gtab_08_redimensionar_cabecalho import redimensionar_cabecalho
from source.Observador.GerenciamentoTabela.gtab_43_atualizar_cabecalhos import atualizar_cabecalhos
from source.Observador.GerenciamentoTabela.gtab_10_atualizar_dados_tabela import atualizar_dados_tabela
from source.Observador.GerenciamentoTabela.gtab_11_atualizar_linha_mais_recente import atualizar_linha_mais_recente
from source.Observador.GerenciamentoTabela.gtab_12_atualizar_visualizacao_tabela import atualizar_visualizacao_tabela
from source.Observador.GerenciamentoTabela.gtab_13_atualizar_visibilidade_colunas import atualizar_visibilidade_colunas
from source.Observador.GerenciamentoTabela.gtab_14_invalidar_cache_cores import _invalidar_cache_cores
from source.Observador.GerenciamentoTabela.gtab_15_obter_cores_operacao import _obter_cores_operacao
from source.Observador.GerenciamentoTabela.gtab_16_obter_indices_colunas import _obter_indices_colunas
from source.Observador.GerenciamentoTabela.gtab_17_ativar_cores import ativar_cores
from source.Observador.GerenciamentoTabela.gtab_18_ocultar_cores import ocultar_cores
from source.Observador.GerenciamentoTabela.gtab_19_aplicar_cores_linha_especifica import aplicar_cores_linha_especifica
from source.Observador.GerenciamentoTabela.gtab_20_aplicar_cores_todas_colunas import aplicar_cores_todas_colunas
from source.Observador.GerenciamentoTabela.gtab_21_redefinir_cores_todas_colunas import redefinir_cores_todas_colunas
from source.Observador.GerenciamentoTabela.gtab_22_remover_cor_coluna import remover_cor_coluna
from source.Observador.GerenciamentoTabela.gtab_23_atualizar_cores_colunas import atualizar_cores_colunas
from source.Observador.GerenciamentoTabela.gtab_24_set_coluna_colorir import set_coluna_colorir
from source.Observador.GerenciamentoTabela.gtab_25_set_colunas_colorir_em_massa import set_colunas_colorir_em_massa
from source.Observador.GerenciamentoTabela.gtab_26_remover_todas_cores_colunas import remover_todas_cores_colunas
from source.Observador.GerenciamentoTabela.gtab_27_salvar_configuracoes_cores import salvar_configuracoes_cores
from source.Observador.GerenciamentoTabela.gtab_28_carregar_configuracoes_cores import _carregar_configuracoes_cores
from source.Observador.GerenciamentoTabela.gtab_29_eh_coluna_personalizada_colorida import eh_coluna_personalizada_colorida
from source.Observador.GerenciamentoTabela.gtab_30_mostrar_dialogo_configuracao import mostrar_dialogo_configuracao
from source.Observador.GerenciamentoTabela.gtab_31_ajustar_cor_selecao import ajustar_cor_selecao
from source.Observador.GerenciamentoTabela.gtab_33_atualizar_estilo_tema import (atualizar_estilo_tema, _atualizar_cores_celulas_incolores, _eh_cor_padrao_qualquer_tema, _forcar_reconstrucao_todas_celulas)
from source.Observador.GerenciamentoTabela.gtab_34_monitor_tema_windows import MonitorTemaWindows
from source.Observador.GerenciamentoTabela.gtab_35_iniciar_processamento_pesado import iniciar_processamento_pesado
from source.Observador.GerenciamentoTabela.gtab_36_aplicar_cores_todas_colunas_processamento import aplicar_cores_todas_colunas_processamento
from source.Observador.GerenciamentoTabela.gtab_37_processar_cores_em_background import _processar_cores_em_background
from source.Observador.GerenciamentoTabela.gtab_38_on_cores_processadas import _on_cores_processadas
from source.Observador.GerenciamentoTabela.gtab_39_atualizar_cores_na_interface import _atualizar_cores_na_interface
from source.Observador.GerenciamentoTabela.gtab_40_atualizar_interface_pos_processamento import atualizar_interface_pos_processamento
from source.Observador.GerenciamentoTabela.gtab_41_processar_selecao_background import _processar_selecao_background
from source.Observador.GerenciamentoTabela.gtab_42_shutdown_executors import shutdown_executors
from source.Observador.GerenciamentoTabela.gtab_44_on_idioma_alterado import _on_idioma_alterado
from source.Observador.GerenciamentoTabela.gtab_45_retraduzir_dados_existentes import retraduzir_dados_existentes
from source.Observador.GerenciamentoTabela.gtab_46_executar_retraducao_agendada import _executar_retraducao_agendada

logger = LogManager.get_logger()


class GerenciadorTabela(QObject):
    cores_processadas = Signal(dict)

    def __init__(self, interface_monitor):
        super().__init__()
        try:
            self.interface = interface_monitor
            self.lock_db = threading.Lock()
            self.loc = interface_monitor.loc

            if hasattr(self.loc, 'idioma_alterado'):
                self.loc.idioma_alterado.connect(self.atualizar_cabecalhos)
                self.loc.idioma_alterado.connect(self._on_idioma_alterado)

            self._idioma_ultima_retraducao = getattr(self.loc, 'idioma_atual', None)
            self._retraducao_realizada_para_idioma = False
            self._idioma_alvo_retraducao = getattr(self.loc, 'idioma_atual', None)
            self._monitor_tema = MonitorTemaWindows()
            self._monitor_tema.tema_alterado.connect(self.atualizar_estilo_tema)
            self._monitor_tema.iniciar_monitoramento()
            self.timer_atualizacao = QTimer()
            self.timer_atualizacao.timeout.connect(self.atualizar_visualizacao_tabela)
            self.timer_atualizacao.start(100)
            self.atualizacao_pendente = False
            self.texto_original_cabecalhos = {}
            self.colunas_para_colorir = set()

            if hasattr(self.interface, 'tabela_dados'):
                self.interface.tabela_dados.setSelectionBehavior(QAbstractItemView.SelectItems)
                self.interface.tabela_dados.setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.interface.tabela_dados.itemSelectionChanged.connect(self.ajustar_cor_selecao)

            self._itens_selecionados_anteriores = []
            self._cache_cores = {}
            self._cache_indices_colunas = {}
            self.cores_visiveis = True
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
            self._cores_originais_cache = {}
            self.ordenacao_habilitada = False
            self._selection_executor = None
            self._selection_future = None
            self._debounce_timer = None
            self._timer_retraducao = QTimer(self)
            self._timer_retraducao.setSingleShot(True)
            self._timer_retraducao.timeout.connect(self._executar_retraducao_agendada)
            self._retraducao_em_andamento = False
            self._retraducao_agendada = False
            QTimer.singleShot(0, lambda: self._carregar_configuracoes_cores())

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorTabela: {e}", exc_info=True)

    detectar_tema_windows = detectar_tema_windows
    calcular_cor_texto_ideal = calcular_cor_texto_ideal
    _eh_cor_fundo_padrao = _eh_cor_fundo_padrao
    configurar_tabela = configurar_tabela
    ajustar_larguras_colunas = ajustar_larguras_colunas
    aplicar_quebra_linha_cabecalho = aplicar_quebra_linha_cabecalho
    aplicar_quebra_linha_todos_cabecalhos = aplicar_quebra_linha_todos_cabecalhos
    ajustar_altura_cabecalho = ajustar_altura_cabecalho
    redimensionar_cabecalho = redimensionar_cabecalho
    atualizar_cabecalhos = atualizar_cabecalhos
    atualizar_dados_tabela = atualizar_dados_tabela
    atualizar_linha_mais_recente = atualizar_linha_mais_recente
    atualizar_visualizacao_tabela = atualizar_visualizacao_tabela
    atualizar_visibilidade_colunas = atualizar_visibilidade_colunas
    _invalidar_cache_cores = _invalidar_cache_cores
    _obter_cores_operacao = _obter_cores_operacao
    _obter_indices_colunas = _obter_indices_colunas
    ativar_cores = ativar_cores
    ocultar_cores = ocultar_cores
    aplicar_cores_linha_especifica = aplicar_cores_linha_especifica
    aplicar_cores_todas_colunas = aplicar_cores_todas_colunas
    redefinir_cores_todas_colunas = redefinir_cores_todas_colunas
    remover_cor_coluna = remover_cor_coluna
    atualizar_cores_colunas = atualizar_cores_colunas
    set_coluna_colorir = set_coluna_colorir
    set_colunas_colorir_em_massa = set_colunas_colorir_em_massa
    remover_todas_cores_colunas = remover_todas_cores_colunas
    salvar_configuracoes_cores = salvar_configuracoes_cores
    _carregar_configuracoes_cores = _carregar_configuracoes_cores
    eh_coluna_personalizada_colorida = eh_coluna_personalizada_colorida
    mostrar_dialogo_configuracao = mostrar_dialogo_configuracao
    ajustar_cor_selecao = ajustar_cor_selecao
    atualizar_estilo_tema = atualizar_estilo_tema
    _atualizar_cores_celulas_incolores = _atualizar_cores_celulas_incolores
    _eh_cor_padrao_qualquer_tema = _eh_cor_padrao_qualquer_tema
    _forcar_reconstrucao_todas_celulas = _forcar_reconstrucao_todas_celulas
    _processar_selecao_background = _processar_selecao_background
    iniciar_processamento_pesado = iniciar_processamento_pesado
    aplicar_cores_todas_colunas_processamento = aplicar_cores_todas_colunas_processamento
    _processar_cores_em_background = _processar_cores_em_background
    _on_cores_processadas = _on_cores_processadas
    _atualizar_cores_na_interface = _atualizar_cores_na_interface
    atualizar_interface_pos_processamento = atualizar_interface_pos_processamento
    shutdown_executors = shutdown_executors
    _on_idioma_alterado = _on_idioma_alterado
    retraduzir_dados_existentes = retraduzir_dados_existentes
    _executar_retraducao_agendada = _executar_retraducao_agendada
