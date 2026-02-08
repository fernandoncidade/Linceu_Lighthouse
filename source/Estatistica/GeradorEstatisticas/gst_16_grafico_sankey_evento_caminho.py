import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from .gst_01_base_gerador import BaseGerador
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoSankeyEventoCaminho(BaseGerador):
    __slots__ = ()

    def gerar(self, top_n_destinos=50):
        titulo = self.loc.get_text("event_to_path_flow") if self.loc else 'Fluxo: Evento → Caminho'
        try:
            df = self._carregar_evento_caminho()
            if df.empty:
                return self._criar_grafico_sem_dados(titulo)

            top_destinos = df['caminho'].value_counts().nlargest(top_n_destinos).index.tolist()
            df = df[df['caminho'].isin(top_destinos)]
            if df.empty:
                return self._criar_grafico_sem_dados(titulo)

            fluxos = df.groupby(['evento', 'caminho']).size().reset_index(name='valor')

            eventos = fluxos['evento'].drop_duplicates().tolist()
            caminhos = fluxos['caminho'].drop_duplicates().tolist()

            caminho_to_short = {}
            short_counts = {}
            caminho_labels = []
            for p in caminhos:
                short = self._encurtar_label(p)
                cnt = short_counts.get(short, 0)
                label = f"{short}" if cnt == 0 else f"{short} ({cnt})"
                short_counts[short] = cnt + 1
                caminho_to_short[p] = label
                caminho_labels.append(label)

            labels = eventos + caminho_labels

            idx_evento = {ev: i for i, ev in enumerate(eventos)}
            idx_caminho = {p: len(eventos) + i for i, p in enumerate(caminhos)}

            fonte = [idx_evento[row['evento']] for _, row in fluxos.iterrows()]
            destino = [idx_caminho[row['caminho']] for _, row in fluxos.iterrows()]
            valores = fluxos['valor'].tolist()

            cores_ops = []
            missing_ops = []
            for ev in eventos:
                c = self.cores_operacoes.get(ev)
                if not c:
                    missing_ops.append(ev)
                    cores_ops.append(None)

                else:
                    cores_ops.append(c)

            if missing_ops:
                gen = self._gerar_cores(len(missing_ops), cmap_name='tab10')
                gi = 0
                for i, ev in enumerate(eventos):
                    if cores_ops[i] is None:
                        cores_ops[i] = gen[gi]; gi += 1

            cores_paths = self._gerar_cores(len(caminhos), cmap_name='tab20')
            cores_links = [mcolors.to_hex(mcolors.to_rgba(self.cores_operacoes.get(ev, '#666666'), 0.5)) for ev in fluxos['evento']]

            try:
                import os as _os
                import importlib
                import plotly.graph_objects as go
                import plotly.io as pio

                try:
                    kaleido_mod = importlib.import_module("kaleido")
                    exe_name = "kaleido.exe" if _os.name == "nt" else "kaleido"
                    env_exe = _os.environ.get("KALEIDO_EXECUTABLE")
                    candidatos = []
                    if env_exe:
                        candidatos.append(env_exe)

                    candidatos.append(_os.path.join(_os.path.dirname(kaleido_mod.__file__), "executable", exe_name))
                    exe_path = next((p for p in candidatos if p and _os.path.exists(p)), None)
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

                import plotly.graph_objects as go
                import plotly.io as pio

                fig_p = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=20,
                        thickness=30,
                        line=dict(color="black", width=0.5),
                        label=labels,
                        color=cores_ops + cores_paths
                    ),
                    link=dict(
                        source=fonte,
                        target=destino,
                        value=valores,
                        color=[f"rgba({int(c[1:3],16)}, {int(c[3:5],16)}, {int(c[5:7],16)}, 0.5)" for c in cores_links]
                    )
                )])

                fig_p.update_layout(
                    title_text=titulo,
                    font_size=14,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    width=1600,               # largura em pixels para renderização
                    height=900,               # altura em pixels para renderização
                    margin=dict(l=100, r=100, t=100, b=100)  # margens reduzidas
                )

                try:
                    img_bytes = pio.to_image(fig_p, format='png', width=1600, height=900, scale=2)

                except Exception as e:
                    logger.error(f"Falha ao renderizar imagem com Kaleido: {e}", exc_info=True)
                    plt.figure(figsize=(16, 9))
                    mensagem = self.loc.get_text("plotly_required") if self.loc else 'Kaleido falhou ao renderizar o Diagrama de Sankey'
                    plt.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=14)
                    plt.axis('off')
                    return plt.gcf()

                from io import BytesIO
                from PIL import Image
                img = Image.open(BytesIO(img_bytes)).convert("RGBA")
                fig, ax = plt.subplots(figsize=(16, 9))
                ax.imshow(np.array(img))
                ax.axis('off')
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
                return fig

            except Exception as e:
                logger.error(f"Falha ao importar/usar Plotly/Kaleido: {e}", exc_info=True)
                plt.figure(figsize=(16, 9))
                mensagem = self.loc.get_text("plotly_required") if self.loc else 'Biblioteca plotly/kaleido necessária para gerar o Diagrama de Sankey'
                plt.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=14)
                plt.axis('off')
                return plt.gcf()

        except Exception as e:
            logger.error(f"Sankey Evento→Caminho - Erro ao gerar: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(f"{titulo} - Erro")

    def _carregar_evento_caminho(self) -> pd.DataFrame:
        try:
            db_uri = f'file:{self.db_path}?mode=ro&cache=shared'
            with sqlite3.connect(db_uri, uri=True, timeout=30) as conn:
                conn.execute("PRAGMA journal_mode=WAL")
                df_all = pd.read_sql_query("SELECT * FROM monitoramento WHERE timestamp IS NOT NULL", conn)

        except Exception as e:
            logger.error(f"Erro lendo base (evento→caminho): {e}", exc_info=True)
            return pd.DataFrame()

        if df_all.empty:
            return df_all

        tipo_col = next((c for c in ['tipo_operacao', 'operacao', 'operation', 'evento', 'event'] if c in df_all.columns), None)
        dir_atual_col = next((c for c in ['dir_atual', 'dir', 'current_dir', 'directory'] if c in df_all.columns), None)
        dir_anterior_col = next((c for c in ['dir_anterior', 'dir_old', 'previous_dir', 'old_dir'] if c in df_all.columns), None)
        nome_col = next((c for c in ['nome', 'arquivo', 'name', 'file'] if c in df_all.columns), None)
        nome_anterior_col = next((c for c in ['nome_anterior', 'nome_old', 'old_name', 'previous_name'] if c in df_all.columns), None)

        if not tipo_col:
            logger.error("Coluna de tipo/operacao não encontrada na tabela monitoramento.")
            return pd.DataFrame()

        records = []
        try:
            mapa = self._obter_mapeamento_operacoes()

        except Exception:
            mapa = {}

        for _, row in df_all.iterrows():
            evento_raw = row.get(tipo_col)
            evento = mapa.get(evento_raw, evento_raw)

            dir_atual = str(row.get(dir_atual_col, '') or '') if dir_atual_col else ''
            nome = str(row.get(nome_col, '') or '') if nome_col else ''
            caminho_atual = ''
            if dir_atual or nome:
                caminho_atual = os.path.normpath(os.path.join(dir_atual, nome)) if nome or dir_atual else ''
                if caminho_atual in ('.', ''):
                    caminho_atual = ''

            if caminho_atual:
                records.append({'evento': evento, 'caminho': caminho_atual})

            dir_ant = str(row.get(dir_anterior_col, '') or '') if dir_anterior_col else ''
            nome_ant = str(row.get(nome_anterior_col, '') or '') if nome_anterior_col else ''

            caminho_anterior = ''
            if dir_ant or nome_ant:
                caminho_anterior = os.path.normpath(os.path.join(dir_ant, nome_ant or nome)) if (dir_ant or nome_ant or nome) else ''
                if caminho_anterior in ('.', ''):
                    caminho_anterior = ''

            if caminho_anterior and caminho_anterior != caminho_atual:
                records.append({'evento': evento, 'caminho': caminho_anterior})

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        df['caminho'] = df['caminho'].replace(['', '.'], np.nan)
        return df[['evento', 'caminho']].dropna()

    def _cor_tipo(self, i: int) -> str:
         pal = [
             (55,126,184),(77,175,74),(228,26,28),(152,78,163),(255,127,0),
             (166,86,40),(247,129,191),(153,153,153),(255,255,51),(166,206,227)
         ]
         r, g, b = pal[i % len(pal)]
         return f"#{r:02x}{g:02x}{b:02x}"

    def _gerar_cores(self, n: int, cmap_name: str = 'tab20') -> list:
        if n <= 0:
            return []

        try:
            cmap = plt.get_cmap(cmap_name)
            if n == 1:
                rgba = cmap(0.5)
                return [mcolors.to_hex(rgba)]

            cores = []
            for i in range(n):
                rgba = cmap(i / max(1, n - 1))
                cores.append(mcolors.to_hex(rgba))

            return cores

        except Exception:
            return [self._cor_tipo(i) for i in range(n)]

    def _encurtar_label(self, path: str, max_len: int = 60) -> str:
        if not isinstance(path, str):
            return str(path)

        p = path.replace('/', '\\')
        if len(p) <= max_len:
            return p

        base = os.path.basename(p)
        if len(base) >= max_len - 3:
            return '...' + base[-(max_len-3):]

        prefix_len = max_len - 3 - len(base)
        return p[:prefix_len] + '...' + base
