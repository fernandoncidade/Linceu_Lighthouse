import sqlite3
from datetime import datetime
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def registrar_evento_especifico(self, tabela, evento):
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {tabela} (
                    nome,
                    dir_anterior,
                    dir_atual,
                    data_criacao,
                    data_modificacao,
                    data_acesso,
                    tipo,
                    size_b,
                    size_kb,
                    size_mb,
                    size_gb,
                    size_tb,
                    atributos,
                    autor,
                    dimensoes,
                    duracao,
                    taxa_bits,
                    protegido,
                    paginas,
                    linhas,
                    palavras,
                    paginas_estimadas,
                    linhas_codigo,
                    total_linhas,
                    slides_estimados,
                    arquivos,
                    unzipped_b,
                    unzipped_kb,
                    unzipped_mb,
                    unzipped_gb,
                    unzipped_tb,
                    slides,
                    binary_file_b,
                    binary_file_kb,
                    binary_file_mb,
                    binary_file_gb,
                    binary_file_tb,
                    planilhas,
                    colunas,
                    registros,
                    tabelas,
                    timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                evento["nome"],
                evento.get("dir_anterior", ""),
                evento.get("dir_atual", ""),
                evento.get("data_criacao", ""),
                evento.get("data_modificacao", ""),
                evento.get("data_acesso", ""),
                evento["tipo"],
                evento.get("size_b", ""),
                evento.get("size_kb", ""),
                evento.get("size_mb", ""),
                evento.get("size_gb", ""),
                evento.get("size_tb", ""),
                evento.get("atributos", ""),
                evento.get("autor", ""),
                evento.get("dimensoes", ""),
                evento.get("duracao", ""),
                evento.get("taxa_bits", ""),
                evento.get("protegido", ""),
                evento.get("paginas", ""),
                evento.get("linhas", ""),
                evento.get("palavras", ""),
                evento.get("paginas_estimadas", ""),
                evento.get("linhas_codigo", ""),
                evento.get("total_linhas", ""),
                evento.get("slides_estimados", ""),
                evento.get("arquivos", ""),
                evento.get("unzipped_b", ""),
                evento.get("unzipped_kb", ""),
                evento.get("unzipped_mb", ""),
                evento.get("unzipped_gb", ""),
                evento.get("unzipped_tb", ""),
                evento.get("slides", ""),
                evento.get("binary_file_b", ""),
                evento.get("binary_file_kb", ""),
                evento.get("binary_file_mb", ""),
                evento.get("binary_file_gb", ""),
                evento.get("binary_file_tb", ""),
                evento.get("planilhas", ""),
                evento.get("colunas", ""),
                evento.get("registros", ""),
                evento.get("tabelas", ""),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            ))

            conn.commit()

    except Exception as e:
        logger.error(f"Erro ao registrar evento na tabela {tabela}: {e}", exc_info=True)
