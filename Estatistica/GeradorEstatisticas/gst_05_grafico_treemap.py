import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import squarify
from .gst_01_base_gerador import BaseGerador
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoTreemap(BaseGerador):
    __slots__ = []

    def gerar(self):
        try:
            df = self._obter_dados()
            titulo = self.loc.get_text("tree_map") if self.loc else 'Mapa de Árvore - Tipos de Arquivo'

            if df.empty:
                logger.warning("Dataset vazio para geração do treemap")
                return self._criar_grafico_sem_dados(titulo)

            tipos = df['tipo'].value_counts()[:30]

            if not tipos.empty:
                plt.figure(figsize=(12, 8))
                squarify.plot(sizes=tipos.values, label=tipos.index, alpha=0.6)
                plt.title(titulo)
                plt.axis('off')

            else:
                logger.warning("Nenhum tipo de arquivo encontrado para gerar o treemap")

            return plt.gcf()

        except Exception as e:
            logger.error(f"Erro ao gerar treemap: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(titulo if 'titulo' in locals() else "Mapa de Árvore - Tipos de Arquivo")
