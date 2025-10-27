from PySide6.QtGui import QColor, QBrush, QPen
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _aplicar_tema(self, novo_tema):
    try:
        tema = (novo_tema or "claro").lower()
        if tema not in ("claro", "escuro"):
            tema = "claro"

        try:
            self._tema_atual = tema

        except Exception:
            pass

        if tema == "escuro":
            bg_color = QColor(28, 28, 30)
            title_color = QColor(220, 220, 220)
            axis_color = QColor(180, 180, 180)
            cpu_color = QColor(102, 204, 255)
            mem_color = QColor(102, 255, 178)
            disk_color = QColor(255, 153, 102)
            grid_alpha = 60

        else:
            bg_color = QColor(250, 250, 250)
            title_color = QColor(20, 20, 20)
            axis_color = QColor(80, 80, 80)
            cpu_color = QColor(0, 102, 204)
            mem_color = QColor(0, 153, 77)
            disk_color = QColor(204, 85, 0)
            grid_alpha = 50

        try:
            self._disk_color_base = disk_color

        except Exception:
            pass

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
                if tema_local == "escuro":
                    col = QColor.fromHsv(hue, 230, 230)

                else:
                    col = QColor.fromHsv(hue, 200, 200)

                out.append(col)

            return out

        charts = [self.cpu_view.chart(), self.mem_view.chart(), self.disk_view.chart()]
        series_list = [self.cpu_series, self.mem_series, self.disk_series]
        series_colors = [cpu_color, mem_color, disk_color]
        for chart, series, color in zip(charts, series_list, series_colors):
            if chart is None:
                continue

            try:
                chart.setBackgroundBrush(QBrush(bg_color))
                chart.setTitleBrush(QBrush(title_color))

            except Exception:
                pass

            try:
                if isinstance(series, list):
                    pal = _distinct_palette(len(series), tema)
                    for i, s in enumerate(series):
                        try:
                            pen = QPen(pal[i])
                            pen.setWidth(2)
                            s.setPen(pen)

                        except Exception:
                            try:
                                s.setColor(pal[i])

                            except Exception:
                                pass

                    try:
                        if hasattr(self, '_update_disk_chart_title'):
                            self._update_disk_chart_title()

                    except Exception:
                        pass

                else:
                    pen = QPen(color)
                    pen.setWidth(2)
                    try:
                        series.setPen(pen)

                    except Exception:
                        try:
                            series.setColor(color)

                        except Exception:
                            pass

            except Exception:
                pass

            try:
                axes = chart.axes()
                for axis in axes:
                    try:
                        if hasattr(axis, "setLabelsBrush"):
                            axis.setLabelsBrush(QBrush(axis_color))

                        elif hasattr(axis, "setLabelsColor"):
                            axis.setLabelsColor(axis_color)

                        subtle_color = QColor(axis_color)
                        subtle_color.setAlpha(grid_alpha)
                        grid_pen = QPen(subtle_color)
                        try:
                            grid_pen.setWidthF(0.5)

                        except Exception:
                            grid_pen.setWidth(1)

                        if hasattr(axis, "setGridLinePen"):
                            try:
                                axis.setGridLinePen(grid_pen)

                            except Exception:
                                pass

                        if hasattr(axis, "setMinorGridLinePen"):
                            try:
                                axis.setMinorGridLinePen(grid_pen)

                            except Exception:
                                pass

                        if hasattr(axis, "setLinePen"):
                            try:
                                axis.setLinePen(grid_pen)

                            except Exception:
                                pass

                        elif hasattr(axis, "setPen"):
                            try:
                                axis.setPen(grid_pen)

                            except Exception:
                                pass

                    except Exception:
                        pass

            except Exception:
                pass

        try:
            for view in (self.cpu_view, self.mem_view, self.disk_view):
                try:
                    view.setBackgroundBrush(QBrush(bg_color))

                except Exception:
                    try:
                        view.setStyleSheet(f"background-color: rgba({bg_color.red()},{bg_color.green()},{bg_color.blue()},{255});")

                    except Exception:
                        pass

                try:
                    view.update()

                except Exception:
                    pass

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao aplicar tema nos gráficos: {e}", exc_info=True)
