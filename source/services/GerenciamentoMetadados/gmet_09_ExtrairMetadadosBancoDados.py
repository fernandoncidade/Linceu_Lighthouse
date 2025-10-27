import os
import tempfile
import shutil
from urllib.parse import quote
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def extrair_metadados_banco_dados(caminho, loc):
    metadados = {}
    ext = os.path.splitext(caminho)[1].lower()

    try:
        if ext == '.sqlite' or ext == '.db':
            try:
                import sqlite3

                def _abrir_sqlite_ro(path_original):
                    norm = os.path.abspath(path_original).replace('\\', '/')
                    uri = f"file:{quote(norm)}?mode=ro&cache=shared&immutable=1"
                    conn = sqlite3.connect(uri, uri=True, timeout=3)
                    conn.execute("PRAGMA busy_timeout=3000")
                    return conn

                try:
                    conexao = _abrir_sqlite_ro(caminho)

                except Exception as e1:
                    logger.warning(f"SQLite bloqueado, tentando cópia temporária: {e1}")
                    tmp = None

                    try:
                        fd, tmp = tempfile.mkstemp(suffix='.db')
                        os.close(fd)
                        shutil.copy2(caminho, tmp)
                        conexao = sqlite3.connect(f"file:{quote(tmp.replace('\\', '/'))}?mode=ro&cache=shared&immutable=1", uri=True, timeout=3)
                        conexao.execute("PRAGMA busy_timeout=3000")

                    except Exception as e2:
                        logger.error(f"Falha ao abrir SQLite mesmo via cópia temporária: {e2}", exc_info=True)
                        if tmp and os.path.exists(tmp):
                            try:
                                os.remove(tmp)

                            except Exception:
                                pass

                        return metadados

                try:
                    cursor = conexao.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tabelas = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']

                    metadados['tabelas'] = len(tabelas)
                    metadados['nomes_tabelas'] = ", ".join(tabelas[:10])

                    total_linhas = 0
                    for nome_tabela in tabelas[:5]:
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM '{nome_tabela}';")
                            contagem = cursor.fetchone()[0]
                            total_linhas += int(contagem)

                        except Exception as e:
                            logger.error(f"Erro ao contar linhas da tabela {nome_tabela} no banco SQLite {caminho}: {e}", exc_info=True)

                    metadados['linhas_estimadas'] = total_linhas
                    metadados['registros'] = str(total_linhas)
                    metadados['linhas'] = str(total_linhas)

                finally:
                    try:
                        conexao.close()

                    except Exception:
                        pass

                    try:
                        if 'tmp' in locals() and tmp and os.path.exists(tmp):
                            os.remove(tmp)

                    except Exception:
                        pass

            except Exception as e:
                logger.error(f"Erro ao extrair metadados do banco SQLite {caminho}: {e}", exc_info=True)

        elif ext == '.mdb' or ext == '.accdb':
            try:
                import pyodbc
                conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' fr'DBQ={caminho};')
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()

                tabelas = []
                for tabela in cursor.tables(tableType='TABLE'):
                    tabelas.append(tabela.table_name)

                metadados['tabelas'] = len(tabelas)
                metadados['nomes_tabelas'] = ", ".join(tabelas[:10])

                conn.close()

            except Exception as e:
                logger.error(f"Erro ao extrair metadados do Access {caminho}: {e}", exc_info=True)
                metadados['tipo_acesso'] = "Microsoft Access Database"

    except Exception as e:
        logger.error(f"Erro geral ao extrair metadados do banco de dados {caminho}: {e}", exc_info=True)

    return metadados
