from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_series(self, cpu_list, mem_list, disk_list):
    def update_series_obj(series_obj, data):
        try:
            series_obj.clear()

        except Exception:
            pass

        try:
            for i, v in enumerate(data):
                try:
                    series_obj.append(i, v)

                except Exception:
                    try:
                        from PySide6.QtCore import QPointF
                        series_obj.append(QPointF(i, v))

                    except Exception:
                        pass

        except Exception:
            pass

        try:
            chart = series_obj.chart()
            if chart:
                axes = chart.axes()
                if axes:
                    try:
                        axes[0].setRange(0, max(1, self.max_pontos))
                        if len(axes) > 1:
                            if series_obj is getattr(self, "cpu_series", None) or series_obj is getattr(self, "mem_series", None):
                                axes[1].setRange(0, 100)

                    except Exception:
                        pass

        except Exception:
            pass

    try:
        try:
            update_series_obj(self.cpu_series, cpu_list)

        except Exception:
            logger.debug("Falha ao atualizar série CPU", exc_info=True)

        try:
            update_series_obj(self.mem_series, mem_list)

        except Exception:
            logger.debug("Falha ao atualizar série MEM", exc_info=True)

        if isinstance(self.disk_series, list):
            for idx, series_obj in enumerate(self.disk_series):
                data = disk_list[idx] if idx < len(disk_list) else []
                try:
                    update_series_obj(series_obj, data)

                except Exception:
                    logger.debug(f"Falha ao atualizar série de disco {idx}", exc_info=True)

            try:
                chart = getattr(self, "disk_view", None).chart()
                if chart:
                    axes = chart.axes()
                    if len(axes) > 1:
                        max_val = 0.0
                        try:
                            for dl in disk_list:
                                if dl:
                                    mv = max(dl)
                                    if mv > max_val:
                                        max_val = mv

                        except Exception:
                            max_val = 0.0

                        upper = max(10.0, max_val * 1.2)

                        try:
                            axes[1].setRange(0, upper)

                        except Exception:
                            pass

            except Exception:
                pass

            if len(self.disk_series) > len(disk_list):
                for extra in range(len(disk_list), len(self.disk_series)):
                    try:
                        self.disk_series[extra].clear()

                    except Exception:
                        pass

        else:
            flattened = []
            try:
                max_len = max((len(dl) for dl in disk_list), default=0)
                for i in range(max_len):
                    vals = []
                    for dl in disk_list:
                        if i < len(dl):
                            vals.append(dl[i])

                    flattened.append(sum(vals) / len(vals) if vals else 0)

            except Exception:
                flattened = []

            try:
                update_series_obj(self.disk_series, flattened)
                try:
                    chart = getattr(self, "disk_view", None).chart()
                    if chart:
                        axes = chart.axes()
                        if len(axes) > 1:
                            max_val = max(flattened) if flattened else 0.0
                            upper = max(10.0, max_val * 1.2)
                            try:
                                axes[1].setRange(0, upper)

                            except Exception:
                                pass

                except Exception:
                    pass

            except Exception:
                logger.debug("Falha ao atualizar série genérica de disco", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao atualizar séries: {e}", exc_info=True)
