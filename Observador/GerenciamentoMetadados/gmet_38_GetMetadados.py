import os
from datetime import datetime
from Observador.GerenciamentoMetadados import (
    extrair_metadados_codigo_fonte,
    extrair_metadados_imagem,
    extrair_metadados_audio,
    extrair_metadados_video,
    extrair_metadados_documento,
    extrair_metadados_planilha,
    extrair_metadados_apresentacao,
    extrair_metadados_banco_dados,
    extrair_metadados_executavel,
    extrair_metadados_temporario,
    extrair_metadados_compactados,
    extrair_metadados_backup,
    extrair_metadados_log,
    extrair_metadados_config,
    extrair_metadados_olefile,
    identificar_tipo_arquivo,
    get_atributos_arquivo,
    get_autor_arquivo,
    get_dimensoes_arquivo,
    get_protecao_arquivo
)
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_metadados(gc, item):
    try:
        caminho = item.get("dir_atual") or item.get("dir_anterior")
        if not caminho or not os.path.exists(caminho):
            tipo = identificar_tipo_arquivo(caminho, gc.loc, item.get("nome"))
            metadados = {"tipo": tipo}
            return metadados

        tipo_operacao = item.get("tipo_operacao", "")
        ops_invalida = {
            gc.loc.get_text("op_added"),
            gc.loc.get_text("op_deleted"),
            gc.loc.get_text("op_modified"),
            gc.loc.get_text("op_moved"),
            gc.loc.get_text("op_renamed"),
        }
        if tipo_operacao in ops_invalida:
            gc._invalidar_cache_diretorios_relacionados(caminho)

        if tipo_operacao == gc.loc.get_text("op_added") and os.path.isfile(caminho):
            with gc.lock_cache:
                if caminho in gc.cache_metadados:
                    gc.cache_metadados.pop(caminho, None)

        with gc.lock_cache:
            if caminho in gc.cache_metadados:
                if (tipo_operacao == gc.loc.get_text("op_added") and 
                    os.path.isdir(caminho) and 
                    gc.cache_metadados[caminho].get("tamanho_dir_bytes", 0) == 0):
                    gc.cache_metadados.pop(caminho, None)

                else:
                    for campo in [
                        "paginas", 
                        "linhas", 
                        "palavras", 
                        "paginas_estimadas", 
                        "linhas_codigo",
                        "total_linhas", 
                        "slides_estimadas", 
                        "arquivos", 
                        "unzipped_b", 
                        "unzipped_kb",
                        "unzipped_mb", 
                        "unzipped_gb", 
                        "unzipped_tb", 
                        "slides", 
                        "binary_file_b",
                        "binary_file_kb", 
                        "binary_file_mb", 
                        "binary_file_gb", 
                        "binary_file_tb",
                        "planilhas", 
                        "colunas", 
                        "registros", 
                        "tabelas"
                    ]:
                        if campo in gc.cache_metadados[caminho]:
                            item[campo] = gc.cache_metadados[caminho][campo]

                    return gc.cache_metadados[caminho]

        if os.path.exists(caminho):
            stats = os.stat(caminho)
            tamanho_bytes = stats.st_size if os.path.isfile(caminho) else gc._get_tamanho_bytes(item)
            metadados = {
                "size_b": int(tamanho_bytes),
                "size_kb": round(tamanho_bytes / 1024, 2),
                "size_mb": round(tamanho_bytes / 1024**2, 2),
                "size_gb": round(tamanho_bytes / 1024**3, 2),
                "size_tb": round(tamanho_bytes / 1024**4, 2),
                "data_acesso": datetime.fromtimestamp(stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
                "data_modificacao": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "data_criacao": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "atributos": get_atributos_arquivo(item, gc.loc),
                "autor": get_autor_arquivo(item, gc.loc),
                "protegido": get_protecao_arquivo(gc, item, gc.loc)
            }
            try:
                tipo = identificar_tipo_arquivo(caminho, gc.loc)
                metadados["tipo"] = tipo
                ext = os.path.splitext(caminho)[1].lower()
                if ext == '.dat':
                    from Observador.GerenciamentoMetadados.gmet_17_ExtrairMetadadosDadosEstruturados import extrair_metadados_dados_estruturados
                    metadados_dat = extrair_metadados_dados_estruturados(caminho, gc.loc)
                    metadados.update(metadados_dat)

                elif os.path.isfile(caminho):
                    if tipo == gc.loc.get_text("file_image"):
                        metadados.update(extrair_metadados_imagem(caminho))

                    elif tipo == gc.loc.get_text("file_audio"):
                        metadados.update(extrair_metadados_audio(caminho))

                    elif tipo == gc.loc.get_text("file_video"):
                        metadados.update(extrair_metadados_video(caminho))

                    elif tipo == gc.loc.get_text("file_document"):
                        metadados.update(extrair_metadados_documento(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_spreadsheet"):
                        metadados.update(extrair_metadados_planilha(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_presentation"):
                        metadados.update(extrair_metadados_apresentacao(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_database"):
                        metadados.update(extrair_metadados_banco_dados(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_executable"):
                        metadados.update(extrair_metadados_executavel(caminho, gc.loc))
                        try:
                            tamanho_bytes = os.path.getsize(caminho)
                            metadados["binary_file_b"] = int(tamanho_bytes)
                            metadados["binary_file_kb"] = round(tamanho_bytes / 1024, 2)
                            metadados["binary_file_mb"] = round(tamanho_bytes / 1024**2, 2)
                            metadados["binary_file_gb"] = round(tamanho_bytes / 1024**3, 2)
                            metadados["binary_file_tb"] = round(tamanho_bytes / 1024**4, 2)

                        except Exception as e:
                            logger.error(f"Erro ao calcular tamanho do executável: {e}", exc_info=True)

                    elif tipo == gc.loc.get_text("file_source_code"):
                        metadados.update(extrair_metadados_codigo_fonte(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_temp"):
                        metadados.update(extrair_metadados_temporario(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_compressed"):
                        metadados_compactados = extrair_metadados_compactados(caminho, gc.loc)
                        metadados.update(metadados_compactados)
                        t_unzipped = metadados_compactados.get("tamanho_descompactado_bytes")
                        if t_unzipped is not None:
                            metadados["unzipped_b"] = int(t_unzipped)
                            metadados["unzipped_kb"] = round(t_unzipped / 1024, 2)
                            metadados["unzipped_mb"] = round(t_unzipped / 1024**2, 2)
                            metadados["unzipped_gb"] = round(t_unzipped / 1024**3, 2)
                            metadados["unzipped_tb"] = round(t_unzipped / 1024**4, 2)

                    elif tipo == gc.loc.get_text("file_backup"):
                        metadados.update(extrair_metadados_backup(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_log"):
                        metadados.update(extrair_metadados_log(caminho, gc.loc))

                    elif tipo == gc.loc.get_text("file_config"):
                        metadados.update(extrair_metadados_config(caminho, gc.loc))

                    ext = os.path.splitext(caminho)[1].lower()
                    if ext in ['.doc', '.xls', '.ppt', '.msg']:
                        metadados.update(extrair_metadados_olefile(caminho, gc.loc))

                metadados["atributos"] = get_atributos_arquivo(item, gc.loc)
                metadados["autor"] = get_autor_arquivo(item, gc.loc)
                metadados["protegido"] = get_protecao_arquivo(gc, item, gc.loc)
                get_dimensoes_arquivo(gc, item, gc.loc)
                with gc.lock_cache:
                    if caminho in gc.cache_metadados:
                        for campo in [
                            "paginas", 
                            "linhas", 
                            "palavras", 
                            "paginas_estimadas", 
                            "linhas_codigo",
                            "total_linhas", 
                            "slides_estimadas", 
                            "arquivos", 
                            "unzipped_b", 
                            "unzipped_kb",
                            "unzipped_mb", 
                            "unzipped_gb", 
                            "unzipped_tb", 
                            "slides", 
                            "binary_file_b",
                            "binary_file_kb", 
                            "binary_file_mb", 
                            "binary_file_gb", 
                            "binary_file_tb",
                            "planilhas", 
                            "colunas", 
                            "registros", 
                            "tabelas"
                        ]:
                            if campo in gc.cache_metadados[caminho]:
                                metadados[campo] = gc.cache_metadados[caminho][campo]
                                item[campo] = gc.cache_metadados[caminho][campo]

            except Exception as e:
                logger.error(f"Erro ao extrair metadados específicos: {e}", exc_info=True)

            with gc.lock_cache:
                gc.cache_metadados[caminho] = metadados

            for campo, valor in metadados.items():
                item[campo] = valor

            return metadados

        return {}

    except Exception as e:
        logger.error(f"Erro ao obter metadados: {e}", exc_info=True)
        return {}
