import os
from utils.LogManager import LogManager
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from utils.IconUtils import get_icon_path


class Configurador:
    @staticmethod
    def setup_ui(interface):
        logger = LogManager.get_logger()
        logger.debug("Configurando interface principal")

        widget_central = QWidget()

        icon_file = get_icon_path("file_manager4.ico")
        if not os.path.exists(icon_file):
            logger.error(f"Ícone principal não encontrado: {icon_file}")

        interface.setWindowTitle(interface.loc.get_text("window_title"))
        interface.setWindowIcon(QIcon(icon_file))
        interface.setCentralWidget(widget_central)
        interface.setGeometry(100, 100, 900, 500)

        layout_principal = QHBoxLayout(widget_central)
        layout_lateral = QVBoxLayout()
        layout_lateral_inferior = QVBoxLayout()
        layout_lateral_inferior.addStretch(1)
        layout_lateral_inferior.setContentsMargins(10, 10, 10, 10)

        interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("select_dir"), 'selecione.ico', interface.selecionar_diretorio, icon_file, "select_dir")
        interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("start_stop"), 'analyze.ico', interface.alternar_analise_diretorio, icon_file, "start_stop")
        interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("save_as"), 'save_as.ico', interface.abrir_salvar_como, icon_file, "save_as")
        interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("statistics"), 'statistics.ico', interface.mostrar_estatisticas, icon_file, "statistics")
        interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("clear_data"), 'clear.ico', interface.limpar_dados, icon_file, "clear_data")

        # Botões novos
        # interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("start"), 'start.ico', interface.gerenciador_botoes.iniciar_monitoramento, icon_file, "start")
        # interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("scan"), 'scan.ico', interface.gerenciador_botoes.iniciar_escaneamento, icon_file, "scan")
        # interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("scan_star"), 'scan_star.ico', interface.gerenciador_botoes.iniciar_scan_e_monitoramento, icon_file, "scan_star")
        # interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("pause"), 'pause.ico', interface.gerenciador_botoes.pausar_monitoramento_ou_escaneamento, icon_file, "pause")
        # interface.gerenciador_botoes_ui.add_button_with_label(layout_lateral_inferior, interface.loc.get_text("stop"), 'stop.ico', interface.gerenciador_botoes.parar_monitoramento_ou_escaneamento, icon_file, "stop")

        layout_lateral.addLayout(layout_lateral_inferior)
        layout_conteudo = QVBoxLayout()

        interface.rotulo_diretorio = QLabel(interface.loc.get_text("no_dir"))
        interface.rotulo_resultado = QLabel(interface.loc.get_text("select_to_start"))

        layout_info = QHBoxLayout()
        layout_info.addWidget(interface.rotulo_resultado, 1)

        interface.loc.idioma_alterado.connect(lambda _: interface.atualizar_status())

        interface.barra_progresso = QProgressBar(interface)
        interface.barra_progresso.setMaximum(100)
        interface.barra_progresso.setMinimum(0)
        interface.barra_progresso.setValue(0)
        interface.barra_progresso.setTextVisible(True)
        interface.barra_progresso.setFormat("%p%")
        interface.barra_progresso.setFixedHeight(20)
        interface.barra_progresso.hide()

        layout_conteudo.addWidget(interface.rotulo_diretorio)
        layout_conteudo.addLayout(layout_info)
        layout_conteudo.addWidget(interface.barra_progresso)
        layout_conteudo.addWidget(interface.tabela_dados)

        layout_principal.addLayout(layout_lateral)
        layout_principal.addLayout(layout_conteudo, stretch=1)

        interface.atualizar_status()
        logger.debug("Interface principal configurada com sucesso")

    @staticmethod
    def setup_menu_bar(interface):
        logger = LogManager.get_logger()
        logger.debug("Configurando barra de menu")
        interface.gerenciador_menus_ui.criar_menu_principal()
        logger.debug("Barra de menu configurada com sucesso")
