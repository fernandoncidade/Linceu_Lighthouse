import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import numpy as np
from .gst_01_base_gerador import BaseGerador
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoSankey(BaseGerador):
    __slots__ = []

    def gerar(self):
        titulo = self.loc.get_text("file_operations_flow") if self.loc else 'Fluxo de Operações em Arquivos'
        try:
            df = self._obter_dados()

            if df.empty:
                return self._criar_grafico_sem_dados(titulo)

            try:
                import os
                import importlib
                import plotly.graph_objects as go
                import plotly.io as pio

                try:
                    kaleido_mod = importlib.import_module("kaleido")
                    exe_name = "kaleido.exe" if os.name == "nt" else "kaleido"

                    env_exe = os.environ.get("KALEIDO_EXECUTABLE")
                    candidatos = []
                    if env_exe:
                        candidatos.append(env_exe)

                    candidatos.append(os.path.join(os.path.dirname(kaleido_mod.__file__), "executable", exe_name))
                    exe_path = next((p for p in candidatos if p and os.path.exists(p)), None)

                    if exe_path:
                        try:
                            scopes_mod = importlib.import_module("kaleido.scopes.plotly")
                            PlotlyScope = getattr(scopes_mod, "PlotlyScope", None)
                            if PlotlyScope and not getattr(getattr(pio, "kaleido", None), "scope", None):
                                pio.kaleido.scope = PlotlyScope(executable=exe_path)

                        except Exception as e:
                            logger.warning(f"Falha ao configurar Kaleido PlotlyScope: {e}")

                    else:
                        logger.warning("Executável do Kaleido não encontrado (defina KALEIDO_EXECUTABLE ou inclua o diretório 'kaleido/executable').")

                except ModuleNotFoundError:
                    logger.warning("Kaleido não disponível no ambiente. plotly.io.to_image pode falhar.")

                except Exception as e:
                    logger.warning(f"Kaleido falhou ao carregar: {e}")

            except Exception as e:
                logger.error(f"Falha ao importar Plotly/Kaleido: {e}", exc_info=True)
                plt.figure(figsize=(16, 9))
                mensagem = self.loc.get_text("plotly_required") if self.loc else 'Biblioteca plotly/kaleido necessária para gerar o Diagrama de Sankey'
                plt.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=14)
                plt.axis('off')
                return plt.gcf()

            df_sankey = df[['tipo_operacao', 'tipo']].copy().dropna()
            if df_sankey.empty:
                return self._criar_grafico_sem_dados(titulo)

            operacoes_top = df_sankey['tipo_operacao'].value_counts().nlargest(6).index.tolist()
            tipos_top = df_sankey['tipo'].value_counts().nlargest(50).index.tolist()

            df_sankey = df_sankey[
                df_sankey['tipo_operacao'].isin(operacoes_top) &
                df_sankey['tipo'].isin(tipos_top)
            ]
            if df_sankey.empty:
                return self._criar_grafico_sem_dados(titulo)

            fluxos = df_sankey.groupby(['tipo_operacao', 'tipo']).size().reset_index(name='valor')

            todas_labels = operacoes_top + tipos_top
            mapa_indices = {label: i for i, label in enumerate(todas_labels)}

            fonte = [mapa_indices[op] for op in fluxos['tipo_operacao']]
            destino = [mapa_indices[t] for t in fluxos['tipo']]
            valores = fluxos['valor'].tolist()

            cores_ops = [self.cores_operacoes.get(op, '#333333') for op in operacoes_top]

            def color_from_index(i):
                pal = [
                    (55,126,184),(77,175,74),(228,26,28),(152,78,163),(255,127,0),
                    (166,86,40),(247,129,191),(153,153,153),(255,255,51),(166,206,227)
                ]
                r, g, b = pal[i % len(pal)]
                return f"#{r:02x}{g:02x}{b:02x}"

            cores_tipos = [color_from_index(i) for i in range(len(tipos_top))]
            cor_por_op = {lbl: cor for lbl, cor in zip(operacoes_top, cores_ops)}
            cores_links = [cor_por_op.get(op, '#666666') for op in fluxos['tipo_operacao']]

            import plotly.graph_objects as go
            import plotly.io as pio

            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=20,
                    thickness=30,
                    line=dict(color="black", width=0.5),
                    label=todas_labels,
                    color=cores_ops + cores_tipos
                ),
                link=dict(
                    source=fonte,
                    target=destino,
                    value=valores,
                    color=[f"rgba({int(c[1:3],16)}, {int(c[3:5],16)}, {int(c[5:7],16)}, 0.5)" for c in cores_links]
                )
            )])

            fig.update_layout(
                title_text=titulo,
                font_size=14,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=1600,               # largura em pixels para renderização
                height=900,               # altura em pixels para renderização
                margin=dict(l=100, r=100, t=100, b=100)  # margens reduzidas
            )

            try:
                img_bytes = pio.to_image(fig, format='png', width=1600, height=900, scale=2)

            except Exception as e:
                logger.error(f"Falha ao renderizar imagem com Kaleido: {e}", exc_info=True)
                plt.figure(figsize=(16, 9))
                mensagem = self.loc.get_text("plotly_required") if self.loc else 'Kaleido falhou ao renderizar o Diagrama de Sankey'
                plt.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=14)
                plt.axis('off')
                return plt.gcf()

            try:
                from io import BytesIO
                from PIL import Image
                img = Image.open(BytesIO(img_bytes)).convert("RGBA")
                plt.figure(figsize=(16, 9))
                plt.imshow(np.array(img))
                plt.axis('off')
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
                return plt.gcf()

            except Exception as e:
                logger.error(f"Falha ao exibir imagem PNG do Sankey: {e}", exc_info=True)
                plt.figure(figsize=(16, 9))
                plt.text(0.5, 0.5, f"Erro exibindo PNG: {e}", ha='center', va='center', fontsize=14)
                plt.axis('off')
                return plt.gcf()

        except Exception as e:
            logger.error(f"Sankey - Erro ao gerar diagrama de Sankey: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(f"{titulo} - Erro")
