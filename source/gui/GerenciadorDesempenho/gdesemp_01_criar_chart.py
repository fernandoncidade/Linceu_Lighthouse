from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtCore import QMargins
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QSizePolicy
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_chart(self, titulo, series_names=None):
    if series_names:
        series = []
        for name in series_names:
            s = QLineSeries()
            try:
                s.setName(str(name))

            except Exception:
                pass

            series.append(s)

    else:
        series = QLineSeries()

    chart = QChart()
    if isinstance(series, list):
        for s in series:
            chart.addSeries(s)

    else:
        chart.addSeries(series)

    chart.setTitle(titulo)
    chart.legend().hide()
    chart.createDefaultAxes()

    try:
        chart.setContentsMargins(0, 0, 0, 0)

    except Exception:
        pass

    try:
        chart.setMargins(QMargins(2, 2, 2, 2))

    except Exception:
        pass

    try:
        chart.setBackgroundRoundness(0)

    except Exception:
        pass

    try:
        for axis in chart.axes():
            try:
                if hasattr(axis, "setLabelsAngle"):
                    axis.setLabelsAngle(0)

                if hasattr(axis, "setLabelsMargin"):
                    axis.setLabelsMargin(0)

                if hasattr(axis, "setTitleText"):
                    try:
                        axis.setTitleText("")

                    except Exception:
                        pass

            except Exception:
                pass

    except Exception:
        pass

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    try:
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view.setMinimumSize(0, 0)

    except Exception:
        pass

    try:
        view.setContentsMargins(0, 0, 0, 0)

    except Exception:
        pass

    try:
        view.setStyleSheet("border: none; background: transparent;")

    except Exception:
        pass

    return series, view
