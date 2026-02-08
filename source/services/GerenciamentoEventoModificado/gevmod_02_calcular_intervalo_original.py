import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _calcular_intervalo_original(self, caminho_completo):
    try:
        PESO_TAMANHO = 0.6
        PESO_FREQUENCIA = 0.4
        tamanho = os.path.getsize(caminho_completo)
        if tamanho > self.grande_arquivo_threshold:
            fator_tamanho = (tamanho / self.tamanho_threshold) ** 0.75

        else:
            fator_tamanho = (tamanho / self.tamanho_threshold) ** 0.5

        nome_arquivo = os.path.basename(caminho_completo)
        freq_mod = self.count_modificacoes.get(nome_arquivo, 0)
        fator_freq = max(0.2, 1.0 / (1 + freq_mod * 0.1))
        intervalo = (self.intervalo_base * (fator_tamanho * PESO_TAMANHO + fator_freq * PESO_FREQUENCIA))
        if tamanho > self.tamanho_threshold:
            intervalo *= 1.5

        return min(max(intervalo, self.min_intervalo), self.max_intervalo)

    except Exception as e:
        logger.error(f"Erro ao calcular intervalo original: {e}", exc_info=True)
        return self.max_intervalo
