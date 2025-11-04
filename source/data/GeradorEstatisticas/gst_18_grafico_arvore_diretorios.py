import os
import sqlite3
import importlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from .gst_01_base_gerador import BaseGerador
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoArvoreDiretorios(BaseGerador):
    __slots__ = ()

    def gerar(self, max_depth=6, max_nodes=300):
        titulo = self.loc.get_text("directory_tree") if self.loc else "Árvore de Diretórios"
        try:
            dirs = self._carregar_diretorios()
            if not dirs:
                return self._criar_grafico_sem_dados(titulo)

            raiz = self._obter_raiz(dirs)
            if not raiz:
                return self._criar_grafico_sem_dados(titulo)

            nodes, links = self._construir_arvore(dirs, raiz, max_depth, max_nodes)
            if not nodes or not links:
                return self._criar_grafico_sem_dados(titulo)

            idx = {p: i for i, p in enumerate(nodes)}

            labels, cores_nodes, depth_map = self._criar_rotulos_e_cores(nodes, raiz)

            fonte = [idx[p] for (p, c, v) in links if p in idx and c in idx]
            destino = [idx[c] for (p, c, v) in links if p in idx and c in idx]
            valores = [max(1, int(v)) for (_, _, v) in links]

            cores_links = []
            for (_, c, _) in links:
                d = depth_map.get(c, 0)
                color = cores_nodes[depth_map.get(c, 0) % len(cores_nodes)]
                rgba = mcolors.to_rgba(color, 0.5)
                cores_links.append(f"rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]:.2f})")

            try:
                import plotly.graph_objects as go
                import plotly.io as pio

                try:
                    kaleido_mod = importlib.import_module("kaleido")
                    exe_name = "kaleido.exe" if os.name == "nt" else "kaleido"
                    env_exe = os.environ.get("KALEIDO_EXECUTABLE")
                    cand = []
                    if env_exe:
                        cand.append(env_exe)

                    cand.append(os.path.join(os.path.dirname(kaleido_mod.__file__), "executable", exe_name))
                    exe_path = next((p for p in cand if p and os.path.exists(p)), None)
                    if exe_path:
                        try:
                            scopes_mod = importlib.import_module("kaleido.scopes.plotly")
                            PlotlyScope = getattr(scopes_mod, "PlotlyScope", None)
                            if PlotlyScope and not getattr(getattr(pio, "kaleido", None), "scope", None):
                                pio.kaleido.scope = PlotlyScope(executable=exe_path)

                        except Exception as e:
                            logger.warning(f"Falha ao configurar Kaleido PlotlyScope: {e}")

                    else:
                        logger.warning("Executável do Kaleido não encontrado (defina KALEIDO_EXECUTABLE).")

                except ModuleNotFoundError:
                    logger.warning("Kaleido não disponível; plotly.io.to_image pode falhar.")

                except Exception as e:
                    logger.warning(f"Kaleido falhou ao carregar: {e}")

                fig_p = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=18,
                        thickness=24,
                        line=dict(color="black", width=0.3),
                        label=labels,
                        color=cores_nodes
                    ),
                    link=dict(
                        source=fonte,
                        target=destino,
                        value=valores,
                        color=cores_links
                    )
                )])

                titulo_plot = f"{titulo} — {self.loc.get_text('root') if self.loc else 'Raiz'}: {self._encurtar_path(raiz, 60)}"
                fig_p.update_layout(
                    title_text=titulo_plot,
                    font_size=13,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    width=1600,
                    height=900,
                    margin=dict(l=40, r=40, t=80, b=40)
                )

                try:
                    img_bytes = pio.to_image(fig_p, format='png', width=1600, height=900, scale=2)

                except Exception as e:
                    logger.error(f"Falha ao renderizar imagem com Kaleido: {e}", exc_info=True)
                    plt.figure(figsize=(16, 9))
                    plt.text(0.5, 0.5, self.loc.get_text("plotly_required") if self.loc else "Kaleido falhou ao renderizar o diagrama", ha='center', va='center', fontsize=14)
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
                mensagem = self.loc.get_text("plotly_required") if self.loc else 'Biblioteca plotly/kaleido necessária para gerar o diagrama'
                plt.text(0.5, 0.5, mensagem, ha='center', va='center', fontsize=14)
                plt.axis('off')
                return plt.gcf()

        except Exception as e:
            logger.error(f"Árvore de Diretórios - Erro ao gerar: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(f"{titulo} - Erro")

    def _carregar_diretorios(self):
        try:
            db_uri = f'file:{self.db_path}?mode=ro&cache=shared'
            with sqlite3.connect(db_uri, uri=True, timeout=30) as conn:
                conn.execute("PRAGMA journal_mode=WAL")
                df = pd.read_sql_query("SELECT * FROM monitoramento WHERE timestamp IS NOT NULL", conn)

        except Exception as e:
            logger.error(f"Erro lendo base para diretórios: {e}", exc_info=True)
            return []

        if df.empty:
            return []

        dir_cols = [
            'dir_atual', 'directory', 'dir', 'current_dir',
            'dir_anterior', 'previous_dir', 'old_dir', 'dir_old'
        ]

        diretores = []
        for col in dir_cols:
            if col in df.columns:
                vals = df[col].dropna().astype(str).tolist()
                diretores.extend(vals)

        norm = []
        for p in diretores:
            p = p.strip()
            if not p:
                continue

            try:
                norm.append(os.path.normpath(p))

            except Exception:
                norm.append(p)

        return sorted(set([p for p in norm if p not in ('', '.', os.sep)]))

    def _obter_raiz(self, paths):
        try:
            if not paths:
                return None

            raiz = None
            try:
                raiz = os.path.commonpath(paths)

            except Exception:
                drives = {}
                for p in paths:
                    drive = os.path.splitdrive(p)[0] if os.name == 'nt' else '/'
                    drives.setdefault(drive, 0)
                    drives[drive] += 1

                drive_mais_comum = max(drives.items(), key=lambda x: x[1])[0]
                cand = [p for p in paths if (os.path.splitdrive(p)[0] if os.name == 'nt' else '/').startswith(drive_mais_comum)]
                raiz = os.path.commonpath(cand) if cand else (drive_mais_comum if drive_mais_comum else None)

            if raiz and raiz.endswith(':'):
                raiz = raiz + os.sep

            return raiz

        except Exception as e:
            logger.warning(f"Falha ao obter raiz: {e}")
            return None

    def _construir_arvore(self, dirs, raiz, max_depth, max_nodes):
        try:
            nodes = [raiz]
            links = []
            node_set = {raiz}
            link_count = {}

            def join_rel(parts):
                p = raiz
                for part in parts:
                    p = os.path.join(p, part)

                return os.path.normpath(p)

            for d in dirs:
                if not d.startswith(raiz):
                    continue

                rel = os.path.relpath(d, raiz)
                if rel == '.' or rel.startswith('..'):
                    continue

                parts = [p for p in rel.replace('/', os.sep).split(os.sep) if p]
                parts = parts[:max_depth]
                for i in range(len(parts)):
                    parent = raiz if i == 0 else join_rel(parts[:i])
                    child = join_rel(parts[:i+1])
                    if child not in node_set:
                        nodes.append(child)
                        node_set.add(child)
                        if len(nodes) >= max_nodes:
                            break

                    key = (parent, child)
                    link_count[key] = link_count.get(key, 0) + 1

                if len(nodes) >= max_nodes:
                    break

            nodes = self._ordenar_por_profundidade(nodes, raiz)
            for (p, c), v in link_count.items():
                if p in nodes and c in nodes:
                    links.append((p, c, v))

            return nodes, links

        except Exception as e:
            logger.error(f"Erro ao construir árvore: {e}", exc_info=True)
            return [], []

    def _ordenar_por_profundidade(self, nodes, raiz):
        def depth(p):
            if p == raiz:
                return 0

            try:
                rel = os.path.relpath(p, raiz)
                if rel in ('.', '..') or rel.startswith('..'):
                    return 0

                return len([x for x in rel.split(os.sep) if x])

            except Exception:
                return 0

        return sorted(nodes, key=lambda p: (depth(p), p.lower()))

    def _criar_rotulos_e_cores(self, nodes, raiz):
        depth_map = {}
        max_depth = 1
        for p in nodes:
            if p == raiz:
                d = 0

            else:
                try:
                    rel = os.path.relpath(p, raiz)
                    d = len([x for x in rel.split(os.sep) if x and x != '.'])

                except Exception:
                    d = 0

            depth_map[p] = d
            max_depth = max(max_depth, d)

        cores = self._gerar_cores(max_depth + 1, cmap_name='tab20')
        cores_nodes = [cores[depth_map[p] % len(cores)] for p in nodes]
        base_names = [self._nome_pasta_legivel(p, raiz) for p in nodes]
        counts = {}
        labels = []
        for name, full in zip(base_names, nodes):
            cnt = counts.get(name, 0)
            label = name if cnt == 0 else f"{name} ({cnt})"
            counts[name] = cnt + 1
            labels.append(label)

        return labels, cores_nodes, depth_map

    def _nome_pasta_legivel(self, path, raiz):
        if path == raiz:
            return self._encurtar_path(os.path.basename(os.path.normpath(raiz)) or raiz, 20)

        base = os.path.basename(os.path.normpath(path))
        return self._encurtar_path(base or path, 20)

    def _encurtar_path(self, p, max_len=60):
        if not isinstance(p, str):
            return str(p)

        s = p.replace('/', os.sep).replace('\\', os.sep)
        if len(s) <= max_len:
            return s

        return s[:max_len-3] + '...'

    def _gerar_cores(self, n: int, cmap_name: str = 'tab20') -> list:
        try:
            import matplotlib.cm as cm
            cmap = cm.get_cmap(cmap_name)
            cores = []
            for i in range(max(1, n)):
                c = cmap(i / max(1, n - 1))
                cores.append(mcolors.to_hex(c))

            return cores

        except Exception as e:
            logger.warning(f"Falha ao gerar cores: {e}")
            return ['#1f77b4'] * max(1, n)
