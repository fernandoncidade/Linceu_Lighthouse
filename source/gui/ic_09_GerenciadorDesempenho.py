from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QToolButton, QSizePolicy, QSplitter
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

try:
    from source.services.GerenciamentoTabela.gtab_34_monitor_tema_windows import MonitorTemaWindows

except Exception:
    MonitorTemaWindows = None


class GerenciadorDesempenho:
    from source.gui.GerenciadorDesempenho.gdesemp_01_criar_chart import _criar_chart
    from source.gui.GerenciadorDesempenho.gdesemp_02_obter_percentual_disco import _obter_percentual_disco
    from source.gui.GerenciadorDesempenho.gdesemp_03_atualizar import _atualizar
    from source.gui.GerenciadorDesempenho.gdesemp_04_atualizar_series import _atualizar_series
    from source.gui.GerenciadorDesempenho.gdesemp_05_on_pin_toggled import _on_pin_toggled
    from source.gui.GerenciadorDesempenho.gdesemp_06_update_shared_dialog_title import _update_shared_dialog_title
    from source.gui.GerenciadorDesempenho.gdesemp_07_rebuild_tab_mapping import _rebuild_tab_mapping
    from source.gui.GerenciadorDesempenho.gdesemp_08_repin_all_from_shared import _repin_all_from_shared
    from source.gui.GerenciadorDesempenho.gdesemp_09_detach_chart import _detach_chart
    from source.gui.GerenciadorDesempenho.gdesemp_10_pin_chart import _pin_chart
    from source.gui.GerenciadorDesempenho.gdesemp_11_aplicar_tema import _aplicar_tema
    from source.gui.GerenciadorDesempenho.gdesemp_12_stop import stop
    from source.gui.GerenciadorDesempenho.gdesemp_14_atualizar_traducoes import _atualizar_traducoes
    from source.gui.GerenciadorDesempenho.gdesemp_15_update_disk_drive_mapping import _update_disk_drive_mapping
    from source.gui.GerenciadorDesempenho.gdesemp_16_update_disk_chart_title import _update_disk_chart_title

    def __init__(self, interface, intervalo_ms=100, max_pontos=60):
        self.interface = interface
        self.intervalo_ms = intervalo_ms
        self.max_pontos = max_pontos
        self.timer = QTimer()
        self.timer.setInterval(self.intervalo_ms)
        self.timer.timeout.connect(self._atualizar)

        self.psutil = None
        try:
            import psutil
            self.psutil = psutil

        except Exception as e:
            logger.warning("psutil não disponível. Instale com: pip install psutil", exc_info=True)

        self.cpu_data = []
        self.mem_data = []
        self.disk_keys = []
        self.disk_labels = []
        if self.psutil:
            try:
                dio = self.psutil.disk_io_counters(perdisk=True) or {}
                self.disk_keys = list(sorted(dio.keys()))
                def _fmt_label(k: str) -> str:
                    try:
                        if k.lower().startswith("physicaldrive"):
                            return f"Disco {k[len('PhysicalDrive'):]}".strip()

                        return k

                    except Exception:
                        return str(k)

                self.disk_labels = [_fmt_label(k) for k in self.disk_keys]

            except Exception:
                self.disk_keys = []
                self.disk_labels = []

        if not self.disk_labels:
            self.disk_keys = ["disk0"]
            self.disk_labels = ["Disco"]

        self.disk_data = [[] for _ in self.disk_labels]
        self._prev_disk_io = {}
        self._disk_drive_letters = {}

        try:
            if self.psutil:
                try:
                    dio = self.psutil.disk_io_counters(perdisk=True)
                    if dio:
                        for k, v in dio.items():
                            self._prev_disk_io[k] = (getattr(v, "read_bytes", 0), getattr(v, "write_bytes", 0))

                except Exception:
                    self._prev_disk_io = {}

        except Exception:
            self._prev_disk_io = {}

        self._update_disk_drive_mapping()

        try:
            if hasattr(self.interface, "loc"):
                cpu_title = self.interface.loc.get_text("CPU_Porcentagem")
                mem_title = self.interface.loc.get_text("Memoria_RAM_Porcentagem")
                disk_title = self.interface.loc.get_text("Discos_Porcentagem")

            else:
                cpu_title = "CPU (%)"
                mem_title = "Memória RAM (%)"
                disk_title = "Discos (%)"

        except Exception:
            cpu_title = "CPU (%)"
            mem_title = "Memória RAM (%)"
            disk_title = "Discos (%)"

        self.cpu_series, self.cpu_view = self._criar_chart(cpu_title)
        self.mem_series, self.mem_view = self._criar_chart(mem_title)
        self.disk_series, self.disk_view = self._criar_chart(disk_title, series_names=self.disk_labels)
        self.chart_containers = []
        self.detached_dialogs = [None, None, None]
        self._shared_dialog = None
        self.pin_buttons = []
        self._tab_for_chart = {}
        self._monitor_tema = None

        try:
            if MonitorTemaWindows:
                self._monitor_tema = MonitorTemaWindows()
                try:
                    self._monitor_tema.tema_alterado.connect(self._aplicar_tema)

                except Exception:
                    pass

                try:
                    self._monitor_tema.iniciar_monitoramento()

                except Exception:
                    pass

        except Exception:
            self._monitor_tema = None

        self.widget = QWidget()
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout = QVBoxLayout(self.widget)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        try:
            if hasattr(self.interface, "loc"):
                labels = [
                    ("CPU", self.interface.loc.get_text("CPU_Porcentagem")),
                    ("RAM", self.interface.loc.get_text("Memoria_RAM_Porcentagem")),
                    ("Discos", self.interface.loc.get_text("Discos_Porcentagem"))
                ]

            else:
                labels = [("CPU", "CPU (%)"), ("RAM", "Memória RAM (%)"), ("Discos", "Discos (%)")]

        except Exception:
            labels = [("CPU", "CPU (%)"), ("RAM", "Memória RAM (%)"), ("Discos", "Discos (%)")]

        for idx, (short_label, full_label) in enumerate(labels):
            lbl = QLabel(full_label)
            lbl.setToolTip(full_label)
            lbl.setMinimumWidth(105)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            btn = QToolButton()
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setToolTip("Destacar/Fixar")
            btn.setText("📌")
            btn.setStyleSheet("QToolButton:checked { color: black } QToolButton { color: gray }")
            btn.toggled.connect(lambda checked, i=idx: self._on_pin_toggled(i, checked))

            self.pin_buttons.append(btn)
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(4)
            item_layout.addWidget(lbl, 1)
            item_layout.addWidget(btn, 0, Qt.AlignRight)
            header_layout.addWidget(item_widget)

        main_layout.addWidget(header, 0)

        splitter = QSplitter(Qt.Vertical)
        for view in (self.cpu_view, self.mem_view, self.disk_view):
            wrapper = QWidget()
            lay = QVBoxLayout(wrapper)
            lay.setContentsMargins(0,0,0,0)
            lay.setSpacing(0)
            view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lay.addWidget(view)
            splitter.addWidget(wrapper)
            self.chart_containers.append(wrapper)

        main_layout.addWidget(splitter, 1)

        try:
            if hasattr(self.interface, 'loc') and hasattr(self.interface.loc, 'idioma_alterado'):
                self.interface.loc.idioma_alterado.connect(self._atualizar_traducoes)

        except Exception as e:
            logger.error(f"Erro ao conectar sinal de alteração de idioma: {e}", exc_info=True)

        try:
            tema_inicial = None
            if self._monitor_tema:
                try:
                    tema_inicial = self._monitor_tema.obter_tema_atual()

                except Exception:
                    tema_inicial = None

            if tema_inicial is None:
                try:
                    from source.services.GerenciamentoTabela.gtab_01_detectar_tema_windows import detectar_tema_windows
                    tema_inicial = detectar_tema_windows(self)

                except Exception:
                    tema_inicial = "claro"

            self._aplicar_tema(tema_inicial)

        except Exception as e:
            logger.error(f"Erro ao aplicar tema inicial nos gráficos: {e}", exc_info=True)

        self._update_disk_chart_title()

        if self.psutil:
            self.timer.start()

        else:
            zeros_disks = [[0] for _ in self.disk_labels]
            self._atualizar_series([0], [0], zeros_disks)

    _obter_percentual_disco = _obter_percentual_disco
    _update_shared_dialog_title = _update_shared_dialog_title
    _rebuild_tab_mapping = _rebuild_tab_mapping
    _repin_all_from_shared = _repin_all_from_shared
    _detach_chart = _detach_chart
    _pin_chart = _pin_chart
    stop = stop
    _update_disk_drive_mapping = _update_disk_drive_mapping
    _update_disk_chart_title = _update_disk_chart_title
