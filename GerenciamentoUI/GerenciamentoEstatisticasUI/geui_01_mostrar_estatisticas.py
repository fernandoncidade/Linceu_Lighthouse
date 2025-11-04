import os
import sys
import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QMessageBox, QApplication, QSplitter)
from utils.LogManager import LogManager
from utils.IconUtils import get_icon_path

logger = LogManager.get_logger()

def mostrar_estatisticas(self):
    statistics_icon_path = get_icon_path("statistics.ico")
    salvar_icon_path = get_icon_path("salvar.ico")
    logger.debug(f"Caminho do ícone de estatísticas: {statistics_icon_path}")
    logger.debug(f"Caminho do ícone de salvar: {salvar_icon_path}")
    logger.debug(f"Arquivo de ícone de estatísticas existe? {os.path.exists(statistics_icon_path)}")
    logger.debug(f"Arquivo de ícone de salvar existe? {os.path.exists(salvar_icon_path)}")

    try:
        if self.dialog_estatisticas and self.dialog_estatisticas.isVisible():
            self.dialog_estatisticas.raise_()
            self.dialog_estatisticas.activateWindow()
            return

        logger.info("Gerando estatísticas")

        try:
            with sqlite3.connect(self.evento_base.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM monitoramento")
                count = cursor.fetchone()[0]

                if count == 0:
                    logger.warning("Não há dados para gerar estatísticas")
                    QMessageBox.warning(self.interface, self.loc.get_text("warning"), self.loc.get_text("no_data_to_plot"))
                    return

        except Exception as e:
            logger.error(f"Erro ao verificar quantidade de dados: {e}", exc_info=True)
            QMessageBox.critical(self.interface, self.loc.get_text("error"), f"{self.loc.get_text('stats_error')}: {str(e)}")
            return

        self.dialog_estatisticas = QDialog(None)  
        self.dialog_estatisticas.setWindowFlags(
            Qt.Window |                   
            Qt.WindowSystemMenuHint |     
            Qt.WindowMinMaxButtonsHint |  
            Qt.WindowCloseButtonHint      
        )
        self.dialog_estatisticas.finished.connect(self.limpar_referencia_dialog)

        estatisticas_icon = get_icon_path("statistics.ico")
        self.dialog_estatisticas.setWindowIcon(QIcon(estatisticas_icon))
        self.dialog_estatisticas.setWindowTitle(self.loc.get_text("statistics"))
        self.dialog_estatisticas.setMinimumSize(1000, 700)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal)

        from Estatistica.st_01_GeradorEstatisticas import GeradorEstatisticas
        self.gerador_atual = GeradorEstatisticas(self.evento_base.db_path, self.loc, self.interface)
        gerador = self.gerador_atual

        graficos = self._criar_lista_graficos(gerador)

        self.painel_selecao = self._criar_painel_selecao(graficos)
        self.splitter.addWidget(self.painel_selecao)

        graphics_panel = self._criar_painel_graficos()
        self.splitter.addWidget(graphics_panel)

        largura_painel = self.painel_selecao.width()
        self.splitter.setSizes([largura_painel, 700])

        main_layout.addWidget(self.splitter)
        self.dialog_estatisticas.setLayout(main_layout)

        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:
            logger.debug("Obtendo dados para estatísticas")
            df = gerador._obter_dados()

            if df.empty:
                logger.warning("DataFrame vazio, não é possível gerar gráficos")
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(self.interface, self.loc.get_text("warning"), self.loc.get_text("no_data_to_plot"))
                return

            self._popular_checkboxes(graficos)
            self.dialog_estatisticas.show()
            QApplication.restoreOverrideCursor()
            self._gerar_todos_graficos(graficos)
            logger.info("Dialog de estatísticas criado com sucesso")

        finally:
            QApplication.restoreOverrideCursor()

        self.dialog_estatisticas.show()

    except Exception as e:
        QApplication.restoreOverrideCursor()
        logger.error(f"Erro ao mostrar estatísticas: {e}", exc_info=True)
        QMessageBox.critical(self.interface, self.loc.get_text("error"), self.loc.get_text("stats_error").format(str(e)))
