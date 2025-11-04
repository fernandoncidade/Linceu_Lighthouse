import sqlite3
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_tipo_from_snapshot(self, nome):
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tipo FROM snapshot 
                WHERE nome = ?
                LIMIT 1
            """, (nome,))

            row = cursor.fetchone()
            return row[0] if row else None

    except Exception as e:
        logger.error(f"Erro ao obter tipo de snapshot: {e}", exc_info=True)
