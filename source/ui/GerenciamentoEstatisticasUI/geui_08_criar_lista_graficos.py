from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_lista_graficos(self, gerador):
    try:
        return [
            {"titulo": self.loc.get_text("operations_pie"), "func": gerador.grafico_operacoes_pizza},
            {"titulo": self.loc.get_text("bar_chart"), "func": gerador.grafico_tipos_arquivo_barras},
            {"titulo": self.loc.get_text("timeline"), "func": gerador.grafico_timeline_operacoes},
            {"titulo": self.loc.get_text("tree_map"), "func": gerador.grafico_treemap_tipos},
            {"titulo": self.loc.get_text("hour_histogram"), "func": gerador.grafico_histograma_horarios},
            {"titulo": self.loc.get_text("pareto_analysis"), "func": gerador.grafico_pareto_operacoes},
            {"titulo": self.loc.get_text("operations_by_day"), "func": gerador.grafico_cluster_linha},
            {"titulo": self.loc.get_text("size_distribution"), "func": gerador.grafico_boxplot_distribuicao},
            {"titulo": self.loc.get_text("events_monitored"), "func": gerador.grafico_boxplot_eventos},
            {"titulo": self.loc.get_text("temporal_distribution"), "func": gerador.grafico_heatmap},
            {"titulo": self.loc.get_text("file_size_analysis"), "func": gerador.grafico_scatter},
            {"titulo": self.loc.get_text("file_operations_flow"), "func": gerador.grafico_sankey},
            {"titulo": self.loc.get_text("event_to_path_flow"), "func": gerador.grafico_sankey_evento_caminho},
            {"titulo": self.loc.get_text("type_to_path_flow"), "func": gerador.grafico_sankey_tipo_caminho},
            {"titulo": self.loc.get_text("operations_by_file_type"), "func": gerador.grafico_radar},
            {"titulo": self.loc.get_text("file_size_distribution"), "func": gerador.grafico_dotplot},
            {"titulo": self.loc.get_text("directory_tree"), "func": gerador.grafico_arvore_diretorios}
        ]

    except Exception as e:
        logger.error(f"Erro ao criar lista de gráficos: {e}", exc_info=True)
