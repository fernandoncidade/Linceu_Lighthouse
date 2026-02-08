from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QGridLayout, QFrame, QWidget, QTabWidget,
                               QColorDialog)
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()


class BotaoCor(QPushButton):
    def __init__(self, cor, tamanho=30):
        super().__init__()
        self.cor = cor
        self.setFixedSize(tamanho, tamanho)
        self.setStyleSheet(f"background-color: {cor}; border: 1px solid #888888;")
        self.setToolTip(cor)


class DialogoPaletaCores(QDialog):
    corSelecionada = Signal(QColor)

    def __init__(self, cor_atual, interface_principal, titulo=None, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        self.setModal(False)

        logger = LogManager.get_logger()
        logger.debug(f"Iniciando DialogoPaletaCores com cor inicial: {cor_atual.name()}")

        self.interface = interface_principal

        try:
            if hasattr(interface_principal, 'loc'):
                self.loc = interface_principal.loc
                logger.debug("Usando localizador da interface principal")

            else:
                from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
                self.loc = LocalizadorQt()
                logger.debug("Criando novo localizador para o diálogo")

        except Exception as e:
            logger.error(f"Erro ao obter localizador: {e}", exc_info=True)
            from GerenciamentoUI.ui_12_LocalizadorQt import LocalizadorQt
            self.loc = LocalizadorQt()

        if titulo is None:
            titulo = self.loc.get_text("select_color")

        logger.debug(f"Configurando diálogo de cores com título: {titulo}")
        self.setWindowTitle(titulo)

        self.cor_atual = cor_atual
        self.cor_selecionada = None
        self.setup_ui()

    def setup_ui(self):
        logger = LogManager.get_logger()
        logger.debug("Configurando interface do diálogo de cores")

        try:
            layout_principal = QVBoxLayout(self)

            layout_preview = QHBoxLayout()
            self.preview_atual = QFrame(self)
            self.preview_atual.setFixedSize(50, 50)
            self.preview_atual.setFrameStyle(QFrame.Box | QFrame.Plain)
            self.preview_atual.setLineWidth(1)
            self.preview_atual.setStyleSheet(f"background-color: {self.cor_atual.name()};")

            self.preview_nova = QFrame(self)
            self.preview_nova.setFixedSize(50, 50)
            self.preview_nova.setFrameStyle(QFrame.Box | QFrame.Plain)
            self.preview_nova.setLineWidth(1)
            self.preview_nova.setStyleSheet(f"background-color: {self.cor_atual.name()};")

            layout_preview.addWidget(QLabel(f"{self.loc.get_text('current')}:"))
            layout_preview.addWidget(self.preview_atual)
            layout_preview.addSpacing(20)
            layout_preview.addWidget(QLabel(f"{self.loc.get_text('new')}:"))
            layout_preview.addWidget(self.preview_nova)
            layout_preview.addStretch(1)

            layout_principal.addLayout(layout_preview)

            tab_widget = QTabWidget(self)

            tab_basicas = QWidget()
            layout_basicas = QVBoxLayout(tab_basicas)

            cores_basicas = [
                "#000000", "#404040", "#808080", "#C0C0C0", "#FFFFFF", "#FF6200",
                "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF",
                "#800000", "#008000", "#000080", "#808000", "#008080", "#800080",
                "#FF8080", "#80FF80", "#8080FF", "#FFFF80", "#80FFFF", "#FF80FF",
                "#A52A2A", "#D2691E", "#CD853F", "#F4A460", "#8B4513", "#A0522D",
                "#B8860B", "#DAA520", "#BDB76B", "#6B8E23", "#556B2F", "#2E8B57",
                "#3CB371", "#20B2AA", "#5F9EA0", "#4682B4", "#4169E1", "#483D8B",
                "#6A5ACD", "#7B68EE", "#9370DB", "#4B0082", "#8A2BE2", "#9400D3",
                "#191970", "#003366", "#006400", "#2F4F4F", "#696969", "#708090",
                "#778899", "#8FBC8F", "#BC8F8F", "#CD5C5C", "#DC143C", "#B22222",
                "#FFA07A", "#D2B48C", "#7B3F00"
            ]

            grid_basicas = QGridLayout()
            self._adicionar_grid_cores(grid_basicas, cores_basicas, 7)
            layout_basicas.addLayout(grid_basicas)
            tab_widget.addTab(tab_basicas, self.loc.get_text("basics"))

            tab_pasteis = QWidget()
            layout_pasteis = QVBoxLayout(tab_pasteis)

            cores_pasteis = [
                "#FFE4E1", "#F0FFF0", "#E6E6FA", "#FFF8DC", "#FFFACD", "#FFE4B5",
                "#FFDAB9", "#FFC0CB", "#FFB6C1", "#FFE4C4", "#F5F5DC", "#F0FFFF",
                "#F5FFFA", "#F8F8FF", "#FFFFF0", "#F0F8FF", "#E0FFFF", "#F5F5F5",
                "#FFF0F5", "#FAF0E6", "#FDF5E6", "#FAEBD7", "#FFEFD5", "#FFEBCD",
                "#FFE4C4", "#FFDEAD", "#EEE8AA", "#F0E68C", "#E0EEE0", "#D8BFD8",
                "#DDA0DD", "#EE82EE", "#DA70D6", "#D8BFD8", "#E6E6FA", "#B0E0E6",
                "#ADD8E6", "#B0C4DE", "#AFEEEE", "#E0FFFF", "#E6C8FF", "#F5E6FF",
                "#F0E6FF", "#E6F0FF", "#E6FFF0", "#F0FFE6", "#FFE6F0", "#FFE6E6",
                "#E6FFE6", "#E6E6FF", "#FFE6FF", "#FFF5E6", "#F5FFE6", "#E6FFF5",
                "#F8F0FF", "#FFF0F8", "#F0FFF8", "#F8FFF0", "#E6F5FF", "#FFE6F5",
                "#FFE6C8", "#C8FFE6", "#E6C8FF"
            ]

            grid_pasteis = QGridLayout()
            self._adicionar_grid_cores(grid_pasteis, cores_pasteis, 7)
            layout_pasteis.addLayout(grid_pasteis)
            tab_widget.addTab(tab_pasteis, self.loc.get_text("pastels"))

            tab_vibrantes = QWidget()
            layout_vibrantes = QVBoxLayout(tab_vibrantes)

            cores_vibrantes = [
                "#FF0000", "#FF4500", "#FF6347", "#FF7F50", "#FF8C00", "#FFA500",
                "#FFD700", "#FFFF00", "#ADFF2F", "#7FFF00", "#00FF00", "#32CD32",
                "#00FA9A", "#00FFFF", "#1E90FF", "#0000FF", "#8A2BE2", "#FF00FF",
                "#C71585", "#FF1493", "#FF69B4", "#FF0066", "#FF3366", "#FF00CC",
                "#CC00FF", "#9900FF", "#6600FF", "#001AFF", "#00B3FF", "#FF33FF",
                "#0033FF", "#0099FF", "#00CCFF", "#00FFCC", "#00FF66", "#33FF00",
                "#99FF00", "#CCFF00", "#FFCC00", "#FF9900", "#FF6600", "#FF5000",
                "#FF0033", "#E100FF", "#FF1A00", "#FF00B3", "#B300FF", "#5500FF",
                "#00FFB3", "#00FF1A", "#B3FF00", "#FF5500", "#FF0055", "#AA00FF",
                "#007FFF", "#00FFAA", "#7FFF00", "#FFAA00", "#FF007F", "#3F00FF",
                "#00FF3F", "#FF3F00", "#FF3F33"
            ]

            grid_vibrantes = QGridLayout()
            self._adicionar_grid_cores(grid_vibrantes, cores_vibrantes, 7)
            layout_vibrantes.addLayout(grid_vibrantes)
            tab_widget.addTab(tab_vibrantes, self.loc.get_text("vibrant"))

            layout_principal.addWidget(tab_widget)

            btn_avancado = QPushButton(self.loc.get_text("advanced_color_picker"))
            btn_avancado.clicked.connect(self._abrir_seletor_avancado)
            layout_principal.addWidget(btn_avancado)

            layout_botoes = QHBoxLayout()
            btn_ok = QPushButton(self.loc.get_text("ok"))
            btn_ok.clicked.connect(self.accept)
            btn_cancelar = QPushButton(self.loc.get_text("cancel"))
            btn_cancelar.clicked.connect(self.reject)

            layout_botoes.addStretch(1)
            layout_botoes.addWidget(btn_ok)
            layout_botoes.addWidget(btn_cancelar)
            layout_principal.addLayout(layout_botoes)

            self.setLayout(layout_principal)
            self.resize(400, 500)

            logger.debug("Interface do diálogo de cores configurada com sucesso")

        except Exception as e:
            logger.error(f"Erro ao configurar interface do diálogo de cores: {e}", exc_info=True)
            raise

    def _adicionar_grid_cores(self, grid_layout, lista_cores, colunas):
        logger = LogManager.get_logger()
        try:
            row, col = 0, 0
            for cor_hex in lista_cores:
                botao = BotaoCor(cor_hex)
                botao.clicked.connect(lambda checked=False, c=cor_hex: self._selecionar_cor(c))
                grid_layout.addWidget(botao, row, col)

                col += 1
                if col >= colunas:
                    col = 0
                    row += 1

            logger.debug(f"Grade de cores adicionada com {len(lista_cores)} cores")

        except Exception as e:
            logger.error(f"Erro ao adicionar grade de cores: {e}", exc_info=True)

    def _selecionar_cor(self, cor_hex):
        logger = LogManager.get_logger()
        try:
            cor = QColor(cor_hex)
            self.preview_nova.setStyleSheet(f"background-color: {cor_hex};")
            self.cor_selecionada = cor
            logger.debug(f"Cor selecionada: {cor_hex}")

        except Exception as e:
            logger.error(f"Erro ao selecionar cor {cor_hex}: {e}", exc_info=True)

    def _abrir_seletor_avancado(self):
        logger = LogManager.get_logger()
        logger.debug("Abrindo seletor avançado de cores")

        try:
            from PySide6.QtCore import QLocale, QTranslator
            from PySide6.QtWidgets import QApplication
            import os

            app = QApplication.instance()
            if app:
                locale_map = {
                    "pt_BR": "pt_BR",
                    "en_US": "en_US", 
                    "es_ES": "es_ES",
                    "fr_FR": "fr_FR",
                    "it_IT": "it_IT",
                    "de_DE": "de_DE"
                }

                locale_code = locale_map.get(self.loc.idioma_atual, "en_US")
                qt_locale = QLocale(locale_code)
                QLocale.setDefault(qt_locale)

                qt_translator = QTranslator()
                translations_paths = [
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations", "qt"),
                    "/usr/share/qt6/translations",
                    "C:/Qt/Tools/QtCreator/share/qtcreator/translations",
                ]

                for path in translations_paths:
                    if os.path.exists(path):
                        if qt_translator.load(qt_locale, "qtbase", "_", path):
                            app.installTranslator(qt_translator)
                            logger.debug(f"Tradutor Qt carregado de: {path}")
                            break

            dialogo = QColorDialog(self.cor_atual, self)
            dialogo.setWindowTitle(self.loc.get_text("advanced_color_picker"))
            dialogo.setOption(QColorDialog.ShowAlphaChannel, False)

            dialogo.setModal(False)
            dialogo.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)

            app.processEvents()

            if self.loc.idioma_atual != "en_US":
                logger.debug(f"Aplicando tradução manual para idioma: {self.loc.idioma_atual}")

                from PySide6.QtCore import QTimer
                timer = QTimer()
                timer.singleShot(50, lambda: self._traduzir_dialogo_cores(dialogo))

                self._traduzir_dialogo_cores(dialogo)

            dialogo.show()

            def on_color_selected(color):
                if color.isValid():
                    self.preview_nova.setStyleSheet(f"background-color: {color.name()};")
                    self.cor_selecionada = color
                    logger.debug(f"Cor selecionada no seletor avançado: {color.name()}")
                    dialogo.close()

            dialogo.colorSelected.connect(on_color_selected)

        except Exception as e:
            logger.error(f"Erro ao abrir seletor avançado de cores: {e}", exc_info=True)

    def accept(self):
        logger = LogManager.get_logger()
        try:
            if self.cor_selecionada and self.cor_selecionada.isValid():
                self.corSelecionada.emit(self.cor_selecionada)
                logger.debug(f"Cor confirmada e aplicada: {self.cor_selecionada.name()}")

            super().accept()

        except Exception as e:
            logger.error(f"Erro ao confirmar seleção de cor: {e}", exc_info=True)

    def _traduzir_dialogo_cores(self, dialogo):
        try:
            from PySide6.QtWidgets import QLabel, QPushButton, QGroupBox

            mapeamento_traducoes = {
                "Basic colors": self.loc.get_text("basic_colors"),
                "&Basic colors": self.loc.get_text("basic_colors"),
                "Custom colors": self.loc.get_text("custom_colors"),
                "&Custom colors": self.loc.get_text("custom_colors"),
                "Pick Screen Color": self.loc.get_text("pick_screen_color"),
                "&Pick Screen Color": self.loc.get_text("pick_screen_color"),
                "Add to Custom Colors": self.loc.get_text("add_to_custom_colors"),
                "&Add to Custom Colors": self.loc.get_text("add_to_custom_colors"),
                "Hue:": f"{self.loc.get_text('hue')}",
                "&Hue:": f"{self.loc.get_text('hue')}",
                "Hue": self.loc.get_text("hue"),
                "&Hue": self.loc.get_text("hue"),
                "Sat:": f"{self.loc.get_text('sat')}",
                "&Sat:": f"{self.loc.get_text('sat')}",
                "Sat": self.loc.get_text("sat"),
                "&Sat": self.loc.get_text("sat"),
                "Val:": f"{self.loc.get_text('val')}",
                "&Val:": f"{self.loc.get_text('val')}",
                "Val": self.loc.get_text("val"),
                "&Val": self.loc.get_text("val"),
                "Red:": f"{self.loc.get_text('red')}",
                "&Red:": f"{self.loc.get_text('red')}",
                "Red": self.loc.get_text("red"),
                "&Red": self.loc.get_text("red"),
                "Green:": f"{self.loc.get_text('green')}",
                "&Green:": f"{self.loc.get_text('green')}",
                "Green": self.loc.get_text("green"),
                "&Green": self.loc.get_text("green"),
                "Blue:": f"{self.loc.get_text('blue')}",
                "&Blue:": f"{self.loc.get_text('blue')}",
                "Blue": self.loc.get_text("blue"),
                "&Blue": self.loc.get_text("blue"),
                "HTML:": f"{self.loc.get_text('html')}",
                "&HTML:": f"{self.loc.get_text('html')}",
                "HTML": self.loc.get_text("html"),
                "&HTML": self.loc.get_text("html"),
                "OK": self.loc.get_text("ok"),
                "&OK": self.loc.get_text("ok"),
                "Cancel": self.loc.get_text("cancel"),
                "&Cancel": self.loc.get_text("cancel")
            }

            def normalizar(texto):
                return texto.strip().replace(":", "").replace("&", "")

            for label in dialogo.findChildren(QLabel):
                texto_original = label.text().strip()
                texto_norm = normalizar(texto_original)
                for chave, traducao in mapeamento_traducoes.items():
                    if normalizar(chave) == texto_norm:
                        label.setText(traducao if ":" not in texto_original else f"{traducao}:")
                        break

            for button in dialogo.findChildren(QPushButton):
                texto_original = button.text().strip()
                texto_norm = normalizar(texto_original)
                for chave, traducao in mapeamento_traducoes.items():
                    if normalizar(chave) == texto_norm:
                        button.setText(traducao)
                        break

            for groupbox in dialogo.findChildren(QGroupBox):
                texto_original = groupbox.title().strip()
                texto_norm = normalizar(texto_original)
                for chave, traducao in mapeamento_traducoes.items():
                    if normalizar(chave) == texto_norm:
                        groupbox.setTitle(traducao)
                        break

            elementos_por_nome = {
                "qt_colorname_label": self.loc.get_text("html"),
            }

            for nome, traducao in elementos_por_nome.items():
                elemento = dialogo.findChild(QLabel, nome)
                if elemento:
                    elemento.setText(f"{traducao}:")

            logger.debug("Tradução manual do diálogo de cores aplicada")

        except Exception as e:
            logger.error(f"Erro ao traduzir diálogo de cores: {e}", exc_info=True)

    def obter_cor(self):
        resultado = self.cor_selecionada if self.cor_selecionada else self.cor_atual
        LogManager.get_logger().debug(f"Retornando cor final: {resultado.name()}")
        return resultado
