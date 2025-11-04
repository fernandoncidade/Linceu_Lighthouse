from PySide6.QtCore import QMetaObject, Qt, Q_ARG
import sqlite3
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_interface_apos_exclusao(self, evento=None):
    try:
        self.eventos_excluidos += 1
        interface = None
        if self.callback and hasattr(self.callback, '__self__'):
            interface = self.callback.__self__

        elif hasattr(self.observador, 'interface'):
            interface = self.observador.interface

        if not interface:
            return

        if evento:
            try:
                QMetaObject.invokeMethod(interface, "inserir_evento_streaming", Qt.ConnectionType.QueuedConnection, Q_ARG(dict, evento))
                return

            except Exception:
                pass

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM monitoramento WHERE tipo_operacao = ? ORDER BY id DESC LIMIT 1",
                               (self.observador.loc.get_text("op_deleted"),))

                registro = cursor.fetchone()
                if not registro:
                    interface.atualizar_status()
                    return

                colunas_db = [desc[0] for desc in cursor.description]
                evento_db = dict(zip(colunas_db, registro))
                if hasattr(interface, 'gerenciador_tabela'):
                    interface.gerenciador_tabela.atualizar_linha_mais_recente(interface.tabela_dados, evento=evento_db)

            interface.atualizar_status()

        except Exception as e:
            logger.error(f"Fallback (DB) pós-exclusão falhou: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao atualizar interface após exclusão: {e}", exc_info=True)
