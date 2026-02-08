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
        metadados = self.gerenciador_colunas.get_metadados(item)
        tipo = self.get_file_type(caminho)
        with self.lock_db:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                        INSERT INTO snapshot (
                                nome,
                                diretorio,
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
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        nome,
                        caminho,
                        tipo,
                        metadados.get("data_criacao", ""),
                        metadados.get("data_modificacao", ""),
                        metadados.get("data_acesso", ""),
                        metadados.get("size_b", ""),
                        metadados.get("size_kb", ""),
                        metadados.get("size_mb", ""),
                        metadados.get("size_gb", ""),
                        metadados.get("size_tb", ""),
                        metadados.get("atributos", ""),
                        metadados.get("autor", ""),
                        metadados.get("dimensoes", ""),
                        metadados.get("duracao", ""),
                        metadados.get("taxa_bits", ""),
                        metadados.get("protegido", ""),
                        metadados.get("paginas", ""),
                        metadados.get("linhas", ""),
                        metadados.get("palavras", ""),
                        metadados.get("paginas_estimadas", ""),
                        metadados.get("linhas_codigo", ""),
                        metadados.get("total_linhas", ""),
                        metadados.get("slides_estimados", ""),
                        metadados.get("arquivos", ""),
                        metadados.get("unzipped_b", ""),
                        metadados.get("unzipped_kb", ""),
                        metadados.get("unzipped_mb", ""),
                        metadados.get("unzipped_gb", ""),
                        metadados.get("unzipped_tb", ""),
                        metadados.get("slides", ""),
                        metadados.get("binary_file_b", ""),
                        metadados.get("binary_file_kb", ""),
                        metadados.get("binary_file_mb", ""),
                        metadados.get("binary_file_gb", ""),
                        metadados.get("binary_file_tb", ""),
                        metadados.get("planilhas", ""),
                        metadados.get("colunas", ""),
                        metadados.get("registros", ""),
                        metadados.get("tabelas", ""),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                ))

                conn.commit()

    except Exception as e:
        logger.error(f"Erro ao processar item {nome}: {e}", exc_info=True)
