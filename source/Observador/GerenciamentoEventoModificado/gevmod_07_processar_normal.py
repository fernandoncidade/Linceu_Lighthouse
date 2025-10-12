import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_normal(self, nome_arquivo, caminho_completo, tempo_atual):
    try:
        ext = os.path.splitext(nome_arquivo)[1].lower()
        if nome_arquivo in self.observador.arquivos_recem_renomeados:
            tempo_renomeacao = self.observador.arquivos_recem_renomeados[nome_arquivo]
            try:
                tamanho = os.path.getsize(caminho_completo)

                if ext in self.EXTENSOES_VIDEO:
                    tempo_espera = min(60, max(5.0, tamanho / (20 * 1024 * 1024)))

                else:
                    tempo_espera = self.tempo_espera_grande_arquivo

                if (tempo_atual - tempo_renomeacao) < tempo_espera:
                    return False

                else:
                    del self.observador.arquivos_recem_renomeados[nome_arquivo]

            except Exception as e:
                logger.error(f"Erro ao processar arquivo renomeado: {e}", exc_info=True)
                del self.observador.arquivos_recem_renomeados[nome_arquivo]

        tamanho = os.path.getsize(caminho_completo)
        if ext == '.log':
            if nome_arquivo in self.observador.arquivos_recem_adicionados:
                tempo_adicao = self.observador.arquivos_recem_adicionados[nome_arquivo]
                if (tempo_atual - tempo_adicao) < 2.0:
                    return False

            intervalo = min(self.min_intervalo, 0.5)
            if nome_arquivo in self.observador.ultima_modificacao:
                ultimo_tempo = self.observador.ultima_modificacao[nome_arquivo]
                if (tempo_atual - ultimo_tempo) < intervalo:
                    return False

            self.modificacoes_recentes[nome_arquivo] = tempo_atual
            self.count_modificacoes[nome_arquivo] = self.count_modificacoes.get(nome_arquivo, 0) + 1
            self.observador.ultima_modificacao[nome_arquivo] = tempo_atual
            self._limpar_cache_metadados(caminho_completo, ext)
            self.notificar_evento(self.observador.loc.get_text("op_modified"), nome_arquivo, caminho_completo, caminho_completo)
            return True

        if ext in self.EXTENSOES_VIDEO:
            if nome_arquivo in self.observador.arquivos_recem_adicionados:
                tempo_adicao = self.observador.arquivos_recem_adicionados[nome_arquivo]
                tempo_espera_video = min(120, max(10.0, tamanho / (10 * 1024 * 1024)))
                if (tempo_atual - tempo_adicao) < tempo_espera_video:
                    return False

        is_codigo_grande = self.is_arquivo_codigo_grande(caminho_completo)
        if is_codigo_grande:
            self.arquivos_em_processamento.add(caminho_completo)
            intervalo = max(self.max_intervalo, self.tempo_espera_grande_arquivo * 2)
            if nome_arquivo in self.observador.ultima_modificacao:
                ultimo_tempo = self.observador.ultima_modificacao[nome_arquivo]
                if (tempo_atual - ultimo_tempo) < intervalo:
                    return False

        else:
            if tamanho > self.grande_arquivo_threshold:
                if nome_arquivo in self.observador.arquivos_recem_adicionados:
                    tempo_adicao = self.observador.arquivos_recem_adicionados[nome_arquivo]
                    if ext in self.EXTENSOES_VIDEO:
                        tempo_extra = min(120, max(10.0, tamanho / (10 * 1024 * 1024)))

                    else:
                        tempo_extra = self.tempo_espera_grande_arquivo

                    if (tempo_atual - tempo_adicao) < tempo_extra:
                        return False

                if nome_arquivo in self.eventos_grandes:
                    ultimo_evento = self.eventos_grandes[nome_arquivo]
                    if (tempo_atual - ultimo_evento) < self.tempo_espera_grande_arquivo:
                        return False

                self.eventos_grandes[nome_arquivo] = tempo_atual

            intervalo = self.calcular_intervalo(caminho_completo)

        if nome_arquivo in self.observador.arquivos_recem_excluidos:
            ultima_exclusao = self.observador.arquivos_recem_excluidos[nome_arquivo]
            if (tempo_atual - ultima_exclusao) < self.exclusao_threshold:
                return False

        if nome_arquivo in self.observador.arquivos_recem_adicionados and ext not in self.EXTENSOES_VIDEO:
            tempo_adicao = self.observador.arquivos_recem_adicionados[nome_arquivo]
            if (tempo_atual - tempo_adicao) < intervalo:
                return False

        if not is_codigo_grande:
            if nome_arquivo in self.observador.ultima_modificacao:
                ultimo_tempo = self.observador.ultima_modificacao[nome_arquivo]
                if (tempo_atual - ultimo_tempo) < intervalo:
                    return False

        self.modificacoes_recentes[nome_arquivo] = tempo_atual
        self.count_modificacoes[nome_arquivo] = self.count_modificacoes.get(nome_arquivo, 0) + 1
        self.observador.ultima_modificacao[nome_arquivo] = tempo_atual
        self._limpar_cache_metadados(caminho_completo, ext)
        self.notificar_evento(self.observador.loc.get_text("op_modified"), nome_arquivo, caminho_completo, caminho_completo)
        if is_codigo_grande:
            self.arquivos_em_processamento.remove(caminho_completo)

        return True

    except Exception as e:
        if caminho_completo in self.arquivos_em_processamento:
            self.arquivos_em_processamento.remove(caminho_completo)

        logger.error(f"Erro ao processar modificação: {e}", exc_info=True)
        return False
