import sqlite3
import threading
import queue
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

_instance = None
_instance_lock = threading.Lock()


class DatabaseWriter:
    def __init__(self, db_path, batch_size=500, batch_timeout=0.5):
        self.db_path = db_path
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self._q = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._started = False

    @classmethod
    def get_instance(cls, db_path):
        global _instance
        with _instance_lock:
            if _instance is None or _instance.db_path != db_path:
                _instance = DatabaseWriter(db_path)

            if not _instance._started:
                _instance.start()

            return _instance

    def start(self):
        try:
            self._thread.start()
            self._started = True

        except Exception as e:
            logger.error(f"Falha ao iniciar DatabaseWriter: {e}", exc_info=True)

    def stop(self):
        self._stop_event.set()
        self._q.put(None)
        if self._started:
            self._thread.join(timeout=2)

    def enqueue_event(self, tabela, evento):
        try:
            self._q.put_nowait((tabela, evento))

        except queue.Full:
            logger.warning("Fila de escrita cheia, evento descartado")

    def _ensure_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _worker(self):
        conn = None
        try:
            conn = self._ensure_connection()
            cursor = conn.cursor()
            while not self._stop_event.is_set():
                batch = []
                try:
                    item = self._q.get(timeout=self.batch_timeout)

                except queue.Empty:
                    item = None

                if item is None:
                    while len(batch) < self.batch_size:
                        try:
                            i = self._q.get_nowait()
                            if i is None:
                                break

                            batch.append(i)

                        except queue.Empty:
                            break

                else:
                    if item is not None:
                        batch.append(item)

                    while len(batch) < self.batch_size:
                        try:
                            i = self._q.get_nowait()
                            if i is None:
                                break

                            batch.append(i)

                        except queue.Empty:
                            break

                if not batch:
                    continue

                try:
                    cursor.execute("BEGIN TRANSACTION")
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
                    placeholders = ", ".join(["?" for _ in colunas])
                    colunas_str = ", ".join(colunas)
                    stmt_cache = {}
                    for tabela, evento in batch:
                        valores = [evento.get(c, "") for c in colunas]
                        valores[0] = evento.get("tipo_operacao", valores[0])
                        if tabela not in stmt_cache:
                            stmt_cache[tabela] = (
                                f"INSERT INTO {tabela} ({colunas_str}) VALUES ({placeholders})",
                                f"INSERT INTO monitoramento ({colunas_str}) VALUES ({placeholders})"
                            )
                        stmt_tab, stmt_mon = stmt_cache[tabela]
                        cursor.execute(stmt_tab, valores)
                        cursor.execute(stmt_mon, valores)

                    cursor.execute("COMMIT")

                except Exception as e:
                    try:
                        cursor.execute("ROLLBACK")

                    except Exception:
                        pass

                    logger.error(f"Erro ao persistir batch de eventos: {e}", exc_info=True)

        except Exception as e:
            logger.critical(f"DatabaseWriter falhou: {e}", exc_info=True)

        finally:
            try:
                if conn:
                    conn.close()

            except Exception:
                pass
