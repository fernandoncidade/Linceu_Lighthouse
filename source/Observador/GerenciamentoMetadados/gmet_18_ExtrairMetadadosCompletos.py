import os
from datetime import datetime
from .gmet_02_ExtrairMetadadosCodigoFonte import extrair_metadados_codigo_fonte
from .gmet_03_ExtrairMetadadosImagem import extrair_metadados_imagem
from .gmet_04_ExtrairMetadadosAudio import extrair_metadados_audio
from .gmet_05_ExtrairMetadadosVideo import extrair_metadados_video
from .gmet_06_ExtrairMetadadosDocumento import extrair_metadados_documento
from .gmet_07_ExtrairMetadadosPlanilha import extrair_metadados_planilha
from .gmet_08_ExtrairMetadadosApresentacao import extrair_metadados_apresentacao
from .gmet_09_ExtrairMetadadosBancoDados import extrair_metadados_banco_dados
from .gmet_10_ExtrairMetadadosExecutavel import extrair_metadados_executavel
from .gmet_11_ExtrairMetadadosTemporario import extrair_metadados_temporario
from .gmet_12_ExtrairMetadadosCompactados import extrair_metadados_compactados
from .gmet_13_ExtrairMetadadosBackup import extrair_metadados_backup
from .gmet_14_ExtrairMetadadosLog import extrair_metadados_log
from .gmet_15_ExtrairMetadadosConfig import extrair_metadados_config
from .gmet_17_ExtrairMetadadosDadosEstruturados import extrair_metadados_dados_estruturados
from .gmet_19_GetTipoArquivo import identificar_tipo_arquivo
from .gmet_20_GetTamanhoDiretorioArquivo import get_tamanho_diretorio_arquivo
from .gmet_21_GetFormataTamanho import formata_tamanho
from .gmet_22_GetAtributosArquivo import get_atributos_arquivo
from .gmet_23_GetAutorArquivo import get_autor_arquivo
from .gmet_27_GetProtecaoArquivo import get_protecao_arquivo
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def extrair_metadados_completos(item, loc=None, contexto=None):
    try:
        caminho = item.get("dir_atual") or item.get("dir_anterior")
        if not caminho or not os.path.exists(caminho):
            return {}

        stats = os.stat(caminho)

        metadados = {
            "tamanho": get_tamanho_diretorio_arquivo(contexto, item, loc) if contexto and loc else str(stats.st_size),
            "data_acesso": datetime.fromtimestamp(stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
            "data_modificacao": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "data_criacao": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "atributos": get_atributos_arquivo(item, loc) if loc else "",
            "autor": get_autor_arquivo(item, loc) if loc else "",
            "protegido": get_protecao_arquivo(contexto, item, loc) if contexto and loc else ""
        }

        if loc is None:
            return metadados

        tipo_arquivo = identificar_tipo_arquivo(caminho, loc)

        if not tipo_arquivo:
            return metadados

        ext = os.path.splitext(caminho)[1].lower()
        if ext == '.dat':
            metadados.update(extrair_metadados_dados_estruturados(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_video"):
            metadados.update(extrair_metadados_video(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_image"):
            metadados.update(extrair_metadados_imagem(caminho))

        elif tipo_arquivo == loc.get_text("file_audio"):
            metadados.update(extrair_metadados_audio(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_source_code"):
            metadados.update(extrair_metadados_codigo_fonte(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_document"):
            metadados.update(extrair_metadados_documento(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_spreadsheet"):
            metadados.update(extrair_metadados_planilha(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_presentation"):
            metadados.update(extrair_metadados_apresentacao(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_database"):
            metadados.update(extrair_metadados_banco_dados(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_executable"):
            metadados.update(extrair_metadados_executavel(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_temp"):
            metadados.update(extrair_metadados_temporario(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_compressed"):
            metadados.update(extrair_metadados_compactados(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_backup"):
            metadados.update(extrair_metadados_backup(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_log"):
            metadados.update(extrair_metadados_log(caminho, loc))

        elif tipo_arquivo == loc.get_text("file_config"):
            metadados.update(extrair_metadados_config(caminho, loc))

        return metadados

    except Exception as e:
        logger.error(f"Erro ao obter metadados completos: {e}", exc_info=True)
        return {}

def get_metadados(self, item=None):
    try:
        import traceback
        call_stack = traceback.format_stack()
        caller_info = call_stack[-2].strip() if len(call_stack) >= 2 else "Desconhecido"

        if item is None:
            item = getattr(self, "current_item", None)
            if item is None:
                return {}

        caminho = item.get("dir_atual") or item.get("dir_anterior")
        if not caminho or not os.path.exists(caminho):
            return {}

        tipo_operacao = item.get("tipo_operacao", "")
        ext = os.path.splitext(caminho)[1].lower()

        if ext == '.txt' and tipo_operacao == self.loc.get_text("op_modified"):
            try:
                linhas = 0
                palavras = 0
                caracteres = 0

                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                    for linha in f:
                        linhas += 1
                        palavras += len(linha.split())
                        caracteres += len(linha)

                tamanho = os.path.getsize(caminho)

                return {
                    "linhas": str(linhas),
                    "palavras": str(palavras),
                    "caracteres": str(caracteres),
                    "tamanho": formata_tamanho(tamanho)
                }

            except Exception as e:
                logger.error(f"Erro ao extrair metadados do TXT modificado {caminho}: {e}", exc_info=True)
                return {}

        return extrair_metadados_completos(item, self.loc, self)

    except Exception as e:
        logger.error(f"Erro ao obter metadados completos: {e}", exc_info=True)
