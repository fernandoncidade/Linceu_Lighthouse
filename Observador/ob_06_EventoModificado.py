import os
from .ob_02_BaseEvento import BaseEvento


class EventoModificado(BaseEvento):
    def __init__(self, observador):
        super().__init__(observador)
        self.intervalo_base = 0.1
        self.tamanho_threshold = 100 * 1024 * 1024
        self.max_intervalo = 5
        self.exclusao_threshold = 0.1
        self.min_intervalo = 0.01
        self.modificacoes_recentes = {}
        self.count_modificacoes = {}
        self.eventos_grandes = {}
        self.grande_arquivo_threshold = 50 * 1024 * 1024
        self.tempo_espera_grande_arquivo = 3
        self.arquivos_em_processamento = set()

        self.EXTENSOES_VIDEO = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mts', '.m2ts', '.mpeg', '.m4v'}

        self.EXTENSOES_RAPIDAS = {'.txt', '.log', '.json', '.xml', '.csv', '.ini', '.cfg', '.conf', '.dat'}

        self.EXTENSOES_CODIGO = {'.tmp', '.temp', '.~', '.bak', '.swp', '.swo', '.$$', '.old', '.part', '.cache', 
                                 '.crdownload', '.download', '.partial', '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
                                 '.tiff', '.tif', '.psd', '.svg', '.webp', '.raw', '.heic', '.heif', '.cr2', '.nef', 
                                 '.arw', '.wav', '.mp3', '.aac', '.flac', '.ogg', '.aiff', '.wma', '.m4a', '.aif',  
                                 '.py', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.js', '.html', '.htm', 
                                 '.mht', '.xhtml', '.mhml', '.css', '.php', '.sql', '.json', '.xml', '.yaml', '.yml', 
                                 '.ini', '.cfg', '.conf', '.log', '.md', '.rst', '.bat', '.sh', '.ps1', '.psm1', 
                                 '.psd1', '.ps1xml', '.pssc', '.psc1', '.doc', '.docx', '.pdf', '.rtf', '.txt', 
                                 '.odt', '.wpd', '.pages', '.xls', '.xlsx', '.ods', '.csv', '.tsv', '.numbers', 
                                 '.ppt', '.pptx', '.odp', '.key', '.db', '.sqlite', '.mdb', '.accdb', '.sav', 
                                 '.spss', '.exe', '.dll', '.bin', '.app', '.apk', '.msi', '.run', '.bat', '.cmd', 
                                 '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.cab', '.dat'}

        self.CODIGO_LINHA_THRESHOLD = 1000

    def calcular_intervalo(self, caminho_completo):
        try:
            ext = os.path.splitext(caminho_completo)[1].lower()

            if ext in self.EXTENSOES_RAPIDAS:
                return self.min_intervalo

            if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada:
                return self.min_intervalo

            tamanho = os.path.getsize(caminho_completo)

            if tamanho > self.grande_arquivo_threshold:
                return min(self.tempo_espera_grande_arquivo, 1.0)

            return self._calcular_intervalo_original(caminho_completo)

        except Exception as e:
            print(f"Erro ao calcular intervalo: {e}")
            return self.min_intervalo

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
            print(f"Erro ao calcular intervalo original: {e}")
            return self.max_intervalo

    def is_arquivo_codigo_grande(self, caminho):
        try:
            ext = os.path.splitext(caminho)[1].lower()
            if ext not in self.EXTENSOES_CODIGO:
                return False

            if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada:
                return False

            with open(caminho, 'rb') as f:
                return sum(1 for _ in f) > self.CODIGO_LINHA_THRESHOLD

        except:
            return False

    def _limpar_cache_metadados(self, caminho_completo, ext):
        try:
            if ext == '.txt' and hasattr(self.observador, 'gerenciador_colunas'):
                if hasattr(self.observador.gerenciador_colunas, 'cache_metadados'):
                    with self.observador.gerenciador_colunas.lock_cache:
                        if caminho_completo in self.observador.gerenciador_colunas.cache_metadados:
                            del self.observador.gerenciador_colunas.cache_metadados[caminho_completo]

                if hasattr(self.observador.gerenciador_colunas, 'metadados_cache'):
                    if caminho_completo in self.observador.gerenciador_colunas.metadados_cache:
                        del self.observador.gerenciador_colunas.metadados_cache[caminho_completo]

            if hasattr(self.observador, 'gerenciador_colunas'):
                if hasattr(self.observador.gerenciador_colunas, 'cache_metadados'):
                    with self.observador.gerenciador_colunas.lock_cache:
                        if caminho_completo in self.observador.gerenciador_colunas.cache_metadados:
                            del self.observador.gerenciador_colunas.cache_metadados[caminho_completo]

                if hasattr(self.observador.gerenciador_colunas, 'metadados_cache'):
                    if caminho_completo in self.observador.gerenciador_colunas.metadados_cache:
                        del self.observador.gerenciador_colunas.metadados_cache[caminho_completo]

        except Exception as e:
            print(f"Erro ao limpar cache de metadados: {e}")

    def processar(self, nome_arquivo, caminho_completo, tempo_atual):
        if not os.path.exists(caminho_completo):
            return False

        if nome_arquivo.startswith(('~$', '.')):
            return False

        if caminho_completo in self.arquivos_em_processamento:
            return False

        ext = os.path.splitext(nome_arquivo)[1].lower()
        if ext in self.EXTENSOES_VIDEO:
            if nome_arquivo in self.observador.arquivos_recem_adicionados:
                tempo_adicao = self.observador.arquivos_recem_adicionados[nome_arquivo]
                try:
                    tamanho = os.path.getsize(caminho_completo)
                    tempo_espera_video = min(120, max(10.0, tamanho / (10 * 1024 * 1024)))

                    if (tempo_atual - tempo_adicao) < tempo_espera_video:
                        return False

                    else:
                        del self.observador.arquivos_recem_adicionados[nome_arquivo]

                except Exception as e:
                    print(f"Erro ao verificar arquivo de vídeo: {e}")
                    if (tempo_atual - tempo_adicao) < 30.0:
                        return False

        if nome_arquivo in self.observador.arquivos_recem_renomeados:
            tempo_renomeacao = self.observador.arquivos_recem_renomeados[nome_arquivo]
            tempo_espera = 2.0 if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada else 1.0

            if (tempo_atual - tempo_renomeacao) < tempo_espera:
                return False

            else:
                del self.observador.arquivos_recem_renomeados[nome_arquivo]

        if nome_arquivo in self.observador.arquivos_recem_adicionados and ext not in self.EXTENSOES_VIDEO:
            tempo_adicao = self.observador.arquivos_recem_adicionados[nome_arquivo]
            if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada:
                if (tempo_atual - tempo_adicao) < 1.5:
                    return False

        if hasattr(self.observador, 'operacao_massiva_detectada') and self.observador.operacao_massiva_detectada:
            return self._processar_massivo(nome_arquivo, caminho_completo, tempo_atual)

        else:
            return self._processar_normal(nome_arquivo, caminho_completo, tempo_atual)

    def _processar_massivo(self, nome_arquivo, caminho_completo, tempo_atual):
        try:
            if nome_arquivo in self.observador.ultima_modificacao:
                ultimo_tempo = self.observador.ultima_modificacao[nome_arquivo]
                if (tempo_atual - ultimo_tempo) < self.min_intervalo:
                    return False

            self.modificacoes_recentes[nome_arquivo] = tempo_atual
            self.count_modificacoes[nome_arquivo] = self.count_modificacoes.get(nome_arquivo, 0) + 1
            self.observador.ultima_modificacao[nome_arquivo] = tempo_atual

            ext = os.path.splitext(nome_arquivo)[1].lower()
            self._limpar_cache_metadados(caminho_completo, ext)

            self.notificar_evento(self.observador.loc.get_text("op_modified"), nome_arquivo, caminho_completo, caminho_completo)
            return True

        except Exception as e:
            print(f"Erro ao processar modificação massiva: {e}")
            return False

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
                    print(f"Erro ao processar arquivo renomeado: {e}")
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
                        print(f"Ignorando modificação de vídeo {nome_arquivo} - ainda em processo de adição")
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

            print(f"Erro ao processar modificação: {e}")
            return False
