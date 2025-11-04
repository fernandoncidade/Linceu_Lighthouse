from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_disk_chart_title(self):
    try:
        if not hasattr(self, 'disk_view') or not self.disk_view.chart():
            return

        try:
            if hasattr(self.interface, "loc"):
                base_title = self.interface.loc.get_text("Discos_Porcentagem")

            else:
                base_title = "Discos (%)"

        except Exception:
            base_title = "Discos (%)"

        if isinstance(self.disk_series, list) and len(self.disk_series) > 0:
            legend_parts = []

            def _get_current_palette():
                hex_base = [
                    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
                    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
                    "#ffff33", "#a65628", "#f781bf", "#999999", "#2b8cbe"
                ]

                return hex_base

            palette = _get_current_palette()

            for i, (disk_key, series) in enumerate(zip(self.disk_keys, self.disk_series)):
                try:
                    drive_info = self._disk_drive_letters.get(disk_key)
                    if drive_info:
                        drive_letter = drive_info[0]

                    else:
                        if disk_key.lower().startswith('physicaldrive'):
                            try:
                                num = disk_key.lower().replace('physicaldrive', '')
                                drive_letter = f"D{num}"

                            except Exception:
                                drive_letter = f"D{i}"

                        else:
                            drive_letter = f"D{i}"

                    color = palette[i % len(palette)]
                    legend_parts.append(f'<span style="color: {color};">■ {drive_letter}:</span>')

                except Exception:
                    continue

            if legend_parts:
                if len(legend_parts) <= 4:
                    legend = " ".join(legend_parts)
                    full_title = f"{base_title} | {legend}"

                else:
                    legend = " ".join(legend_parts[:3]) + " ..."
                    full_title = f"{base_title} | {legend}"

            else:
                full_title = base_title

        else:
            full_title = base_title

        self.disk_view.chart().setTitle(full_title)

    except Exception as e:
        logger.debug(f"Erro ao atualizar título do gráfico de discos: {e}")
