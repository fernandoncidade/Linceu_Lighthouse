from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QCheckBox, QFrame, QPushButton
from source.utils.LogManager import LogManager
from source.utils.IconUtils import get_icon_path
logger = LogManager.get_logger()

def _criar_painel_selecao(self, graficos=None):
    try:
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        texto_ocultar = self.loc.get_text("hide_selection_panel")
        self.btn_toggle_painel = self._criar_botao_toggle_painel(texto_ocultar)

        largura_botao = 25
        self.btn_toggle_painel.setFixedWidth(largura_botao)

        container_layout.addWidget(self.btn_toggle_painel, 0, Qt.AlignLeft | Qt.AlignTop)

        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        max_width = self._calcular_largura_ideal(graficos)
        self.tamanho_painel_original = max_width
        panel.setFixedWidth(max_width)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        self.titulo_selecionar_graficos = QLabel(self.loc.get_text("select_graphs"))
        layout.addWidget(self.titulo_selecionar_graficos)

        scroll_area = QScrollArea()
        scroll_widget = QWidget()

        self.checkboxes_layout = QVBoxLayout()
        self.checkbox_todos = QCheckBox(self.loc.get_text("select_all"))
        self.checkbox_todos.setChecked(True)
        self.checkbox_todos.setTristate(True)
        self.checkbox_todos.clicked.connect(self._alternar_todos_checkboxes)
        self.checkboxes_layout.addWidget(self.checkbox_todos)

        separador = QFrame()
        separador.setFrameStyle(QFrame.HLine)
        self.checkboxes_layout.addWidget(separador)
        self.checkboxes_layout.addStretch()

        scroll_widget.setLayout(self.checkboxes_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(500)
        layout.addWidget(scroll_area, 1)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)

        self.btn_salvar_selecionados = QPushButton(self.loc.get_text("save_selected"))
        self.btn_salvar_selecionados.setIcon(QIcon(get_icon_path("salvar.ico")))
        self.btn_salvar_selecionados.clicked.connect(self._salvar_graficos_selecionados)
        buttons_layout.addWidget(self.btn_salvar_selecionados)

        self.btn_salvar_todos = QPushButton(self.loc.get_text("save_all"))
        self.btn_salvar_todos.setIcon(QIcon(get_icon_path("salvar.ico")))
        self.btn_salvar_todos.clicked.connect(lambda: self.salvar_todos_graficos(self.gerador_atual))
        buttons_layout.addWidget(self.btn_salvar_todos)

        self.btn_atualizar = QPushButton(self.loc.get_text("refresh"))
        self.btn_atualizar.setIcon(QIcon(get_icon_path("atualizar.ico")))
        self.btn_atualizar.clicked.connect(lambda: self._atualizar_graficos(self.dialog_estatisticas))
        buttons_layout.addWidget(self.btn_atualizar)

        layout.addLayout(buttons_layout, 0)
        panel.setLayout(layout)

        container_layout.addWidget(panel, 1, Qt.AlignTop)

        largura_total = largura_botao + max_width
        container.setFixedWidth(largura_total)
        container.setLayout(container_layout)
        self.painel_selecao_interno = panel
        return container

    except Exception as e:
        logger.error(f"Erro ao criar painel de seleção: {e}", exc_info=True)
