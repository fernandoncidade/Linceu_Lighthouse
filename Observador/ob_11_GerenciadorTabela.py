import concurrent.futures
import threading
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QAbstractItemView, QApplication
from utils.LogManager import LogManager

from Observador.GerenciamentoTabela.gtab_01_detectar_tema_windows import detectar_tema_windows
from Observador.GerenciamentoTabela.gtab_02_calcular_cor_texto_ideal import calcular_cor_texto_ideal, _eh_cor_fundo_padrao
from Observador.GerenciamentoTabela.gtab_03_configurar_tabela import configurar_tabela, _processar_selecao_background
from Observador.GerenciamentoTabela.gtab_04_ajustar_larguras_colunas import ajustar_larguras_colunas
from Observador.GerenciamentoTabela.gtab_05_aplicar_quebra_linha_cabecalho import aplicar_quebra_linha_cabecalho
from Observador.GerenciamentoTabela.gtab_06_aplicar_quebra_linha_todos_cabecalhos import aplicar_quebra_linha_todos_cabecalhos
from Observador.GerenciamentoTabela.gtab_07_ajustar_altura_cabecalho import ajustar_altura_cabecalho
from Observador.GerenciamentoTabela.gtab_08_redimensionar_cabecalho import redimensionar_cabecalho
from Observador.GerenciamentoTabela.gtab_09_atualizar_cabecalhos import atualizar_cabecalhos
from Observador.GerenciamentoTabela.gtab_10_atualizar_dados_tabela import atualizar_dados_tabela
from Observador.GerenciamentoTabela.gtab_11_atualizar_linha_mais_recente import atualizar_linha_mais_recente
from Observador.GerenciamentoTabela.gtab_12_atualizar_visualizacao_tabela import atualizar_visualizacao_tabela
from Observador.GerenciamentoTabela.gtab_13_atualizar_visibilidade_colunas import atualizar_visibilidade_colunas
from Observador.GerenciamentoTabela.gtab_14_invalidar_cache_cores import _invalidar_cache_cores
from Observador.GerenciamentoTabela.gtab_15_obter_cores_operacao import _obter_cores_operacao
from Observador.GerenciamentoTabela.gtab_16_obter_indices_colunas import _obter_indices_colunas
from Observador.GerenciamentoTabela.gtab_17_ativar_cores import ativar_cores
from Observador.GerenciamentoTabela.gtab_18_ocultar_cores import ocultar_cores
from Observador.GerenciamentoTabela.gtab_19_aplicar_cores_linha_especifica import aplicar_cores_linha_especifica
from Observador.GerenciamentoTabela.gtab_20_aplicar_cores_todas_colunas import aplicar_cores_todas_colunas
from Observador.GerenciamentoTabela.gtab_21_redefinir_cores_todas_colunas import redefinir_cores_todas_colunas
from Observador.GerenciamentoTabela.gtab_22_remover_cor_coluna import remover_cor_coluna
from Observador.GerenciamentoTabela.gtab_23_atualizar_cores_colunas import atualizar_cores_colunas
from Observador.GerenciamentoTabela.gtab_24_set_coluna_colorir import set_coluna_colorir
from Observador.GerenciamentoTabela.gtab_25_set_colunas_colorir_em_massa import set_colunas_colorir_em_massa
from Observador.GerenciamentoTabela.gtab_26_remover_todas_cores_colunas import remover_todas_cores_colunas
from Observador.GerenciamentoTabela.gtab_27_salvar_configuracoes_cores import salvar_configuracoes_cores
from Observador.GerenciamentoTabela.gtab_28_carregar_configuracoes_cores import _carregar_configuracoes_cores
from Observador.GerenciamentoTabela.gtab_29_eh_coluna_personalizada_colorida import eh_coluna_personalizada_colorida
from Observador.GerenciamentoTabela.gtab_30_mostrar_dialogo_configuracao import mostrar_dialogo_configuracao
from Observador.GerenciamentoTabela.gtab_31_ajustar_cor_selecao import ajustar_cor_selecao
from Observador.GerenciamentoTabela.gtab_32_worker_thread import WorkerThread
from Observador.GerenciamentoTabela.gtab_33_atualizar_estilo_tema import (atualizar_estilo_tema, _atualizar_cores_celulas_incolores, 
                                                                          _eh_cor_padrao_qualquer_tema, _forcar_reconstrucao_todas_celulas)
from Observador.GerenciamentoTabela.gtab_34_monitor_tema_windows import MonitorTemaWindows

logger = LogManager.get_logger()


