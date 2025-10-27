import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from source.utils.LogManager import LogManager
from .GeradorEstatisticas import (GraficoPizza, GraficoBarras, GraficoTimeline, 
                                  GraficoTreemap, GraficoHistograma, GraficoPareto, GraficoLinha, 
                                  GraficoBoxplot, GraficoRadarEventos, GraficoHeatmap, GraficoScatter, 
                                  GraficoSankey, GraficoRadar, GraficoDotplot,
                                  GraficoSankeyEventoCaminho, GraficoSankeyTipoCaminho, GraficoArvoreDiretorios)
logger = LogManager.get_logger()


class GeradorEstatisticas:
    __slots__ = ['db_path', 'loc', 'interface', '_geradores']

    def __init__(self, db_path, localizador=None, interface_principal=None):
        self.db_path = db_path
        self.loc = localizador
        self.interface = interface_principal
        self._geradores = {}

        self._inicializar_geradores()

    def _inicializar_geradores(self):
        geradores_classes = {
            'pizza': GraficoPizza,
            'barras': GraficoBarras,
            'timeline': GraficoTimeline,
            'treemap': GraficoTreemap,
            'histograma': GraficoHistograma,
            'pareto': GraficoPareto,
            'linha': GraficoLinha,
            'boxplot': GraficoBoxplot,
            'boxplot_eventos': GraficoRadarEventos,
            'heatmap': GraficoHeatmap,
            'scatter': GraficoScatter,
            'sankey': GraficoSankey,
            'radar': GraficoRadar,
            'dotplot': GraficoDotplot,
            'sankey_evento_caminho': GraficoSankeyEventoCaminho,
            'sankey_tipo_caminho': GraficoSankeyTipoCaminho,
            'arvore_diretorios': GraficoArvoreDiretorios
        }

        try:
            for nome, classe in geradores_classes.items():
                self._geradores[nome] = classe(self.db_path, self.loc, self.interface)

        except Exception as e:
            logger.error(f"Erro ao inicializar geradores: {e}", exc_info=True)

    def _obter_dados(self):
        try:
            if self._geradores:
                primeiro_nome = next(iter(self._geradores))
                return self._geradores[primeiro_nome]._obter_dados()

            query = """
                SELECT tipo_operacao, tipo, timestamp, tamanho 
                FROM monitoramento 
                WHERE timestamp IS NOT NULL
            """

            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)

            return df

        except Exception as e:
            logger.error(f"Erro ao obter dados: {e}", exc_info=True)
            return pd.DataFrame()

    def atualizar_textos_traduzidos(self):
        try:
            for nome, gerador in self._geradores.items():
                if hasattr(gerador, '_atualizar_textos_traduzidos'):
                    gerador._atualizar_textos_traduzidos()

        except Exception as e:
            logger.error(f"Erro ao atualizar textos traduzidos: {e}", exc_info=True)

    def adicionar_gerador(self, nome, classe_gerador):
        try:
            if hasattr(classe_gerador, '__slots__'):
                self._geradores[nome] = classe_gerador(self.db_path, self.loc, self.interface)

            else:
                msg = "Gerador deve usar __slots__ para consistência"
                logger.error(msg)
                raise ValueError(msg)

        except Exception as e:
            logger.error(f"Erro ao adicionar gerador '{nome}': {e}", exc_info=True)
            raise

    def remover_gerador(self, nome):
        try:
            if nome in self._geradores:
                del self._geradores[nome]

            else:
                logger.warning(f"Tentativa de remover gerador inexistente: '{nome}'")

        except Exception as e:
            logger.error(f"Erro ao remover gerador '{nome}': {e}", exc_info=True)

    def listar_geradores(self):
        return list(self._geradores.keys())

    def grafico_operacoes_pizza(self):
        try:
            return self._geradores['pizza'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de pizza: {e}", exc_info=True)
            raise

    def grafico_tipos_arquivo_barras(self):
        try:
            return self._geradores['barras'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de barras: {e}", exc_info=True)
            raise

    def grafico_timeline_operacoes(self):
        try:
            return self._geradores['timeline'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico timeline: {e}", exc_info=True)
            raise

    def grafico_treemap_tipos(self):
        try:
            return self._geradores['treemap'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico treemap: {e}", exc_info=True)
            raise

    def grafico_histograma_horarios(self):
        try:
            return self._geradores['histograma'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar histograma: {e}", exc_info=True)
            raise

    def grafico_pareto_operacoes(self):
        try:
            return self._geradores['pareto'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de pareto: {e}", exc_info=True)
            raise

    def grafico_cluster_linha(self):
        try:
            return self._geradores['linha'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de linha: {e}", exc_info=True)
            raise
    
    def grafico_boxplot_distribuicao(self):
        try:
            return self._geradores['boxplot'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar boxplot: {e}", exc_info=True)
            raise

    def grafico_boxplot_eventos(self):
        try:
            return self._geradores['boxplot_eventos'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar boxplot de eventos: {e}", exc_info=True)
            raise

    def grafico_heatmap(self):
        try:
            return self._geradores['heatmap'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar heatmap: {e}", exc_info=True)
            raise

    def grafico_scatter(self):
        try:
            return self._geradores['scatter'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar scatter: {e}", exc_info=True)
            raise

    def grafico_sankey(self):
        try:
            return self._geradores['sankey'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar sankey: {e}", exc_info=True)
            raise

    def grafico_radar(self):
        try:
            return self._geradores['radar'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar radar: {e}", exc_info=True)
            raise

    def grafico_dotplot(self):
        try:
            return self._geradores['dotplot'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar dotplot: {e}", exc_info=True)
            raise

    def grafico_sankey_evento_caminho(self):
        try:
            return self._geradores['sankey_evento_caminho'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar sankey evento→caminho: {e}", exc_info=True)
            raise

    def grafico_sankey_tipo_caminho(self):
        try:
            return self._geradores['sankey_tipo_caminho'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar sankey tipo→caminho: {e}", exc_info=True)
            raise

    def grafico_arvore_diretorios(self):
        try:
            return self._geradores['arvore_diretorios'].gerar()

        except Exception as e:
            logger.error(f"Erro ao gerar árvore de diretórios: {e}", exc_info=True)
            raise

    def gerar_grafico(self, tipo_grafico):
        try:
            if tipo_grafico in self._geradores:
                return self._geradores[tipo_grafico].gerar()

            else:
                msg = f"Tipo de gráfico '{tipo_grafico}' não encontrado"
                logger.error(msg)
                raise ValueError(msg)

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico '{tipo_grafico}': {e}", exc_info=True)
            raise

    def salvar_graficos(self, diretorio):
        logger = LogManager.get_logger()

        graficos = {
            self.loc.get_text("operations_pie") if self.loc else "operations_pie": self.grafico_operacoes_pizza,
            self.loc.get_text("bar_chart") if self.loc else "bar_chart": self.grafico_tipos_arquivo_barras,
            self.loc.get_text("timeline") if self.loc else "timeline": self.grafico_timeline_operacoes,
            self.loc.get_text("tree_map") if self.loc else "tree_map": self.grafico_treemap_tipos,
            self.loc.get_text("hour_histogram") if self.loc else "hour_histogram": self.grafico_histograma_horarios,
            self.loc.get_text("pareto_analysis") if self.loc else "pareto_analysis": self.grafico_pareto_operacoes,
            self.loc.get_text("operations_by_day") if self.loc else "operations_by_day": self.grafico_cluster_linha,
            self.loc.get_text("size_distribution") if self.loc else "size_distribution": self.grafico_boxplot_distribuicao,
            self.loc.get_text("events_monitored") if self.loc else "events_monitored": self.grafico_boxplot_eventos,
            self.loc.get_text("temporal_distribution") if self.loc else "temporal_distribution": self.grafico_heatmap,
            self.loc.get_text("file_size_analysis") if self.loc else "file_size_analysis": self.grafico_scatter,
            self.loc.get_text("file_operations_flow") if self.loc else "file_operations_flow": self.grafico_sankey,
            self.loc.get_text("event_to_path_flow") if self.loc else "event_to_path_flow": self.grafico_sankey_evento_caminho,
            self.loc.get_text("type_to_path_flow") if self.loc else "type_to_path_flow": self.grafico_sankey_tipo_caminho,
            self.loc.get_text("operations_by_file_type") if self.loc else "operations_by_file_type": self.grafico_radar,
            self.loc.get_text("file_size_distribution") if self.loc else "file_size_distribution": self.grafico_dotplot,
            self.loc.get_text("directory_tree") if self.loc else "directory_tree": self.grafico_arvore_diretorios
        }

        resultados = {}

        if not os.path.exists(diretorio):
            try:
                os.makedirs(diretorio, exist_ok=True)

            except Exception as e:
                logger.error(f"Erro ao criar diretório {diretorio}: {e}", exc_info=True)
                return {nome: False for nome in graficos.keys()}

        if not os.access(diretorio, os.W_OK):
            logger.error(f"Sem permissão de escrita no diretório {diretorio}")
            return {nome: False for nome in graficos.keys()}

        for nome, func in graficos.items():
            try:
                fig = func()
                arquivo_destino = os.path.join(diretorio, f"{nome}.png")

                try:
                    fig.savefig(arquivo_destino, bbox_inches='tight', dpi=100)
                    resultados[nome] = True

                except Exception as e:
                    logger.error(f"Erro ao salvar gráfico {nome}: {e}", exc_info=True)
                    resultados[nome] = False

                finally:
                    plt.close(fig)
                    plt.clf()
                    plt.cla()

            except Exception as e:
                logger.error(f"Erro ao processar gráfico {nome}: {e}", exc_info=True)
                resultados[nome] = False

        plt.close('all')
        return resultados
