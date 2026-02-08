from PySide6.QtWidgets import QAbstractItemView, QPushButton
from PySide6.QtCore import Qt, QTimer
from utils.LogManager import LogManager
import concurrent.futures
logger = LogManager.get_logger()

def configurar_tabela(self, tabela_dados):
    try:
        if tabela_dados is None:
            logger.error("Tabela de dados é None, não é possível configurar")
            return

        tabela_dados.setAlternatingRowColors(True)
        ordenacao_habilitada = getattr(self.interface, '_ordenacao_linhas_habilitada', False)
        tabela_dados.setSortingEnabled(ordenacao_habilitada)
        tabela_dados.setSelectionBehavior(QAbstractItemView.SelectItems)
        tabela_dados.setSelectionMode(QAbstractItemView.ExtendedSelection)
        tabela_dados.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tabela_dados.setCornerButtonEnabled(True)
        if not hasattr(self, '_selection_executor') or self._selection_executor is None:
            self._selection_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="Selection")
            self._selection_future = None

        if not hasattr(self, '_debounce_timer') or self._debounce_timer is None:
            self._debounce_timer = QTimer()
            self._debounce_timer.setSingleShot(True)

        def selecionar_todas_celulas():
            try:
                if hasattr(self, '_selection_future') and self._selection_future and not self._selection_future.done():
                    self._selection_future.cancel()

                tabela_dados.blockSignals(True)
                tabela_dados.selectAll()
                tabela_dados.blockSignals(False)
                if self._selection_executor:
                    self._selection_future = self._selection_executor.submit(self._processar_selecao_background)

            except Exception as e:
                logger.error(f"Erro ao selecionar todas as células: {e}", exc_info=True)
                tabela_dados.blockSignals(False)

        def selecionar_coluna_completa(logical_index):
            try:
                if hasattr(self, '_selection_future') and self._selection_future and not self._selection_future.done():
                    self._selection_future.cancel()

                tabela_dados.blockSignals(True)
                tabela_dados.selectColumn(logical_index)
                tabela_dados.blockSignals(False)
                if self._selection_executor:
                    self._selection_future = self._selection_executor.submit(self._processar_selecao_background)

            except Exception as e:
                logger.error(f"Erro ao selecionar coluna {logical_index}: {e}", exc_info=True)
                tabela_dados.blockSignals(False)

        corner_button = tabela_dados.findChild(QPushButton)
        if corner_button:
            try:
                corner_button.clicked.disconnect()

            except (TypeError, RuntimeError):
                pass

            corner_button.clicked.connect(selecionar_todas_celulas)

        tabela_dados.setStyleSheet("""
            QTableWidget::item:hover {
                background-color: palette(alternate-base);
                color: palette(text);
            }
            QTableWidget {
                selection-background-color: transparent;
                selection-color: palette(text);
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: palette(text);
                border: 1px solid palette(highlight);
                border-radius: 3px;
                padding: 1px;
            }
            QTableCornerButton::section {
                background-color: palette(button);
                border: 1px solid palette(mid);
            }
            QTableCornerButton::section:pressed {
                background-color: palette(highlight);
            }
        """)

        from PySide6.QtWidgets import QApplication
        palette = QApplication.palette()
        tabela_dados.setPalette(palette)
        header_horizontal = tabela_dados.horizontalHeader()
        header_horizontal.setSectionsMovable(True)
        header_horizontal.setHighlightSections(True)
        header_horizontal.setDefaultAlignment(Qt.AlignCenter)
        header_horizontal.setTextElideMode(Qt.ElideNone)
        header_horizontal.setStretchLastSection(False)
        font = header_horizontal.font()
        font.setBold(True)
        header_horizontal.setFont(font)
        try:
            receivers = header_horizontal.receivers(header_horizontal.sectionClicked)
            if receivers > 0:
                header_horizontal.sectionClicked.disconnect()

        except (TypeError, RuntimeError):
            pass

        header_horizontal.sectionClicked.connect(selecionar_coluna_completa)
        colunas_disponiveis = [(key, col) for key, col in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"])]
        tabela_dados.setColumnCount(len(colunas_disponiveis))
        self.texto_original_cabecalhos = {}
        headers = []
        for i, (key, coluna) in enumerate(colunas_disponiveis):
            texto = coluna["nome"]
            self.texto_original_cabecalhos[i] = texto
            headers.append(texto)

        tabela_dados.setHorizontalHeaderLabels(headers)
        for i, (key, coluna) in enumerate(colunas_disponiveis):
            tabela_dados.setColumnHidden(i, not coluna["visivel"])

        header_horizontal.sectionResized.connect(self.redimensionar_cabecalho)
        try:
            tabela_dados.itemSelectionChanged.disconnect()

        except (TypeError, RuntimeError):
            pass

        def ajustar_cor_selecao_debounced():
            try:
                if hasattr(self, '_debounce_timer') and self._debounce_timer is not None:
                    if self._debounce_timer.isActive():
                        self._debounce_timer.stop()

                    self._debounce_timer = QTimer()
                    self._debounce_timer.setSingleShot(True)
                    if self._selection_executor:
                        self._debounce_timer.timeout.connect(lambda: self._selection_executor.submit(self._processar_selecao_background))
                        self._debounce_timer.start(50)

            except Exception as e:
                logger.error(f"Erro no debounce de seleção: {e}", exc_info=True)

        tabela_dados.itemSelectionChanged.connect(ajustar_cor_selecao_debounced)
        if not hasattr(self, '_cores_originais_cache'):
            self._cores_originais_cache = {}

        self.ajustar_larguras_colunas(tabela_dados, colunas_disponiveis)
        self.aplicar_quebra_linha_todos_cabecalhos(tabela_dados)
        self._invalidar_cache_cores()
        self.atualizar_dados_tabela(tabela_dados)
        tabela_dados.viewport().update()
        QApplication.processEvents()
        if hasattr(self, 'aplicar_cores_todas_colunas_processamento'):
            QTimer.singleShot(100, lambda: self.aplicar_cores_todas_colunas_processamento({'inicializacao': True}))

    except Exception as e:
        logger.error(f"Erro ao configurar tabela: {e}", exc_info=True)

def _processar_selecao_background(self):
    try:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self.ajustar_cor_selecao)
        return True

    except Exception as e:
        logger.error(f"Erro no processamento background de seleção: {e}", exc_info=True)
        return False
