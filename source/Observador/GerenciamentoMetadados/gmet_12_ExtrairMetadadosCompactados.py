import os
from .gmet_21_GetFormataTamanho import get_formata_tamanho
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def extrair_metadados_compactados(caminho, loc):
    metadados = {}
    ext = os.path.splitext(caminho)[1].lower()

    try:
        if ext == '.zip':
            try:
                import zipfile
                try:
                    with zipfile.ZipFile(caminho, 'r') as zip_ref:
                        arquivos = zip_ref.namelist()
                        qtd_arquivos = len(arquivos)

                        tamanho_total = sum(info.file_size for info in zip_ref.infolist())
                        tamanho_compactado = os.path.getsize(caminho)

                        if tamanho_total > 0:
                            taxa_compressao = (1 - tamanho_compactado / tamanho_total) * 100
                            
                        else:
                            taxa_compressao = 0

                        metadados['arquivos'] = qtd_arquivos
                        metadados['tamanho_descompactado'] = get_formata_tamanho(tamanho_total)
                        metadados['tamanho_descompactado_bytes'] = tamanho_total
                        metadados['taxa_compressao'] = f"{taxa_compressao:.1f}%"
                        metadados['descompactados'] = metadados['tamanho_descompactado']

                        if arquivos:
                            arquivos_top = sorted([a for a in arquivos if '/' not in a])[:5]
                            if arquivos_top:
                                metadados['conteudo'] = ", ".join(arquivos_top)
                                if len(arquivos) > 5:
                                    metadados['conteudo'] += f" {loc.get_text('and_others')} {len(arquivos)-5}"

                except UnicodeDecodeError as ude:
                    logger.warning(f"Nome de entrada ZIP com encoding inválido: {ude}. Tentando fallback CP437.")
                    try:
                        with zipfile.ZipFile(caminho, 'r', encoding='cp437') as zip_ref:
                            arquivos = zip_ref.namelist()
                            qtd_arquivos = len(arquivos)

                            tamanho_total = sum(info.file_size for info in zip_ref.infolist())
                            tamanho_compactado = os.path.getsize(caminho)

                            if tamanho_total > 0:
                                taxa_compressao = (1 - tamanho_compactado / tamanho_total) * 100

                            else:
                                taxa_compressao = 0

                            metadados['arquivos'] = qtd_arquivos
                            metadados['tamanho_descompactado'] = get_formata_tamanho(tamanho_total)
                            metadados['tamanho_descompactado_bytes'] = tamanho_total
                            metadados['taxa_compressao'] = f"{taxa_compressao:.1f}%"
                            metadados['descompactados'] = metadados['tamanho_descompactado']

                            if arquivos:
                                arquivos_top = sorted([a for a in arquivos if '/' not in a])[:5]
                                if arquivos_top:
                                    metadados['conteudo'] = ", ".join(arquivos_top)
                                    if len(arquivos) > 5:
                                        metadados['conteudo'] += f" {loc.get_text('and_others')} {len(arquivos)-5}"

                    except TypeError:
                        logger.warning("zipfile.ZipFile não aceita parametro 'encoding' nesta versão do Python. Retornando metadados básicos.")
                        metadados['arquivos'] = 0
                        metadados['tamanho_compactado'] = os.path.getsize(caminho)

                except Exception as e:
                    logger.error(f"Erro ao extrair metadados do ZIP {caminho}: {e}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro ao extrair metadados do ZIP {caminho}: {e}", exc_info=True)

        elif ext == '.rar':
            try:
                import rarfile
                with rarfile.RarFile(caminho) as rar:
                    arquivos = rar.namelist()
                    qtd_arquivos = len(arquivos)

                    tamanho_total = sum(f.file_size for f in rar.infolist())
                    tamanho_compactado = os.path.getsize(caminho)

                    if tamanho_total > 0:
                        taxa_compressao = (1 - tamanho_compactado / tamanho_total) * 100

                    else:
                        taxa_compressao = 0

                    metadados['arquivos'] = qtd_arquivos
                    metadados['tamanho_descompactado'] = get_formata_tamanho(tamanho_total)
                    metadados['tamanho_descompactado_bytes'] = tamanho_total
                    metadados['taxa_compressao'] = f"{taxa_compressao:.1f}%"
                    metadados['descompactados'] = metadados['tamanho_descompactado']

                    if arquivos:
                        arquivos_top = sorted([a for a in arquivos if '/' not in a])[:5]
                        if arquivos_top:
                            metadados['conteudo'] = ", ".join(arquivos_top)
                            if len(arquivos) > 5:
                                metadados['conteudo'] += f" {loc.get_text('and_others')} {len(arquivos)-5}"

            except Exception as e:
                logger.error(f"Erro ao extrair metadados do RAR {caminho}: {e}", exc_info=True)

        elif ext == '.7z':
            try:
                import py7zr
                with py7zr.SevenZipFile(caminho, mode='r') as z:
                    arquivos = z.getnames()
                    qtd_arquivos = len(arquivos)

                    arquivos_info = z.list()
                    tamanho_total = sum(info.uncompressed for info in arquivos_info)
                    tamanho_compactado = os.path.getsize(caminho)

                    if tamanho_total > 0:
                        taxa_compressao = (1 - tamanho_compactado / tamanho_total) * 100

                    else:
                        taxa_compressao = 0

                    metadados['arquivos'] = qtd_arquivos
                    metadados['tamanho_descompactado'] = get_formata_tamanho(tamanho_total)
                    metadados['tamanho_descompactado_bytes'] = tamanho_total
                    metadados['taxa_compressao'] = f"{taxa_compressao:.1f}%"
                    metadados['descompactados'] = metadados['tamanho_descompactado']

                    if arquivos:
                        arquivos_top = sorted([a for a in arquivos if '/' not in a])[:5]
                        if arquivos_top:
                            metadados['conteudo'] = ", ".join(arquivos_top)
                            if len(arquivos) > 5:
                                metadados['conteudo'] += f" {loc.get_text('and_others')} {len(arquivos)-5}"

            except Exception as e:
                logger.error(f"Erro ao extrair metadados do 7Z {caminho}: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro geral ao extrair metadados do arquivo compactado {caminho}: {e}", exc_info=True)

    return metadados
