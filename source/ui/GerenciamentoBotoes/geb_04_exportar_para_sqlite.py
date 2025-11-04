import sqlite3
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _exportar_para_sqlite(self, dados, nome_arquivo):
    try:
        conn = sqlite3.connect(nome_arquivo)
        cursor = conn.cursor()
        if dados:
            cursor.execute("DROP TABLE IF EXISTS eventos")
            colunas = list(dados[0].keys())
            create_query = f"CREATE TABLE eventos ({', '.join([f'{col.lower().replace(' ', '_')} TEXT' for col in colunas])})"
            cursor.execute(create_query)
            for evento in dados:
                placeholders = ','.join(['?' for _ in evento])
                insert_query = f"INSERT INTO eventos ({','.join([col.lower().replace(' ', '_') for col in evento.keys()])}) VALUES ({placeholders})"
                cursor.execute(insert_query, list(evento.values()))

            conn.commit()

        conn.close()

    except sqlite3.Error as e:
        logger.error(f"Erro ao exportar para SQLite: {str(e)}", exc_info=True)
        raise Exception(f"Erro ao exportar para SQLite: {str(e)}")
