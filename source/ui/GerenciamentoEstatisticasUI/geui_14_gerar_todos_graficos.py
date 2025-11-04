from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressDialog, QMessageBox, QApplication
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from source.utils.LogManager import LogManager
from .geui_31_worker_grafico import GraficoWorker
logger = LogManager.get_logger()

def _gerar_todos_graficos(self, graficos):
    self.graficos_dados.clear()
    self.fila_graficos = []
    self.gerando_grafico = False
    self.total_graficos = len(graficos)
    self.graficos_processados = 0

    self.progress_dialog = QProgressDialog(
        self.loc.get_text("preparing_charts_data") if self.loc else "Preparando dados para gráficos", 
        self.loc.get_text("cancel") if self.loc else "Cancelar", 
        0, self.total_graficos * 2, self.dialog_estatisticas
    )
    self.progress_dialog.setWindowTitle(self.loc.get_text("please_wait") if self.loc else "Aguarde")
    self.progress_dialog.setModal(False)
    self.progress_dialog.setMinimumDuration(0)
    self.progress_dialog.setAutoClose(False)

    self.worker = GraficoWorker(graficos)
    self.worker.dados_grafico_prontos.connect(self._enfileirar_grafico)
    self.worker.todos_concluidos.connect(self._iniciar_geracao_graficos)
    self.worker.progresso_atualizado.connect(self._atualizar_progresso_preparacao)
    self.worker.erro_ocorrido.connect(self._tratar_erro_grafico)
    self.progress_dialog.canceled.connect(self._cancelar_processo)
    self.worker.start()

def _atualizar_progresso_preparacao(self, atual, total):
    try:
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setValue(atual)
            self.progress_dialog.setLabelText(f"{self.loc.get_text('preparing_chart_data') if self.loc else 'Preparando dados do gráfico'} {atual}/{total}")
            QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao atualizar progresso de preparação: {e}", exc_info=True)

def _iniciar_geracao_graficos(self):
    try:
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setLabelText(self.loc.get_text("generating_charts") if self.loc else "Gerando gráficos")
            self.progress_dialog.setValue(self.total_graficos)
            QApplication.processEvents()

        if not self.gerando_grafico:
            self._processar_proximo_grafico()

    except Exception as e:
        logger.error(f"Erro ao iniciar geração de gráficos: {e}", exc_info=True)

def _enfileirar_grafico(self, titulo, dados, func, titulo_original):
    try:
        self.fila_graficos.append({
            'titulo': titulo, 
            'dados': dados,
            'func': func,
            'titulo_original': titulo_original
        })

    except Exception as e:
        logger.error(f"Erro ao enfileirar gráfico {titulo}: {e}", exc_info=True)

def _processar_proximo_grafico(self):
    try:
        if not self.fila_graficos:
            self.gerando_grafico = False
            self._finalizar_processo()
            return

        self.gerando_grafico = True
        grafico = self.fila_graficos.pop(0)
        self.graficos_processados += 1

        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            progresso_atual = self.total_graficos + self.graficos_processados
            self.progress_dialog.setValue(progresso_atual)
            self.progress_dialog.setLabelText(f"{self.loc.get_text('generating_chart') if self.loc else 'Gerando gráfico'}: {grafico['titulo']} ({self.graficos_processados}/{self.total_graficos})")
            QApplication.processEvents()

        QTimer.singleShot(50, lambda: self._gerar_e_adicionar_grafico(grafico))

    except Exception as e:
        logger.error(f"Erro ao processar próximo gráfico: {e}", exc_info=True)
        self.gerando_grafico = False
        self._processar_proximo_grafico()

def _gerar_e_adicionar_grafico(self, grafico):
    try:
        titulo = grafico['titulo']
        func = grafico['func']
        titulo_original = grafico['titulo_original']
        QApplication.processEvents()
        fig = func()

        self.graficos_dados[titulo] = {'fig': fig, 'func': func, 'titulo': titulo_original}

        canvas = FigureCanvas(fig)
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(canvas)
        tab.setLayout(tab_layout)
        QApplication.processEvents()

        self.tab_widget.addTab(tab, titulo)

        QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico {grafico['titulo']}: {e}", exc_info=True)
        QMessageBox.warning(
            self.dialog_estatisticas, 
            self.loc.get_text("error") if self.loc else "Erro", 
            f"{self.loc.get_text('error_generating_chart') if self.loc else 'Erro ao gerar gráfico'} {grafico['titulo']}: {str(e)}"
        )

    finally:
        self.gerando_grafico = False
        QTimer.singleShot(50, self._processar_proximo_grafico)

def _finalizar_processo(self):
    try:
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.close()

    except Exception as e:
        logger.error(f"Erro ao finalizar processo: {e}", exc_info=True)

def _cancelar_processo(self):
    try:
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            self.worker.parar()
            self.worker.wait(3000)

        self.fila_graficos.clear()
        self.gerando_grafico = False

        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.close()

    except Exception as e:
        logger.error(f"Erro ao cancelar processo: {e}", exc_info=True)

def _tratar_erro_grafico(self, titulo, erro):
    logger.error(f"Erro recebido do worker para gráfico {titulo}: {erro}")

    QMessageBox.warning(
        self.dialog_estatisticas, 
        self.loc.get_text("error") if self.loc else "Erro", 
        f"{self.loc.get_text('error_preparing_chart') if self.loc else 'Erro ao preparar dados do gráfico'} {titulo}: {erro}"
    )
