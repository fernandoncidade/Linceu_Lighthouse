from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_estilo_tema(self, novo_tema):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados
        tema_anterior = getattr(self, '_ultimo_tema_aplicado', None)
        self._ultimo_tema_aplicado = novo_tema
        tabela.blockSignals(True)

        try:
            palette = QApplication.palette()
            tabela.setPalette(palette)

            tabela.setStyleSheet("""
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

            self._invalidar_cache_cores()
            self._forcar_reconstrucao_todas_celulas(novo_tema)
            if hasattr(self, 'aplicar_cores_todas_colunas_processamento'):
                self.aplicar_cores_todas_colunas_processamento({'mudanca_tema': True})

            if hasattr(self, 'ajustar_cor_selecao'):
                self.ajustar_cor_selecao()

            tabela.viewport().update()
            QApplication.processEvents()

        finally:
            tabela.blockSignals(False)

    except Exception as e:
        logger.error(f"Erro ao atualizar estilo do tema: {e}", exc_info=True)
        if hasattr(self.interface, 'tabela_dados'):
            self.interface.tabela_dados.blockSignals(False)

def _forcar_reconstrucao_todas_celulas(self, novo_tema):
    try:
        tabela = self.interface.tabela_dados
        palette = QApplication.palette()
        cor_fundo_padrao = palette.color(QPalette.ColorRole.Base)
        cor_alternativa = palette.color(QPalette.ColorRole.AlternateBase)
        cor_texto_claro = QColor(0, 0, 0)
        cor_texto_escuro = QColor(255, 255, 255)
        cor_texto_tema_atual = cor_texto_escuro if novo_tema == "escuro" else cor_texto_claro

        for row in range(tabela.rowCount()):
            for col in range(tabela.columnCount()):
                item = tabela.item(row, col)
                if not item:
                    continue

                cor_atual = item.background().color()
                if cor_atual.isValid() and cor_atual != QColor() and cor_atual.alpha() > 0:
                    nome_coluna = tabela.horizontalHeaderItem(col).text().replace('\n', ' ').strip()
                    key_coluna = None
                    for key, coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items():
                        if coluna["nome"].replace('\n', ' ').strip() == nome_coluna:
                            key_coluna = key
                            break

                    eh_personalizada = (
                        key_coluna in self.colunas_para_colorir or
                        key_coluna == "tipo_operacao" or
                        (hasattr(self, 'eh_coluna_personalizada_colorida') and 
                         self.eh_coluna_personalizada_colorida(key_coluna))
                    )

                    if eh_personalizada:
                        cor_texto = self.calcular_cor_texto_ideal(cor_atual, True)
                        item.setForeground(cor_texto)

                    elif self._eh_cor_padrao_qualquer_tema(cor_atual):
                        item.setForeground(cor_texto_tema_atual)
                        if row % 2 == 0:
                            item.setBackground(cor_fundo_padrao)

                        else:
                            item.setBackground(cor_alternativa)

                    else:
                        cor_texto = self.calcular_cor_texto_ideal(cor_atual, False)
                        item.setForeground(cor_texto)

                else:
                    item.setForeground(cor_texto_tema_atual)
                    if row % 2 == 0:
                        item.setBackground(cor_fundo_padrao)

                    else:
                        item.setBackground(cor_alternativa)

    except Exception as e:
        logger.error(f"Erro ao forçar reconstrução de células: {e}", exc_info=True)

def _atualizar_cores_celulas_incolores(self, novo_tema):
    try:
        tabela = self.interface.tabela_dados
        palette = QApplication.palette()
        cor_fundo_padrao = palette.color(QPalette.ColorRole.Base)
        cor_alternativa = palette.color(QPalette.ColorRole.AlternateBase)
        if novo_tema == "escuro":
            cor_texto_padrao = QColor(255, 255, 255)

        else:
            cor_texto_padrao = QColor(0, 0, 0)

        cor_texto_tema_oposto = QColor(0, 0, 0) if novo_tema == "escuro" else QColor(255, 255, 255)
        for row in range(tabela.rowCount()):
            for col in range(tabela.columnCount()):
                item = tabela.item(row, col)
                if item:
                    cor_atual = item.background().color()
                    cor_texto_atual = item.foreground().color()

                    texto_do_tema_oposto = (
                        (novo_tema == "escuro" and cor_texto_atual.red() == 0 and cor_texto_atual.green() == 0 and cor_texto_atual.blue() == 0) or
                        (novo_tema == "claro" and cor_texto_atual.red() == 255 and cor_texto_atual.green() == 255 and cor_texto_atual.blue() == 255)
                    )

                    if (not cor_atual.isValid() or 
                        cor_atual == QColor() or 
                        cor_atual.alpha() == 0 or
                        self._eh_cor_padrao_qualquer_tema(cor_atual) or
                        texto_do_tema_oposto):
                        item.setForeground(cor_texto_padrao)

                        if not cor_atual.isValid() or cor_atual == QColor() or cor_atual.alpha() == 0:
                            if row % 2 == 0:
                                item.setBackground(cor_fundo_padrao)

                            else:
                                item.setBackground(cor_alternativa)

                        elif self._eh_cor_padrao_qualquer_tema(cor_atual):
                            if row % 2 == 0:
                                item.setBackground(cor_fundo_padrao)

                            else:
                                item.setBackground(cor_alternativa)

    except Exception as e:
        logger.error(f"Erro ao atualizar células incolores: {e}", exc_info=True)

def _eh_cor_fundo_padrao(self, cor):
    try:
        palette = QApplication.palette()
        cor_base = palette.color(QPalette.ColorRole.Base)
        cor_alternativa = palette.color(QPalette.ColorRole.AlternateBase)
        cor_janela = palette.color(QPalette.ColorRole.Window)

        return (abs(cor.red() - cor_base.red()) < 10 and 
                abs(cor.green() - cor_base.green()) < 10 and 
                abs(cor.blue() - cor_base.blue()) < 10) or \
               (abs(cor.red() - cor_alternativa.red()) < 10 and 
                abs(cor.green() - cor_alternativa.green()) < 10 and 
                abs(cor.blue() - cor_alternativa.blue()) < 10) or \
               (abs(cor.red() - cor_janela.red()) < 10 and 
                abs(cor.green() - cor_janela.green()) < 10 and 
                abs(cor.blue() - cor_janela.blue()) < 10)

    except Exception as e:
        logger.error(f"Erro ao verificar cor padrão: {e}", exc_info=True)
        return False

def _eh_cor_padrao_qualquer_tema(self, cor):
    try:
        cores_tema_claro = [
            QColor(255, 255, 255),
            QColor(248, 248, 248),
            QColor(240, 240, 240),
            QColor(230, 230, 230),
            QColor(245, 245, 245)
        ]

        cores_tema_escuro = [
            QColor(32, 32, 32),
            QColor(43, 43, 43),
            QColor(30, 30, 30),
            QColor(37, 37, 37),
            QColor(25, 25, 25)
        ]

        for cor_tema in cores_tema_claro + cores_tema_escuro:
            if (abs(cor.red() - cor_tema.red()) < 15 and 
                abs(cor.green() - cor_tema.green()) < 15 and 
                abs(cor.blue() - cor_tema.blue()) < 15):
                return True

        return self._eh_cor_fundo_padrao(cor)

    except Exception as e:
        logger.error(f"Erro ao verificar cor padrão de qualquer tema: {e}", exc_info=True)
        return False
