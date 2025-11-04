import os
import sys
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QLineEdit, QDateTimeEdit, QFormLayout, QPushButton
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QIcon
from Filtros.fil_03_AdministradorFiltros import AdministradorFiltros
from utils.IconUtils import get_icon_path
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        icon_path = os.path.join(base_path, "icones")

        layout = QVBoxLayout(self)

        grupo_operacao = QGroupBox(self.loc.get_text("operation_filter"))
        grupo_operacao.setObjectName("grupo_operacao")
        layout_operacao = QVBoxLayout()
        self.checkboxes_operacao = {}
        for op in ["op_moved", "op_renamed", "op_added", "op_deleted", "op_modified", "op_scanned"]:
            cb = QCheckBox(self.loc.get_text(op))
            cb.setChecked(True)
            cb.stateChanged.connect(self.on_filtro_alterado)
            self.checkboxes_operacao[op] = cb
            layout_operacao.addWidget(cb)

        grupo_operacao.setLayout(layout_operacao)

        grupo_busca = QGroupBox(self.loc.get_text("search"))
        grupo_busca.setObjectName("grupo_busca")
        layout_busca = QHBoxLayout()
        self.campo_busca = QLineEdit()
        self.campo_busca.textChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_busca.addWidget(self.campo_busca)
        grupo_busca.setLayout(layout_busca)

        grupo_extensao = QGroupBox(self.loc.get_text("extension_filter"))
        grupo_extensao.setObjectName("grupo_extensao")
        layout_extensao = QHBoxLayout()
        self.campo_extensao = QLineEdit()
        self.campo_extensao.setPlaceholderText("pdf, txt, doc...")
        self.campo_extensao.textChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_extensao.addWidget(self.campo_extensao)
        grupo_extensao.setLayout(layout_extensao)

        grupo_data = QGroupBox(self.loc.get_text("date_filter"))
        layout_data = QFormLayout()

        self.ignorar_mover = QCheckBox(self.loc.get_text("ignore_move_filter"))
        self.ignorar_mover.setChecked(AdministradorFiltros.filtros_estado.get("ignorar_mover", True))
        self.ignorar_mover.stateChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_data.addRow(self.ignorar_mover)

        self.ignorar_renomeados = QCheckBox(self.loc.get_text("ignore_rename_filter"))
        self.ignorar_renomeados.setChecked(AdministradorFiltros.filtros_estado.get("ignorar_renomeados", True))
        self.ignorar_renomeados.stateChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_data.addRow(self.ignorar_renomeados)

        self.ignorar_adicionados = QCheckBox(self.loc.get_text("ignore_add_filter"))
        self.ignorar_adicionados.setChecked(AdministradorFiltros.filtros_estado.get("ignorar_adicionados", True))
        self.ignorar_adicionados.stateChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_data.addRow(self.ignorar_adicionados)

        self.ignorar_excluidos = QCheckBox(self.loc.get_text("ignore_delete_filter"))
        self.ignorar_excluidos.setChecked(AdministradorFiltros.filtros_estado.get("ignorar_excluidos", True))
        self.ignorar_excluidos.stateChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_data.addRow(self.ignorar_excluidos)

        self.ignorar_data_modificados = QCheckBox(self.loc.get_text("ignore_modified_filter"))
        self.ignorar_data_modificados.setChecked(AdministradorFiltros.filtros_estado.get("ignorar_data_modificados", True))
        self.ignorar_data_modificados.stateChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_data.addRow(self.ignorar_data_modificados)

        self.ignorar_escaneados = QCheckBox(self.loc.get_text("ignore_scanned_filter"))
        self.ignorar_escaneados.setChecked(AdministradorFiltros.filtros_estado.get("ignorar_escaneados", True))
        self.ignorar_escaneados.stateChanged.connect(self.administrador_filtros.aplicar_filtros)
        layout_data.addRow(self.ignorar_escaneados)

        container_data_inicial = QHBoxLayout()
        self.data_inicial = QDateTimeEdit()
        self.data_inicial.setDateTime(QDateTime.currentDateTime().addDays(-30))
        self.data_inicial.dateTimeChanged.connect(self.administrador_filtros.aplicar_filtros)
        container_data_inicial.addWidget(self.data_inicial)

        btn_calendario_inicial = QPushButton()
        btn_calendario_inicial.setIcon(QIcon(get_icon_path("calendar.ico")))
        btn_calendario_inicial.setFixedSize(24, 24)
        btn_calendario_inicial.clicked.connect(lambda: self.administrador_calendario.mostrar_calendario(self.data_inicial))
        container_data_inicial.addWidget(btn_calendario_inicial)

        container_data_final = QHBoxLayout()
        self.data_final = QDateTimeEdit()
        self.data_final.setDateTime(QDateTime.currentDateTime())
        self.data_final.dateTimeChanged.connect(self.administrador_filtros.aplicar_filtros)
        container_data_final.addWidget(self.data_final)

        btn_calendario_final = QPushButton()
        btn_calendario_final.setIcon(QIcon(get_icon_path("calendar.ico")))
        btn_calendario_final.setFixedSize(24, 24)
        btn_calendario_final.clicked.connect(lambda: self.administrador_calendario.mostrar_calendario(self.data_final))
        container_data_final.addWidget(btn_calendario_final)

        layout_data.addRow(self.loc.get_text("start_date"), container_data_inicial)
        layout_data.addRow(self.loc.get_text("end_date"), container_data_final)
        grupo_data.setLayout(layout_data)

        layout.addWidget(grupo_operacao)
        layout.addWidget(grupo_busca)
        layout.addWidget(grupo_extensao)
        layout.addWidget(grupo_data)

        self.gerenciador_botoes.add_button_with_label(
            layout, 
            self.loc.get_text("clear_filters"), 
            'clear_button3.ico', 
            self.administrador_filtros.limpar_filtros
        )

        layout.addStretch()

        self.sincronizar_com_menu_principal()

    except Exception as e:
        logger.error(f"Erro ao configurar interface de filtros: {e}", exc_info=True)
