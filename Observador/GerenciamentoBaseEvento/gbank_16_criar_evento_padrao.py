import os
from datetime import datetime
from Observador.GerenciamentoMetadados.gmet_19_GetTipoArquivo import identificar_tipo_arquivo
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_evento_padrao(self, tipo_operacao, nome_base, dir_anterior, dir_atual):
    try:
        caminho = dir_atual if os.path.exists(dir_atual) else dir_anterior
        metadados = {}
        tipo_arquivo = ""
        size_b = 0
        arquivos = 0

        if os.path.exists(caminho):
            e_pasta = self.is_directory(caminho)
            if e_pasta:
                tipo_arquivo = self.observador.loc.get_text("folder")
                total_bytes = 0
                total_arquivos = 0
                for root, dirs, files in os.walk(caminho):
                    total_arquivos += len(files)
                    for f in files:
                        try:
                            total_bytes += os.path.getsize(os.path.join(root, f))

                        except Exception:
                            pass

                size_b = total_bytes
                arquivos = total_arquivos

            else:
                extensao = os.path.splitext(nome_base)[1][1:].lower()
                tipo_arquivo = extensao if extensao else self.observador.loc.get_text("unknown")
                try:
                    size_b = os.path.getsize(caminho)

                except Exception:
                    size_b = 0

            stats = os.stat(caminho)
            data_criacao = datetime.fromtimestamp(stats.st_ctime)
            data_modificacao = datetime.fromtimestamp(stats.st_mtime)
            data_acesso = datetime.fromtimestamp(stats.st_atime)

        else:
            tipo_arquivo = identificar_tipo_arquivo(nome_base, self.observador.loc)
            if not tipo_arquivo:
                tipo_arquivo = self.get_tipo_from_snapshot(nome_base)
                if not tipo_arquivo:
                    extensao = os.path.splitext(nome_base)[1][1:].lower()
                    tipo_arquivo = extensao if extensao else self.observador.loc.get_text("unknown")

            data_criacao = data_modificacao = data_acesso = datetime.now()
            if dir_anterior and self.is_directory(dir_anterior):
                tipo_arquivo = self.observador.loc.get_text("folder")
                total_bytes = 0
                total_arquivos = 0
                for root, dirs, files in os.walk(dir_anterior):
                    total_arquivos += len(files)
                    for f in files:
                        try:
                            total_bytes += os.path.getsize(os.path.join(root, f))

                        except Exception:
                            pass

                size_b = total_bytes
                arquivos = total_arquivos

        ext = os.path.splitext(nome_base)[1].lower()
        TIPOS_TEMPORARIOS = {'.tmp', '.temp', '.~', '.swp', '.swo', '.$$', '.old', '.part', 
                            '.cache', '.crdownload', '.download', '.partial', '.lock', '.thumb',
                            '.TMP', '.TEMP'}
        eh_temporario = ext in TIPOS_TEMPORARIOS or \
            nome_base.lower().startswith(("~", "._", ".#", "~$")) or \
            nome_base.lower().endswith(("~", ".lock")) or \
            "temp-index" in nome_base.lower() or \
            "~index" in nome_base.lower() or \
            "thumb" in nome_base.lower()

        item_data = {
            "nome": nome_base,
            "dir_atual": dir_atual,
            "dir_anterior": dir_anterior,
            "tipo": tipo_arquivo
        }
        self.current_item = item_data
        metadados = self.observador.gerenciador_colunas.get_metadados(item_data)

        if tipo_arquivo == self.observador.loc.get_text("folder"):
            metadados["size_b"] = size_b
            metadados["size_kb"] = round(size_b / 1024, 2)
            metadados["size_mb"] = round(size_b / 1024**2, 2)
            metadados["size_gb"] = round(size_b / 1024**3, 2)
            metadados["size_tb"] = round(size_b / 1024**4, 2)
            metadados["arquivos"] = arquivos
            metadados["atributos"] = self.observador.loc.get_text("folder")
            metadados["autor"] = os.environ.get("USERNAME", "")
            metadados["protegido"] = self.observador.loc.get_text("No")

        elif eh_temporario:
            metadados["atributos"] = self.observador.loc.get_text("file")

        return {
            "tipo_operacao": tipo_operacao,
            "nome": nome_base,
            "dir_anterior": dir_anterior,
            "dir_atual": dir_atual,
            "data_criacao": data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "data_modificacao": data_modificacao.strftime("%Y-%m-%d %H:%M:%S"),
            "data_acesso": data_acesso.strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo_arquivo,
            "size_b": metadados.get("size_b", size_b),
            "size_kb": metadados.get("size_kb", round(size_b / 1024, 2)),
            "size_mb": metadados.get("size_mb", round(size_b / 1024**2, 2)),
            "size_gb": metadados.get("size_gb", round(size_b / 1024**3, 2)),
            "size_tb": metadados.get("size_tb", round(size_b / 1024**4, 2)),
            "atributos": metadados.get("atributos", self.observador.loc.get_text("file") if eh_temporario else ""),
            "autor": metadados.get("autor", os.environ.get("USERNAME", "")),
            "dimensoes": metadados.get("dimensoes", ""),
            "duracao": metadados.get("duracao", ""),
            "taxa_bits": metadados.get("taxa_bits", ""),
            "protegido": metadados.get("protegido", self.observador.loc.get_text("No")),
            "paginas": metadados.get("paginas", ""),
            "linhas": metadados.get("linhas", ""),
            "palavras": metadados.get("palavras", ""),
            "paginas_estimadas": metadados.get("paginas_estimadas", ""),
            "linhas_codigo": metadados.get("linhas_codigo", ""),
            "total_linhas": metadados.get("total_linhas", ""),
            "slides_estimados": metadados.get("slides_estimados", ""),
            "arquivos": metadados.get("arquivos", arquivos),
            "unzipped_b": metadados.get("unzipped_b", ""),
            "unzipped_kb": metadados.get("unzipped_kb", ""),
            "unzipped_mb": metadados.get("unzipped_mb", ""),
            "unzipped_gb": metadados.get("unzipped_gb", ""),
            "unzipped_tb": metadados.get("unzipped_tb", ""),
            "slides": metadados.get("slides", ""),
            "binary_file_b": metadados.get("binary_file_b", ""),
            "binary_file_kb": metadados.get("binary_file_kb", ""),
            "binary_file_mb": metadados.get("binary_file_mb", ""),
            "binary_file_gb": metadados.get("binary_file_gb", ""),
            "binary_file_tb": metadados.get("binary_file_tb", ""),
            "planilhas": metadados.get("planilhas", ""),
            "colunas": metadados.get("colunas", ""),
            "registros": metadados.get("registros", ""),
            "tabelas": metadados.get("tabelas", "")
        }

    except Exception as e:
        logger.error(f"Erro ao criar evento padrão: {e}", exc_info=True)
