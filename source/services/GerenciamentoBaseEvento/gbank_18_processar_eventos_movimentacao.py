import sqlite3
from datetime import datetime
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def processar_eventos_movimentacao(self, eventos_movidos, callback=None):
    if not eventos_movidos:
        return

    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA synchronous = OFF")
            cursor.execute("BEGIN TRANSACTION")
            valores_lote = []
            colunas = [
                'tipo_operacao', 
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
                'timestamp'
            ]

            for evento in eventos_movidos:
                if not evento or evento.get("tipo_operacao") != self.observador.loc.get_text("op_moved"):
                    continue

                valores = []
                for coluna in colunas:
                    if coluna == "tipo_operacao":
                        valores.append(self.observador.loc.get_text("op_moved"))

                    elif coluna == "timestamp" and "timestamp" not in evento:
                        valores.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

                    else:
                        valores.append(evento.get(coluna, ""))

                valores_lote.append(tuple(valores))

            if valores_lote:
                placeholders = ", ".join(["?" for _ in colunas])
                colunas_str = ", ".join(colunas)
                cursor.executemany(f"INSERT INTO movido ({colunas_str}) VALUES ({placeholders})", valores_lote)
                cursor.executemany(f"INSERT INTO monitoramento ({colunas_str}) VALUES ({placeholders})", valores_lote)

            cursor.execute("COMMIT")
            cursor.execute("PRAGMA synchronous = NORMAL")
            if callback and callable(callback):
                callback()

    except Exception as e:
        logger.error(f"Erro ao processar lote de eventos movidos: {e}", exc_info=True)
        try:
            if 'conn' in locals() and conn:
                cursor.execute("ROLLBACK")

        except Exception as e:
            logger.error(f"Erro ao reverter transação: {e}", exc_info=True)
