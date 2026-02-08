from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class AjudaDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        try:
            self.setWindowFlags(
                Qt.Window
                | Qt.WindowTitleHint
                | Qt.WindowSystemMenuHint
                | Qt.WindowMinimizeButtonHint
                | Qt.WindowMaximizeButtonHint
                | Qt.WindowCloseButtonHint
            )
            self.setModal(False)
            self._parent = parent
            self._loc = getattr(parent, 'loc', None)

            layout = QVBoxLayout(self)
            layout.setContentsMargins(6, 6, 6, 6)

            self.browser = QTextBrowser(self)
            self.browser.setOpenExternalLinks(True)
            layout.addWidget(self.browser)

            footer = QWidget(self)
            footer_layout = QHBoxLayout(footer)
            footer_layout.addStretch()
            btn_ok = QPushButton(self.tr('OK'), self)
            btn_ok.clicked.connect(self.close)
            footer_layout.addWidget(btn_ok)
            layout.addWidget(footer)

            self._btn_ok = btn_ok

            self.resize(640, 360)

            try:
                loc = self._loc
                if loc is not None and hasattr(loc, 'idioma_alterado'):
                    loc.idioma_alterado.connect(self._on_idioma_alterado)

            except Exception:
                pass

            self._build_content()

        except Exception as e:
            logger.error(f"Erro ao inicializar AjudaDialog: {e}", exc_info=True)

    def _t(self, key, default):
        try:
            if self._loc is not None and hasattr(self._loc, 'get_text'):
                return self._loc.get_text(key) or default

        except Exception:
            pass

        return default

    def _build_content(self):
        try:
            t = self._t

            atalhos = [
                ("F1", t("help", "Ajuda") + ": " + t("help_description", "Exibe a lista de atalhos e descrições.")),
                ("Ctrl+M", t("manual", "Manual") + ": " + t("open_manual", "Abre o manual da aplicação.")),
                ("Ctrl+I", t("about", "Sobre") + ": " + t("open_about", "Exibe informações sobre o aplicativo.")),
                ("Ctrl+A", t("select_all_columns", "Selecionar todas colunas") + ": " + t("select_all_columns_desc", "Marca todas as colunas visíveis.")),
                ("Ctrl+Shift+A", t("select_all_columns", "Selecionar todas colunas") + " (" + t("color_columns", "Colunas coloridas") + "): " + t("select_all_columns_colors_desc", "Seleciona todas nas configurações de coloração de colunas.")),
                ("Ctrl+O", t("sort_rows", "Ordenar linhas") + ": " + t("toggle_sort_rows_desc", "Ativa/desativa ordenação automática das linhas.")),
                ("Ctrl+T", t("performance_charts", "Gráficos de desempenho") + ": " + t("toggle_performance_desc", "Alterna a exibição de gráficos de desempenho.")),
                ("Ctrl+Shift+O", t("select_dir", "Selecionar diretório") + " " + t("select_dir_desc", "Abre diálogo para selecionar diretório.")),
                ("Ctrl+R", t("start_stop", "Iniciar/Parar") + " " + t("start_stop_desc", "Inicia ou para a análise do diretório.")),
                ("Ctrl+P", t("pause_analysis", "Pausar análise") + " " + t("pause_analysis_desc", "Pausa/retoma o monitoramento ou escaneamento.")),
                ("Ctrl+Shift+S", t("save_as", "Salvar como") + " " + t("save_as_desc", "Abre diálogo para salvar dados com outro nome.")),
                ("Ctrl+S", t("save", "Salvar") + " " + t("save_desc", "Salva os dados atuais.")),
                ("Ctrl+G", t("statistics", "Estatísticas") + " " + t("statistics_desc", "Exibe estatísticas do projeto.")),
                ("Ctrl+L", t("clear_data", "Limpar dados") + " " + t("clear_data_desc", "Limpa os dados carregados.")),
                ("Ctrl+Q", t("exit", "Sair") + ": " + t("exit_desc", "Encerra a aplicação.")),
            ]

            html_lines = [f"<h3>{t('keyboard_shortcuts', 'Atalhos de teclado')}</h3>", "<table cellpadding=6>"]
            for key, desc in atalhos:
                html_lines.append(f"<tr><td><b>{key}</b></td><td>{desc}</td></tr>")

            html_lines.append("</table>")
            html = "\n".join(html_lines)

            titulo = t("help", "Ajuda")

            try:
                self.setWindowTitle(titulo)

            except Exception:
                pass

            try:
                self._btn_ok.setText(self.tr('OK'))

            except Exception:
                pass

            self.browser.setHtml(html)

        except Exception as e:
            logger.error(f"Erro ao construir conteúdo AjudaDialog: {e}", exc_info=True)

    def _on_idioma_alterado(self, novo_idioma: str):
        try:
            self._loc = getattr(self._parent, 'loc', None)
            self._build_content()

        except Exception:
            pass

def _exibir_ajuda(self):
    try:
        dialog = AjudaDialog(None)

        try:
            dialog._parent = self.interface
            dialog._loc = getattr(self, 'loc', None)
            if getattr(self, 'loc', None) is not None and hasattr(self.loc, 'idioma_alterado') and hasattr(dialog, '_on_idioma_alterado'):
                self.loc.idioma_alterado.connect(dialog._on_idioma_alterado)

        except Exception:
            pass

        self.interface._ajuda_dialog = dialog
        self.interface._ajuda_dialog.show()

    except Exception as e:
        logger.error(f"Erro ao exibir Ajuda: {e}", exc_info=True)
