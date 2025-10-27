import sqlite3
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_tipo_anterior(self, nome_base):
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tipo FROM monitoramento
                WHERE nome = ?
                ORDER BY id DESC
                LIMIT 1
            """, (nome_base,))

            row = cursor.fetchone()

            if row:
                return row[0]

        return self.get_tipo_from_snapshot(nome_base)

    except Exception as e:
        logger.error(f"Erro ao obter tipo anterior: {e}", exc_info=True)
