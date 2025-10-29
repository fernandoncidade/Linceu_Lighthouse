import os
import sqlite3
from datetime import datetime
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_item(self, nome, caminho, tipo):
    try:
        item = {
            "nome": nome,
            "dir_atual": caminho
        }

        self.current_item = item

        metadados = {}
        if caminho and os.path.exists(caminho):
            try:
                metadados = self.gerenciador_colunas.get_metadados(item) or {}

            except Exception as e:
                logger.debug(f"Falha ao obter metadados para {caminho}: {e}", exc_info=True)
                metadados = {}

            tipo = self.get_file_type(caminho)

        else:
            tipo = ""
            metadados = {}

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        evento = {
            "tipo_operacao": self.observador.loc.get_text("op_scanned"),
            "nome": nome,
            "dir_anterior": "",
            "dir_atual": caminho,
            "data_criacao": metadados.get("data_criacao", ""),
            "data_modificacao": metadados.get("data_modificacao", ""),
            "data_acesso": metadados.get("data_acesso", ""),
            "tipo": tipo,
            "size_b": metadados.get("size_b", ""),
            "size_kb": metadados.get("size_kb", ""),
            "size_mb": metadados.get("size_mb", ""),
            "size_gb": metadados.get("size_gb", ""),
            "size_tb": metadados.get("size_tb", ""),
            "atributos": metadados.get("atributos", ""),
            "autor": metadados.get("autor", ""),
            "dimensoes": metadados.get("dimensoes", ""),
            "duracao": metadados.get("duracao", ""),
            "taxa_bits": metadados.get("taxa_bits", ""),
            "protegido": metadados.get("protegido", ""),
            "paginas": metadados.get("paginas", ""),
            "linhas": metadados.get("linhas", ""),
            "palavras": metadados.get("palavras", ""),
            "paginas_estimadas": metadados.get("paginas_estimadas", ""),
            "linhas_codigo": metadados.get("linhas_codigo", ""),
            "total_linhas": metadados.get("total_linhas", ""),
            "slides_estimados": metadados.get("slides_estimados", ""),
            "arquivos": metadados.get("arquivos", ""),
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
            "tabelas": metadados.get("tabelas", ""),
            "timestamp": timestamp
        }

        try:
            self.observador.evento_base.registrar_evento_no_banco(evento)

        except Exception as e:
            logger.error(f"Falha ao enfileirar evento para {caminho}: {e}", exc_info=True)
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    colunas = ['tipo_operacao',
                               'nome',
                               'dir_anterior',
                               'dir_atual',
                               'data_criacao',
                               'data_modificacao',
                               'data_acesso',
                               'tipo',
                               'size_b',
                               'size_kb',
                               'size_mb',
                               'size_gb',
                               'size_tb',
                               'atributos',
                               'autor',
                               'dimensoes',
                               'duracao',
                               'taxa_bits',
                               'protegido',
                               'paginas',
                               'linhas',
                               'palavras',
                               'paginas_estimadas',
                               'linhas_codigo',
                               'total_linhas',
                               'slides_estimados',
                               'arquivos',
                               'unzipped_b',
                               'unzipped_kb',
                               'unzipped_mb',
                               'unzipped_gb',
                               'unzipped_tb',
                               'slides',
                               'binary_file_b',
                               'binary_file_kb',
                               'binary_file_mb',
                               'binary_file_gb',
                               'binary_file_tb',
                               'planilhas',
                               'colunas',
                               'registros',
                               'tabelas',
                               'timestamp']
                    valores = [evento.get(c, "") for c in colunas]
                    placeholders = ", ".join(["?" for _ in colunas])
                    colunas_str = ", ".join(colunas)
                    query_monitoramento = f"INSERT INTO monitoramento ({colunas_str}) VALUES ({placeholders})"
                    cursor.execute(query_monitoramento, valores)
                    conn.commit()

            except Exception as e2:
                logger.error(f"Erro no fallback de gravação para {caminho}: {e2}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao processar item {nome}: {e}", exc_info=True)
