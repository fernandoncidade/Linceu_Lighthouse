import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def processar(self, nome_arquivo, caminho_completo, tempo_atual):
    try:
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
                        return False

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

    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}", exc_info=True)
