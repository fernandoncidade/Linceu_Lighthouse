import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSplitter
from PySide6.QtCore import Qt, QObject, QEvent
from source.utils.IconUtils import get_icon_path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class Configurador:
    @staticmethod
    def setup_ui(interface):
        try:
            widget_central = QWidget()
            icon_file = get_icon_path("file_manager4.ico")
            if not os.path.exists(icon_file):
                logger.error(f"Ícone principal não encontrado: {icon_file}")

            interface.setWindowTitle(interface.loc.get_text("window_title"))
            interface.setWindowIcon(QIcon(icon_file))
            interface.setCentralWidget(widget_central)
            interface.setGeometry(100, 100, 900, 500)

            splitter_principal = QSplitter(Qt.Horizontal, widget_central)
            splitter_lateral = QSplitter(Qt.Vertical)

            try:
                interface.gerenciador_desempenho = None
                widget_desempenho = QWidget()

            except Exception as e:
                logger.error(f"Erro ao preparar área de desempenho: {e}", exc_info=True)
                widget_desempenho = QWidget()

            layout_lateral_inferior = QVBoxLayout()
            layout_lateral_inferior.setContentsMargins(10, 10, 10, 10)
            layout_lateral_inferior.setSpacing(8)

            container_botoes = QWidget()
            container_botoes.setLayout(layout_lateral_inferior)
            container_botoes.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            container_botoes.setMaximumHeight(200)

            interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("select_dir"), 'selecione.ico', interface.selecionar_diretorio, icon_file, "select_dir")
            interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("start_stop"), 'analyze.ico', interface.alternar_analise_diretorio, icon_file, "start_stop")
            interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("pause_analysis"), 'pause2.ico', interface.gerenciador_botoes.pausar_monitoramento_ou_escaneamento, icon_file, "pause_analysis")
            interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("save_as"), 'save_as.ico', interface.abrir_salvar_como, icon_file, "save_as")
            interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("statistics"), 'statistics.ico', interface.mostrar_estatisticas, icon_file, "statistics")
            interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("clear_data"), 'clear.ico', interface.limpar_dados, icon_file, "clear_data")

            splitter_lateral.addWidget(widget_desempenho)
            splitter_lateral.addWidget(container_botoes)
            splitter_lateral.setStretchFactor(0, 7)
            splitter_lateral.setStretchFactor(1, 1)
            interface.splitter_lateral = splitter_lateral
            interface.widget_desempenho = widget_desempenho

            layout_conteudo = QVBoxLayout()
            container_conteudo = QWidget()
            container_conteudo.setLayout(layout_conteudo)

            interface.rotulo_diretorio = QLabel(interface.loc.get_text("no_dir"))
            interface.rotulo_resultado = QLabel(interface.loc.get_text("select_to_start"))

            layout_info_h = QHBoxLayout()
            layout_info_h.addWidget(interface.rotulo_resultado, 1)

            interface.loc.idioma_alterado.connect(lambda _: interface.atualizar_status())
            interface.barra_progresso = QProgressBar(interface)
            interface.barra_progresso.setMaximum(100)
            interface.barra_progresso.setMinimum(0)
            interface.barra_progresso.setValue(0)
            interface.barra_progresso.setTextVisible(True)
            interface.barra_progresso.setFormat("%p%")
            interface.barra_progresso.setFixedHeight(20)
            interface.barra_progresso.hide()

            info_widget = QWidget()
            info_layout = QVBoxLayout(info_widget)
            info_layout.setContentsMargins(0, 0, 0, 0)
            info_layout.setSpacing(4)
            info_layout.addWidget(interface.rotulo_diretorio)
            info_layout.addLayout(layout_info_h)
            info_layout.addWidget(interface.barra_progresso)

            content_splitter = QSplitter(Qt.Vertical)
            content_splitter.addWidget(info_widget)
            content_splitter.addWidget(interface.tabela_dados)
            content_splitter.setStretchFactor(0, 0)
            content_splitter.setStretchFactor(1, 1)
            info_widget.setMaximumHeight(160)

            layout_conteudo.addWidget(content_splitter)

            splitter_principal.addWidget(splitter_lateral)
            splitter_principal.addWidget(container_conteudo)
            splitter_principal.setStretchFactor(0, 0)
            splitter_principal.setStretchFactor(1, 1)

            layout_wrapper = QHBoxLayout(widget_central)
            layout_wrapper.setContentsMargins(0, 0, 0, 0)
            layout_wrapper.addWidget(splitter_principal)

            interface.atualizar_status()

            try:
                if not hasattr(interface, "desempenho_ativo"):
                    interface.desempenho_ativo = False

                class _WindowStateFilter(QObject):
                    def __init__(self, iface):
                        super().__init__(iface)
                        self.iface = iface

                    def eventFilter(self, obj, event):
                        try:
                            if obj is self.iface and event.type() == QEvent.WindowStateChange:
                                if not self.iface.isMaximized() and not self.iface.isFullScreen():
                                    if getattr(self.iface, "desempenho_ativo", False):
                                        self.iface.setGeometry(100, 100, 1300, 800)

                                    else:
                                        self.iface.setGeometry(100, 100, 900, 500)

                        except Exception as e:
                            logger.error(f"Erro no filtro de estado da janela: {e}", exc_info=True)

                        return False

                interface._window_state_filter = _WindowStateFilter(interface)
                interface.installEventFilter(interface._window_state_filter)

            except Exception as e:
                logger.error(f"Erro ao instalar filtro de estado da janela: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao configurar interface principal: {e}", exc_info=True)

    @staticmethod
    def setup_menu_bar(interface):
        try:
            interface.gerenciador_menus_ui.criar_menu_principal()

        except Exception as e:
            logger.error(f"Erro ao configurar barra de menu: {e}", exc_info=True)