class GerenciadorTabela(QObject):
    cores_processadas = Signal(dict)

    def __init__(self, interface_monitor):
        super().__init__()
        self.interface = interface_monitor
        self.lock_db = threading.Lock()
        self.loc = interface_monitor.loc
        self.loc.idioma_alterado.connect(self.atualizar_cabecalhos)
        self._idioma_ultima_retraducao = self.loc.idioma_atual
        self._retraducao_realizada_para_idioma = False
        self._idioma_alvo_retraducao = self.loc.idioma_atual
        self.loc.idioma_alterado.connect(self._on_idioma_alterado)
        self._monitor_tema = MonitorTemaWindows()
        self._monitor_tema.tema_alterado.connect(self.atualizar_estilo_tema)
        self._monitor_tema.iniciar_monitoramento()
        self.timer_atualizacao = QTimer()
        self.timer_atualizacao.timeout.connect(self.atualizar_visualizacao_tabela)
        self.timer_atualizacao.start(100)
        self.atualizacao_pendente = False
        self.texto_original_cabecalhos = {}
        self.colunas_para_colorir = set()
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

        logger.info("GerenciadorTabela inicializado com sucesso.")

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

    def iniciar_processamento_pesado(self, dados, callback=None):
        def processamento_pesado(dados):
            self._invalidar_cache_cores()
            self.aplicar_cores_todas_colunas()
            self.redefinir_cores_todas_colunas()
            self.atualizar_dados_tabela(self.interface.tabela_dados)
            self.atualizar_linha_mais_recente(self.interface.tabela_dados)
            self.atualizar_visualizacao_tabela()
            self.atualizar_visibilidade_colunas(atualizar_em_massa=True)
            self.atualizar_cores_colunas(aplicar_em_massa=True)
            self.ajustar_cor_selecao()
            return True

        self.worker = WorkerThread(dados, processamento_pesado)
        if callback:
            self.worker.finished.connect(callback)

    def aplicar_cores_todas_colunas_processamento(self, dados):
        future = self.executor.submit(self._processar_cores_em_background, dados)
        future.add_done_callback(self._on_cores_processadas)

    def _processar_cores_em_background(self, dados):
        resultado = {}
        tabela = self.interface.tabela_dados
        cores_operacao = self._obter_cores_operacao()
        cor_padrao = cores_operacao.get(self.loc.get_text("op_scanned"))
        cor_texto_padrao = self.calcular_cor_texto_ideal(cor_padrao)
        header_indices = self._obter_indices_colunas(tabela)
        colunas = list(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items())
        for row in range(tabela.rowCount()):
            tipo_operacao_valor = ""
            indice_tipo_operacao = header_indices.get(
                self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS["tipo_operacao"]["nome"].replace('\n', ' ').strip()
            )

            if indice_tipo_operacao is not None:
                item_tipo = tabela.item(row, indice_tipo_operacao)
                tipo_operacao_valor = item_tipo.text() if item_tipo else ""

            for key, coluna in colunas:
                nome_coluna = coluna["nome"].replace('\n', ' ').strip()
                indice_coluna = header_indices.get(nome_coluna)
                if indice_coluna is None or indice_coluna >= tabela.columnCount():
                    continue

                if key != "tipo_operacao" and key not in self.colunas_para_colorir:
                    cor_fundo = cor_padrao
                    cor_texto = cor_texto_padrao

                elif not self.cores_visiveis:
                    cor_fundo = cor_padrao
                    cor_texto = cor_texto_padrao

                else:
                    cor_fundo = cores_operacao.get(tipo_operacao_valor, cor_padrao)
                    cor_texto = self.calcular_cor_texto_ideal(cor_fundo, eh_coluna_personalizada=(key != "tipo_operacao"))

                resultado[(row, indice_coluna)] = (cor_fundo, cor_texto)

        return resultado

    def _on_cores_processadas(self, future):
        resultado = future.result()
        self.cores_processadas.emit(resultado)

    def _atualizar_cores_na_interface(self, resultado):
        tabela = self.interface.tabela_dados
        tabela.blockSignals(True)
        try:
            for (row, col), (cor_fundo, cor_texto) in resultado.items():
                item = tabela.item(row, col)
                if item:
                    item.setBackground(cor_fundo)
                    item.setForeground(cor_texto)

            tabela.viewport().update()

        finally:
            tabela.blockSignals(False)
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()

        self.atualizacao_pendente = True

    def atualizar_interface_pos_processamento(self, resultado):
        self.atualizar_visualizacao_tabela()
        if hasattr(self.interface, 'atualizar_status'):
            self.interface.atualizar_status()

        if hasattr(self.interface, 'atualizar_contador_eventos'):
            try:
                total_linhas = self.interface.tabela_dados.rowCount()
                self.interface.atualizar_contador_eventos(total_linhas)

            except Exception:
                pass

        if hasattr(self, 'ajustar_cor_selecao'):
            self.ajustar_cor_selecao()

    def _processar_selecao_background(self):
        try:
            QTimer.singleShot(0, self.ajustar_cor_selecao)
            return True

        except Exception as e:
            logger.error(f"Erro no processamento background de seleção: {e}", exc_info=True)
            return False

    def shutdown_executors(self):
        try:
            if hasattr(self, '_monitor_tema') and self._monitor_tema:
                self._monitor_tema.parar_monitoramento()
                logger.debug("Monitor de tema parado com sucesso")

            if hasattr(self, '_selection_executor') and self._selection_executor:
                self._selection_executor.shutdown(wait=True)
                logger.debug("Selection executor encerrado com sucesso")

            if hasattr(self, 'executor') and self.executor:
                self.executor.shutdown(wait=True)
                logger.debug("Main executor encerrado com sucesso")

        except Exception as e:
            logger.error(f"Erro ao encerrar executors: {e}", exc_info=True)

    def _on_idioma_alterado(self, idioma: str):
        try:
            self._idioma_alvo_retraducao = idioma
            self._retraducao_realizada_para_idioma = False
            self.retraduzir_dados_existentes()

        except Exception as e:
            logger.error(f"Erro no handler de idioma_alterado: {e}", exc_info=True)

    def retraduzir_dados_existentes(self):
        try:
            if self._retraducao_realizada_para_idioma and self.loc.idioma_atual == self._idioma_ultima_retraducao:
                logger.debug("Retradução já realizada para este idioma; ignorando chamada.")
                return

            if self._retraducao_em_andamento:
                self._retraducao_agendada = True
                return

            if self._timer_retraducao.isActive():
                return

            self._retraducao_agendada = True
            self._timer_retraducao.start(50)

        except Exception as e:
            logger.error(f"Erro ao agendar retradução: {e}", exc_info=True)

    def _executar_retraducao_agendada(self):
        if not self._retraducao_agendada:
            return

        if self._retraducao_realizada_para_idioma and self.loc.idioma_atual == self._idioma_ultima_retraducao:
            logger.debug("Ignorando execução de retradução: já concluída para este idioma.")
            return

        self._retraducao_agendada = False
        self._retraducao_em_andamento = True
        try:
            logger.debug("Iniciando retradução de dados existentes")

            if not hasattr(self.interface, 'tabela_dados'):
                return

            tabela = self.interface.tabela_dados
            tabela.blockSignals(True)
            tabela.setUpdatesEnabled(False)
            if hasattr(self.interface, 'gerenciador_progresso_ui'):
                self.interface.gerenciador_progresso_ui.criar_barra_progresso()
                self.interface.rotulo_resultado.setText(self.loc.get_text("translating_table"))

            header_indices = self._obter_indices_colunas(tabela)
            colunas_traduziveis = ["tipo_operacao","atributos","protegido"]
            mapa_colunas = {}
            for key, coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items():
                nome_coluna = coluna["nome"].replace('\n', ' ').strip()
                mapa_colunas[nome_coluna] = key

            total_linhas = tabela.rowCount()
            for row in range(total_linhas):
                tipo_operacao_valor = None
                for nome_coluna, indice_coluna in header_indices.items():
                    key = mapa_colunas.get(nome_coluna)
                    if key == "tipo_operacao":
                        item = tabela.item(row, indice_coluna)
                        if item:
                            valor_atual = item.text()
                            valor_retraduzido = self.loc.traduzir_tipo_operacao(valor_atual)
                            if valor_atual != valor_retraduzido:
                                item.setText(valor_retraduzido)

                            tipo_operacao_valor = valor_retraduzido

                        break

                for nome_coluna, indice_coluna in header_indices.items():
                    key = mapa_colunas.get(nome_coluna)
                    if key and key in colunas_traduziveis and key != "tipo_operacao":
                        item = tabela.item(row, indice_coluna)
                        if item:
                            valor_atual = item.text()
                            if valor_atual:
                                valor_retraduzido = self.loc.traduzir_metadados(valor_atual, key)
                                if valor_atual != valor_retraduzido:
                                    item.setText(valor_retraduzido)

                if tipo_operacao_valor and self.cores_visiveis:
                    self.aplicar_cores_linha_especifica(tabela, row, tipo_operacao_valor)

                if hasattr(self.interface, 'gerenciador_progresso_ui') and row % 100 == 0:
                    progresso = int((row + 1) * 100 / total_linhas) if total_linhas else 100
                    self.interface.gerenciador_progresso_ui.atualizar_progresso_traducao(progresso, row + 1, total_linhas)
                    QApplication.processEvents()

            logger.debug(f"Retradução concluída para {total_linhas} linhas")

        except Exception as e:
            logger.error(f"Erro ao retraduzir dados existentes: {e}", exc_info=True)

        finally:
            try:
                if hasattr(self.interface, 'tabela_dados'):
                    tabela = self.interface.tabela_dados
                    tabela.setUpdatesEnabled(True)
                    tabela.blockSignals(False)
                    tabela.viewport().update()
                    QApplication.processEvents()

            except Exception:
                pass

            try:
                if hasattr(self.interface, 'gerenciador_progresso_ui'):
                    from InterfaceCore.ic_05_GerenciadorProgresso import GerenciadorProgresso
                    GerenciadorProgresso.esconder_barra_progresso(self.interface)
                    self.interface.rotulo_resultado.setText(self.loc.get_text("translation_complete"))

            except Exception:
                pass

            self._idioma_ultima_retraducao = self.loc.idioma_atual
            self._retraducao_realizada_para_idioma = True
            self._retraducao_em_andamento = False
            self._retraducao_agendada = False
