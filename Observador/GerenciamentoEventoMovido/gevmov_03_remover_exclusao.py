import sqlite3
from PySide6.QtCore import QTimer
from Observador.GerenciamentoEventoMovido.gevmov_04_atualizar_linha_recente import _atualizar_linha_recente
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _remover_exclusao(interfaceMonitor, nome, dir_anterior, exclusao_id=None):
    try:
        with sqlite3.connect(interfaceMonitor.evento_base.db_path) as conn:
            conn.execute('PRAGMA synchronous = OFF')
            conn.execute('PRAGMA journal_mode = WAL')
            cursor = conn.cursor()
            try:
                cursor.execute("BEGIN IMMEDIATE TRANSACTION")
                if exclusao_id:
                    cursor.execute("""
                        SELECT id FROM monitoramento 
                        WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                        ORDER BY id DESC LIMIT 1
                    """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior))

                    resultado = cursor.fetchone()
                    if resultado:
                        registro_id = resultado[0]
                        cursor.execute("""
                            DELETE FROM monitoramento 
                            WHERE id = ?
                        """, (registro_id,))

                        cursor.execute("""
                            DELETE FROM excluido 
                            WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                            AND timestamp = (SELECT timestamp FROM monitoramento WHERE id = ?)
                        """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior, registro_id))

                else:
                    cursor.execute("""
                        DELETE FROM monitoramento 
                        WHERE id IN (
                            SELECT id FROM monitoramento
                            WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                            ORDER BY id DESC LIMIT 1
                        )
                    """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior))

                    cursor.execute("""
                        DELETE FROM excluido 
                        WHERE id IN (
                            SELECT id FROM excluido
                            WHERE tipo_operacao = ? AND nome = ? AND dir_anterior = ?
                            ORDER BY id DESC LIMIT 1
                        )
                    """, (interfaceMonitor.loc.get_text("op_deleted"), nome, dir_anterior))

                cursor.execute("COMMIT")

            except sqlite3.Error as e:
                cursor.execute("ROLLBACK")
                logger.error(f"Erro SQL ao remover exclusão: {e}", exc_info=True)
                return False

        QTimer.singleShot(0, lambda: _atualizar_linha_recente(interfaceMonitor))
        return True

    except Exception as e:
        logger.error(f"Erro ao remover registro de exclusão: {e}", exc_info=True)
        return False
