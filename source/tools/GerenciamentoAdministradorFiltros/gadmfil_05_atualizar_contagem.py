from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_contagem(self):
    try:
        main_loc = self.parent.loc if hasattr(self.parent, 'loc') else None

        if main_loc is None:
            from ui.ui_12_LocalizadorQt import LocalizadorQt
            main_loc = LocalizadorQt()

        if self.parent and hasattr(self.parent, 'tabela_dados'):
            try:
                total = self.parent.tabela_dados.rowCount()
                visiveis = sum(1 for row in range(total) if not self.parent.tabela_dados.isRowHidden(row))

                if total == 0:
                    return f"{main_loc.get_text('visible_filters')}: 0 / {main_loc.get_text('total_monitored')}: 0 | {main_loc.get_text('filtered_rate')}: 0%"

                taxa_filtragem = 100 - ((visiveis / total) * 100)
                taxa_filtragem = round(taxa_filtragem, 2)
                return (
                    f"{main_loc.get_text('visible_filters')}: {visiveis} / "
                    f"{main_loc.get_text('total_monitored')}: {total} | "
                    f"{main_loc.get_text('filtered_rate')}: {taxa_filtragem}%"
                )

            except RuntimeError:
                logger.error("Tabela de dados não está mais disponível", exc_info=True)

        return f"{main_loc.get_text('visible_filters')}: 0 / {main_loc.get_text('total_monitored')}: 0 | {main_loc.get_text('filtered_rate')}: 0%"

    except Exception as e:
        logger.error(f"Erro ao atualizar contagem: {e}", exc_info=True)
        return "0 / 0 | 0%"
