from source.utils.LogManager import LogManager
from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
logger = LogManager.get_logger()

def _obter_percentual_disco(self):
    try:
        results = []
        if not self.psutil:
            return [0.0 for _ in (self.disk_keys or [None])]

        intervalo_s = max(0.001, getattr(self, "intervalo_ms", 100) / 1000.0)

        try:
            current = self.psutil.disk_io_counters(perdisk=True) or {}

        except Exception:
            current = {}

        chart = getattr(self, "disk_view", None).chart() if getattr(self, "disk_view", None) else None

        def _distinct_palette(n, tema_local):
            hex_base = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
                "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
                "#ffff33", "#a65628", "#f781bf", "#999999", "#2b8cbe"
            ]

            base = [QColor(h) for h in hex_base]
            if n <= len(base):
                return base[:n]

            out = list(base)
            for i in range(n - len(base)):
                hue = int((360 * i) / max(1, (n - len(base))))
                if (tema_local or "claro").lower() == "escuro":
                    col = QColor.fromHsv(hue, 230, 230)

                else:
                    col = QColor.fromHsv(hue, 200, 200)

                out.append(col)

            return out

        def _reaplicar_cores_disks():
            try:
                if not isinstance(self.disk_series, list):
                    return

                pal = _distinct_palette(len(self.disk_series), getattr(self, "_tema_atual", "claro"))
                for i, s in enumerate(self.disk_series):
                    try:
                        pen = QPen(pal[i]); pen.setWidth(2)
                        s.setPen(pen)

                    except Exception:
                        try:
                            s.setColor(pal[i])

                        except Exception:
                            pass

            except Exception:
                pass

        try:
            removed = [k for k in list(self.disk_keys) if k not in current]
            for rk in removed:
                idx = self.disk_keys.index(rk)
                try:
                    if isinstance(self.disk_series, list) and idx < len(self.disk_series):
                        s = self.disk_series.pop(idx)
                        if chart and s:
                            try:
                                chart.removeSeries(s)

                            except Exception:
                                pass

                except Exception:
                    pass

                try:
                    self.disk_keys.pop(idx)
                    self.disk_labels.pop(idx)

                except Exception:
                    pass

                try:
                    if idx < len(self.disk_data):
                        self.disk_data.pop(idx)

                except Exception:
                    pass

            if removed:
                _reaplicar_cores_disks()

        except Exception:
            pass

        try:
            added = [k for k in current.keys() if k not in self.disk_keys]
            for nk in sorted(added):
                try:
                    s = QLineSeries()
                    try:
                        if nk.lower().startswith("physicaldrive"):
                            s.setName(f"Disco {nk[len('PhysicalDrive'):]}")

                        else:
                            s.setName(str(nk))

                    except Exception:
                        pass

                    if chart:
                        try:
                            chart.addSeries(s)
                            axes = chart.axes()
                            ax_x = next((a for a in axes if hasattr(a, "orientation") and a.orientation() == Qt.Horizontal), None)
                            ax_y = next((a for a in axes if hasattr(a, "orientation") and a.orientation() == Qt.Vertical), None)
                            if ax_x: s.attachAxis(ax_x)
                            if ax_y: s.attachAxis(ax_y)

                        except Exception:
                            pass

                    if not isinstance(self.disk_series, list):
                        self.disk_series = [self.disk_series]

                    self.disk_series.append(s)
                    self.disk_keys.append(nk)

                    try:
                        lbl = s.name()

                    except Exception:
                        lbl = nk

                    self.disk_labels.append(lbl)
                    self.disk_data.append([])

                except Exception:
                    logger.debug("Falha ao adicionar série para novo disco", exc_info=True)

            if added:
                _reaplicar_cores_disks()

                try:
                    self._update_disk_drive_mapping()
                    self._update_disk_chart_title()

                except Exception:
                    pass

        except Exception:
            pass

        for k in self.disk_keys:
            try:
                v = current.get(k)
                prev = self._prev_disk_io.get(k, (0, 0))
                read_cur = getattr(v, "read_bytes", 0)
                write_cur = getattr(v, "write_bytes", 0)
                delta = (read_cur - prev[0]) + (write_cur - prev[1])
                if delta < 0:
                    delta = 0

                kb_s = (delta / intervalo_s) / 1024.0
                results.append(float(kb_s))

            except Exception:
                results.append(0.0)

        try:
            for k, v in current.items():
                try:
                    self._prev_disk_io[k] = (getattr(v, "read_bytes", 0), getattr(v, "write_bytes", 0))

                except Exception:
                    self._prev_disk_io[k] = (0, 0)

        except Exception:
            pass

        return results

    except Exception as e:
        logger.error(f"Erro ao ler uso/IO de disco: {e}", exc_info=True)

    return [0.0 for _ in (self.disk_keys or [None])]
