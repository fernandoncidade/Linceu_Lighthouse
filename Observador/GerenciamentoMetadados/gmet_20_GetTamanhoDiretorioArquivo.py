import os
import time
from .gmet_21_GetFormataTamanho import get_formata_tamanho
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_tamanho_diretorio_arquivo(self, item_data, loc):
    try:
        caminho = item_data.get("dir_atual") or item_data.get("dir_anterior", "")
        if not caminho or not os.path.exists(caminho):
            return ""

        is_file = os.path.isfile(caminho)
        is_dir = os.path.isdir(caminho)

        if is_file:
            with self.lock_cache:
                if caminho in self.cache_metadados and "tamanho" in self.cache_metadados[caminho]:
                    return self.cache_metadados[caminho]["tamanho"]

            try:
                tamanho = os.path.getsize(caminho)
                resultado = get_formata_tamanho(tamanho)

                with self.lock_cache:
                    if caminho not in self.cache_metadados:
                        self.cache_metadados[caminho] = {}

                    self.cache_metadados[caminho]["tamanho"] = resultado

                return resultado

            except Exception as e:
                logger.error(f"Erro ao obter tamanho do arquivo {caminho}: {e}", exc_info=True)
                return ""

        tipo_operacao = item_data.get("tipo_operacao", "")
        timestamp_item = item_data.get("timestamp", "")

        if tipo_operacao == loc.get_text("op_added") and timestamp_item:
            try:
                from datetime import datetime
                ts = datetime.fromisoformat(timestamp_item.replace('Z', '+00:00'))
                tempo_desde_adicao = (datetime.now() - ts.replace(tzinfo=None)).total_seconds()

                if tempo_desde_adicao < 5:
                    time.sleep(2)

            except Exception as e:
                logger.error(f"Erro ao processar timestamp do item {item_data}: {e}", exc_info=True)

        ttl = 3 if tipo_operacao == loc.get_text("op_added") else getattr(self, "dir_size_cache_ttl", 10)

        try:
            dir_mtime = os.path.getmtime(caminho)

        except Exception:
            dir_mtime = None

        with self.lock_cache:
            cache = self.cache_metadados.get(caminho, {}).copy()

        if cache:
            cached_val = cache.get("tamanho_dir")
            cached_bytes = cache.get("tamanho_dir_bytes")
            cached_mtime = cache.get("tamanho_dir_mtime")
            cached_at = cache.get("tamanho_dir_cached_at", 0)

            if tipo_operacao == loc.get_text("op_added") and cached_bytes == 0:
                pass

            elif (
                cached_val
                and cached_mtime is not None
                and dir_mtime is not None
                and cached_mtime >= dir_mtime
                and (time.time() - cached_at) <= ttl
            ):
                return cached_val

        total_bytes = 0
        arquivos_ignorados = 0

        try:
            def calcular_tamanho_dir(dir_path):
                nonlocal total_bytes, arquivos_ignorados
                try:
                    with os.scandir(dir_path) as entries:
                        for entry in entries:
                            try:
                                if entry.is_file(follow_symlinks=False):
                                    total_bytes += entry.stat(follow_symlinks=False).st_size

                                elif entry.is_dir(follow_symlinks=False):
                                    calcular_tamanho_dir(entry.path)

                            except (OSError, IOError, PermissionError) as e:
                                logger.error(f"Erro ao processar {entry.path}: {e}", exc_info=True)
                                arquivos_ignorados += 1

                except Exception as e:
                    logger.error(f"Erro ao escanear diretório {dir_path}: {e}", exc_info=True)
                    arquivos_ignorados += 1

            calcular_tamanho_dir(caminho)

            resultado = get_formata_tamanho(total_bytes)
            if arquivos_ignorados > 0:
                resultado = f"{resultado} ({arquivos_ignorados} {loc.get_text('ignored')})"

            agora = time.time()
            with self.lock_cache:
                if caminho not in self.cache_metadados:
                    self.cache_metadados[caminho] = {}

                self.cache_metadados[caminho]["tamanho"] = resultado
                self.cache_metadados[caminho]["tamanho_dir"] = resultado
                self.cache_metadados[caminho]["tamanho_dir_bytes"] = total_bytes
                self.cache_metadados[caminho]["tamanho_dir_mtime"] = dir_mtime if dir_mtime is not None else agora
                self.cache_metadados[caminho]["tamanho_dir_cached_at"] = agora

            return resultado

        except Exception as e:
            logger.error(f"Erro ao calcular tamanho do diretório {caminho}: {e}", exc_info=True)
            return ""

    except Exception as e:
        logger.error(f"Erro geral no cálculo de tamanho: {e}", exc_info=True)
        return ""
