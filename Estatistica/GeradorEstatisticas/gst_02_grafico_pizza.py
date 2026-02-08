import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from .gst_01_base_gerador import BaseGerador
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoPizza(BaseGerador):
    __slots__ = []

    def _calcular_luminosidade(self, cor_hex):
        try:
            if cor_hex.startswith('#'):
                cor_hex = cor_hex[1:]

            try:
                r = int(cor_hex[0:2], 16) / 255.0
                g = int(cor_hex[2:4], 16) / 255.0
                b = int(cor_hex[4:6], 16) / 255.0

            except (IndexError, ValueError):
                logger.warning(f"Cor inválida: {cor_hex}, usando valor padrão")
                return 0.5

            return 0.299 * r + 0.587 * g + 0.114 * b

        except Exception as e:
            logger.error(f"Erro ao calcular luminosidade: {e}", exc_info=True)
            return 0.5

    def _obter_cor_texto(self, cor_bg):
        try:
            luminosidade = self._calcular_luminosidade(cor_bg)
            return 'white' if luminosidade < 0.5 else 'black'

        except Exception as e:
            logger.error(f"Erro ao obter cor do texto: {e}", exc_info=True)
            return 'black'

    def gerar(self):
        try:
            df = self._obter_dados()
            titulo = self.loc.get_text("operations_pie") if self.loc else 'Distribuição de Operações'

            if df.empty:
                logger.warning("Dataset vazio para geração do gráfico de pizza")
                return self._criar_grafico_sem_dados(titulo)

            plt.figure(figsize=(10, 8))
            contagem = df['tipo_operacao'].value_counts()

            if not contagem.empty:
                cores = [self.cores_operacoes.get(op, '#333333') for op in contagem.index]

                wedges, texts, autotexts = plt.pie(contagem, labels=contagem.index, autopct='%1.1f%%', colors=cores)

                for i, autotext in enumerate(autotexts):
                    cor_texto = self._obter_cor_texto(cores[i])
                    autotext.set_color(cor_texto)

                plt.title(titulo)

            else:
                logger.warning("Nenhuma operação encontrada para gerar o gráfico de pizza")

            return plt.gcf()

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de pizza: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(titulo if 'titulo' in locals() else "Distribuição de Operações")
