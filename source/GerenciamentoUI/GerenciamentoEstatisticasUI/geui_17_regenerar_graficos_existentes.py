from PySide6.QtWidgets import QVBoxLayout, QApplication, QProgressDialog, QMessageBox
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from utils.LogManager import LogManager
logger = LogManager.get_logger()

try:
    from shiboken6 import isValid as _shiboken_is_valid

except Exception:
    _shiboken_is_valid = None

def _close_widget_safe(widget):
    try:
        if not widget:
            return

        if _shiboken_is_valid and not _shiboken_is_valid(widget):
            return

        try:
            widget.close()

        except RuntimeError:
            try:
                widget.deleteLater()

            except Exception:
                pass

    except Exception:
        pass

def _regenerar_graficos_existentes(self, graficos_atualizados, mapeamento_funcoes):
    try:
        if hasattr(self, 'progress_regeneracao') and self.progress_regeneracao:
            _close_widget_safe(self.progress_regeneracao)
            self.progress_regeneracao = None

        if not self.tab_widget or self.tab_widget.count() == 0:
            return

        graficos_para_atualizar = []

        for i in range(self.tab_widget.count()):
            titulo_atual = self.tab_widget.tabText(i)

            func_correspondente = None
            for titulo_antigo, data in self.checkboxes_graficos.items():
                if titulo_antigo == titulo_atual or mapeamento_funcoes.get(data['grafico_data']['func']) == titulo_atual:
                    func_correspondente = data['grafico_data']['func']
                    break

            if func_correspondente:
                grafico_atualizado = None
                for grafico in graficos_atualizados:
                    if grafico['func'] == func_correspondente:
                        grafico_atualizado = grafico
                        break

                if grafico_atualizado:
                    graficos_para_atualizar.append({
                        'index': i,
                        'titulo_atual': titulo_atual,
                        'grafico': grafico_atualizado
                    })

        if not graficos_para_atualizar:
            return

        self.graficos_para_regenerar = graficos_para_atualizar
        self.indice_regeneracao_atual = 0

        if not getattr(self, '_atualizando_idioma', False):
            self.progress_regeneracao = QProgressDialog(
                self.loc.get_text("updating_charts") if self.loc else "Atualizando gráficos...",
                self.loc.get_text("cancel") if self.loc else "Cancelar",
                0, len(graficos_para_atualizar),
                self.dialog_estatisticas
            )
            self.progress_regeneracao.setWindowTitle(self.loc.get_text("please_wait") if self.loc else "Aguarde")
            self.progress_regeneracao.setModal(False)
            self.progress_regeneracao.setMinimumDuration(0)
            self.progress_regeneracao.setAutoClose(False)
            self.progress_regeneracao.canceled.connect(self._cancelar_regeneracao)

        QTimer.singleShot(50, self._regenerar_proximo_grafico)

    except Exception as e:
        logger.error(f"Erro ao preparar regeneração de gráficos: {e}", exc_info=True)

def _regenerar_proximo_grafico(self):
    try:
        if self.indice_regeneracao_atual >= len(self.graficos_para_regenerar):
            if hasattr(self, 'progress_regeneracao') and self.progress_regeneracao:
                self.progress_regeneracao.close()

            return

        grafico_info = self.graficos_para_regenerar[self.indice_regeneracao_atual]
        i = grafico_info['index']
        grafico_atualizado = grafico_info['grafico']

        if hasattr(self, 'progress_regeneracao') and self.progress_regeneracao:
            self.progress_regeneracao.setValue(self.indice_regeneracao_atual)
            self.progress_regeneracao.setLabelText(f"{self.loc.get_text('updating_chart') if self.loc else 'Atualizando gráfico'}: {grafico_atualizado['titulo']}")
            QApplication.processEvents()

        try:
            QApplication.processEvents()

            if hasattr(grafico_atualizado["func"].__self__, 'atualizar_textos_traduzidos'):
                grafico_atualizado["func"].__self__.atualizar_textos_traduzidos()

            nova_fig = grafico_atualizado["func"]()
            novo_titulo = grafico_atualizado["func"].__self__.loc.get_text(grafico_atualizado["titulo"]) \
                if hasattr(grafico_atualizado["func"].__self__.loc, 'get_text') else grafico_atualizado["titulo"]

            self.graficos_dados[novo_titulo] = {
                'fig': nova_fig, 
                'func': grafico_atualizado["func"], 
                'titulo': novo_titulo
            }

            titulo_antigo = grafico_info['titulo_atual']
            if titulo_antigo != novo_titulo and titulo_antigo in self.graficos_dados:
                del self.graficos_dados[titulo_antigo]

            novo_canvas = FigureCanvas(nova_fig)
            QApplication.processEvents()

            tab_atual = self.tab_widget.widget(i)
            if tab_atual:
                layout_atual = tab_atual.layout()
                if layout_atual:
                    while layout_atual.count():
                        child = layout_atual.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()

                    layout_atual.addWidget(novo_canvas)

                else:
                    novo_layout = QVBoxLayout()
                    novo_layout.addWidget(novo_canvas)
                    tab_atual.setLayout(novo_layout)

            self.tab_widget.setTabText(i, novo_titulo)
            QApplication.processEvents()

        except Exception as e:
            logger.error(f"Erro ao regenerar gráfico {grafico_atualizado['titulo']}: {e}", exc_info=True)
            if not getattr(self, '_atualizando_idioma', False):
                QMessageBox.warning(
                    self.dialog_estatisticas, 
                    self.loc.get_text("error") if self.loc else "Erro", 
                    f"{self.loc.get_text('error_updating_chart') if self.loc else 'Erro ao atualizar gráfico'} {grafico_atualizado['titulo']}: {str(e)}"
                )

        self.indice_regeneracao_atual += 1
        QTimer.singleShot(50 if not getattr(self, '_atualizando_idioma', False) else 10, self._regenerar_proximo_grafico)

    except Exception as e:
        logger.error(f"Erro durante regeneração de gráfico: {e}", exc_info=True)
        self.indice_regeneracao_atual += 1
        QTimer.singleShot(50 if not getattr(self, '_atualizando_idioma', False) else 10, self._regenerar_proximo_grafico)

def _cancelar_regeneracao(self):
    try:
        self.indice_regeneracao_atual = len(self.graficos_para_regenerar)
        if hasattr(self, 'progress_regeneracao') and self.progress_regeneracao:
            self.progress_regeneracao.close()

    except Exception as e:
        logger.error(f"Erro ao cancelar regeneração: {e}", exc_info=True)
