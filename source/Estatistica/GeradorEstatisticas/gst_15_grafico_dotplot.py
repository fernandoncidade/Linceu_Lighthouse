import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from .gst_01_base_gerador import BaseGerador
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GraficoDotplot(BaseGerador):
    __slots__ = []

    def _parse_tamanho(self, tamanho_str):
        try:
            if pd.isna(tamanho_str) or tamanho_str == '':
                return None

            tamanho_str = str(tamanho_str).strip().lower()

            pattern = r'(\d+(?:[.,]\d+)?)\s*([a-z]*)'
            match = re.match(pattern, tamanho_str)

            if not match:
                return None

            numero_str = match.group(1).replace(',', '.')
            unidade = match.group(2)

            try:
                numero = float(numero_str)
            except ValueError:
                return None

            multiplicadores = {
                'b': 1,
                'kb': 1024,
                'mb': 1024**2,
                'gb': 1024**3,
                'tb': 1024**4
            }

            multiplicador = multiplicadores.get(unidade, 1)
            return int(numero * multiplicador)

        except Exception as e:
            logger.error(f"Dotplot - Erro ao parsear tamanho '{tamanho_str}': {e}", exc_info=True)
            return None

    def _extrair_tamanho_bytes(self, row):
        try:
            campos = [
                ('size_tb', 1024**4),
                ('size_gb', 1024**3),
                ('size_mb', 1024**2),
                ('size_kb', 1024),
                ('size_b', 1)
            ]
            for campo, fator in campos:
                valor = row.get(campo)
                if pd.notna(valor) and str(valor).strip() != '':
                    try:
                        return float(str(valor).replace(',', '.')) * fator

                    except Exception:
                        continue

            return None

        except Exception as e:
            logger.error(f"Dotplot - Erro ao extrair tamanho em bytes da linha: {e}", exc_info=True)
            return None

    def gerar(self):
        df = self._obter_dados()
        titulo = self.loc.get_text("file_size_distribution") if self.loc else 'Distribuição de Tamanhos de Arquivo'

        if df.empty:
            logger.warning("Dataset vazio para geração do dotplot")
            return self._criar_grafico_sem_dados(titulo)

        try:
            df['tamanho_bytes'] = df.apply(self._extrair_tamanho_bytes, axis=1)
            df_filtrado = df.dropna(subset=['tamanho_bytes'])

            tamanhos_invalidos = len(df) - len(df_filtrado)
            if tamanhos_invalidos > 0:
                pass

            df_filtrado = df_filtrado[df_filtrado['tamanho_bytes'] > 0]

            if len(df_filtrado) == 0:
                logger.warning("Dotplot - Nenhum registro com tamanho válido")
                return self._criar_grafico_sem_dados(self.loc.get_text("no_size_data") if self.loc else "Sem dados de tamanho disponíveis")

            df_filtrado['tamanho_mb'] = df_filtrado['tamanho_bytes'] / (1024 * 1024)

            tipos_top = df_filtrado['tipo'].value_counts().nlargest(8).index.tolist()
            df_plot = df_filtrado[df_filtrado['tipo'].isin(tipos_top)]

            limite_superior = df_plot['tamanho_mb'].quantile(0.95)
            df_plot = df_plot[df_plot['tamanho_mb'] <= limite_superior]

            for tipo in tipos_top:
                count = len(df_plot[df_plot['tipo'] == tipo])
                media = df_plot[df_plot['tipo'] == tipo]['tamanho_mb'].mean() if count > 0 else 0

            if len(df_plot) == 0:
                logger.warning("Dotplot - Sem dados suficientes após filtragem")
                return self._criar_grafico_sem_dados(
                    self.loc.get_text("insufficient_data_after_filtering") if self.loc else "Sem dados suficientes após filtragem"
                )

            plt.figure(figsize=(12, 8))

            posicoes = np.arange(len(tipos_top))
            cores = plt.cm.tab10(np.linspace(0, 1, len(tipos_top)))

            for i, tipo in enumerate(tipos_top):
                dados = df_plot[df_plot['tipo'] == tipo]['tamanho_mb']

                if len(dados) == 0:
                    continue

                x_jitter = np.random.normal(posicoes[i], 0.04, size=len(dados))

                plt.scatter(x_jitter, dados, color=cores[i], alpha=0.6, edgecolor='none', s=40)

                media = dados.mean()
                plt.hlines(y=media, xmin=posicoes[i]-0.2, xmax=posicoes[i]+0.2, color=cores[i], linestyle='-', linewidth=2)

            if df_plot['tamanho_mb'].max() / (df_plot['tamanho_mb'].min() + 0.001) > 100:
                plt.yscale('log')

            plt.xticks(posicoes, [t if len(t) < 15 else t[:12]+'...' for t in tipos_top], rotation=45, ha='right')
            plt.xlabel(self.loc.get_text("file_types") if self.loc else 'Tipos de Arquivo')
            plt.ylabel(self.loc.get_text("file_size_mb") if self.loc else 'Tamanho do Arquivo (MB)')
            plt.title(titulo)
            plt.grid(True, axis='y', alpha=0.3)

            plt.tight_layout()

            return plt.gcf()

        except Exception as e:
            logger.error(f"Dotplot - Erro ao gerar dot plot: {e}", exc_info=True)
            return self._criar_grafico_sem_dados(f"{titulo} - Erro: {str(e)}")
