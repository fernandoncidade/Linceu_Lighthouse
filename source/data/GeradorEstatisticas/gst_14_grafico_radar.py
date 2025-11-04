import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import numpy as np
from .gst_01_base_gerador import BaseGerador
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoRadar(BaseGerador):
    __slots__ = []

    def gerar(self):
        df = self._obter_dados()
        titulo = self.loc.get_text("operations_by_file_type") if self.loc else 'Operações por Tipo de Arquivo'

        if df.empty:
            logger.warning("Dataset vazio para geração do gráfico radar")
            return self._criar_grafico_sem_dados(titulo)

        try:
            df_radar = df[['tipo_operacao', 'tipo']].copy()
            df_radar = df_radar.dropna()

            registros_removidos = len(df) - len(df_radar)
            if registros_removidos > 0:
                pass

            if df_radar.empty:
                logger.warning("Radar - Sem dados válidos após filtrar valores nulos")
                return self._criar_grafico_sem_dados(titulo)

            tipos_top = df_radar['tipo'].value_counts().nlargest(10).index.tolist()
            operacoes = [self.loc.get_text('op_added'), 
                         self.loc.get_text('op_deleted'), 
                         self.loc.get_text('op_renamed'), 
                         self.loc.get_text('op_modified'), 
                         self.loc.get_text('op_moved'), 
                         self.loc.get_text('op_scanned')]

            n_operacoes = len(operacoes)
            n_cols = 3
            n_rows = int(np.ceil(n_operacoes / n_cols))
            fig, axs = plt.subplots(n_rows, n_cols, figsize=(16, 8), subplot_kw={'projection': 'polar'})
            axs = axs.flatten()

            angulos = np.linspace(0, 2*np.pi, len(tipos_top), endpoint=False).tolist()
            angulos += angulos[:1]
            tipos_top_show = [t if len(t) < 15 else t[:12] + '...' for t in tipos_top]

            for idx, operacao in enumerate(operacoes):
                matriz = []
                for tipo in tipos_top:
                    count = len(df_radar[(df_radar['tipo_operacao'] == operacao) & (df_radar['tipo'] == tipo)])
                    matriz.append(count)

                matriz = np.array(matriz)
                total = matriz.sum()
                valores = (matriz / total * 100) if total > 0 else np.zeros_like(matriz)
                valores = valores.tolist()
                valores += valores[:1]

                cor = self.cores_operacoes.get(operacao, '#333333')
                ax = axs[idx]
                ax.plot(angulos, valores, linewidth=2, linestyle='solid', label=operacao, color=cor)
                ax.fill(angulos, valores, alpha=0.1, color=cor)
                ax.set_theta_offset(np.pi / 2)
                ax.set_theta_direction(-1)
                ax.set_xticks(angulos[:-1])
                ax.set_xticklabels(tipos_top_show)
                ax.yaxis.grid(True)
                ax.set_ylim(0, 100)
                ax.set_title(f"{titulo} - {operacao}", y=1.08)
                ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

            for i in range(len(operacoes), len(axs)):
                fig.delaxes(axs[i])

            plt.tight_layout()
            return plt.gcf()

        except Exception as e:
            logger.error(f"Radar - Erro ao gerar gráfico de radar: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(f"{titulo} - Erro: {str(e)}")
