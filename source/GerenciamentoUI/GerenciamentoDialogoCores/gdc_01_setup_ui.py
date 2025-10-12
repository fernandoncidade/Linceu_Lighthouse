from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QFrame, QWidget, QTabWidget
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_ui(self):
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

        self.label_atual = QLabel(f"{self.loc.get_text('current')}:")
        self.label_novo = QLabel(f"{self.loc.get_text('new')}:")
        layout_preview.addWidget(self.label_atual)
        layout_preview.addWidget(self.preview_atual)
        layout_preview.addSpacing(20)
        layout_preview.addWidget(self.label_novo)
        layout_preview.addWidget(self.preview_nova)
        layout_preview.addStretch(1)

        layout_principal.addLayout(layout_preview)

        self.tab_widget = QTabWidget(self)

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
        self.tab_widget.addTab(tab_basicas, self.loc.get_text("basics"))

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
        self.tab_widget.addTab(tab_pasteis, self.loc.get_text("pastels"))

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
        self.tab_widget.addTab(tab_vibrantes, self.loc.get_text("vibrant"))

        layout_principal.addWidget(self.tab_widget)

        self.btn_avancado = QPushButton(self.loc.get_text("advanced_color_picker"))
        self.btn_avancado.clicked.connect(self._abrir_seletor_avancado)
        layout_principal.addWidget(self.btn_avancado)

        layout_botoes = QHBoxLayout()
        self.btn_ok = QPushButton(self.loc.get_text("ok"))
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancelar = QPushButton(self.loc.get_text("cancel"))
        self.btn_cancelar.clicked.connect(self.reject)

        layout_botoes.addStretch(1)
        layout_botoes.addWidget(self.btn_ok)
        layout_botoes.addWidget(self.btn_cancelar)
        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)
        self.resize(400, 500)

    except Exception as e:
        logger.error(f"Erro ao configurar interface do diálogo de cores: {e}", exc_info=True)
        raise
