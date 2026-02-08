import os
import gc
import sqlite3
from PySide6.QtCore import QMutexLocker
from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()


class GerenciadorMonitoramento:
    def __init__(self, interface_principal):
        try:
            self.interface = interface_principal

        except Exception as e:
            logger.error(f"Erro ao inicializar GerenciadorMonitoramento: {e}", exc_info=True)

    def reiniciar_sistema_monitoramento(self):
        try:
            rows_antes = self.interface.tabela_dados.rowCount()

            if hasattr(self.interface, 'observador') and self.interface.observador:
                try:
                    self.interface.observador.parar()

                except Exception as e:
                    logger.error(f"Erro ao parar observador: {e}", exc_info=True)

                self.interface.observador = None

            if hasattr(self.interface, 'refresh_timer'):
                try:
                    self.interface.refresh_timer.stop()
                    self.interface.refresh_timer.timeout.disconnect()

                except Exception as e:
                    logger.error(f"Erro ao parar/desconectar refresh_timer: {e}", exc_info=True)

            if hasattr(self.interface, 'exclusao_timer'):
                try:
                    self.interface.exclusao_timer.stop()
                    self.interface.exclusao_timer.timeout.disconnect()

                except Exception as e:
                    logger.error(f"Erro ao parar/desconectar exclusao_timer: {e}", exc_info=True)

            try:
                self.interface.excluidos_recentemente.clear()

            except Exception as e:
                logger.error(f"Erro ao limpar excluídos recentemente: {e}", exc_info=True)

            if hasattr(self.interface, 'processador_evento'):
                try:
                    self.interface.processador_evento.evento_processado.disconnect()

                except Exception as e:
                    logger.error(f"Erro ao desconectar evento_processado: {e}", exc_info=True)

                self.interface.processador_evento = None

            if hasattr(self.interface, 'evento_base'):
                try:
                    with sqlite3.connect(self.interface.evento_base.db_path) as conn:
                        conn.execute("PRAGMA optimize")
                        conn.execute("VACUUM")
                        cursor = conn.cursor()
                        count = cursor.execute("SELECT COUNT(*) FROM monitoramento").fetchone()[0]

                except Exception as e:
                    logger.error(f"Erro ao otimizar banco de dados: {e}", exc_info=True)

            if hasattr(self.interface, 'gerenciador_colunas') and hasattr(self.interface.gerenciador_colunas, 'cache_metadados'):
                try:
                    self.interface.gerenciador_colunas.cache_metadados.clear()

                except Exception as e:
                    logger.error(f"Erro ao limpar cache_metadados: {e}", exc_info=True)

            if hasattr(self.interface, 'evento_buffer'):
                try:
                    with QMutexLocker(self.interface.evento_buffer.lock):
                        self.interface.evento_buffer.eventos.clear()

                    self.interface.evento_buffer.timer.stop()
                    self.interface.evento_buffer.timer = None
                    self.interface.evento_buffer = None

                except Exception as e:
                    logger.error(f"Erro ao limpar evento_buffer: {e}", exc_info=True)

            try:
                gc.collect()

            except Exception as e:
                logger.error(f"Erro ao executar garbage collector: {e}", exc_info=True)

            if hasattr(self.interface, 'evento_base'):
                try:
                    if hasattr(self.interface, 'painel_filtros'):
                        filtros_estado = {}
                        for op, checkbox in self.interface.painel_filtros.checkboxes_operacao.items():
                            filtros_estado[op] = checkbox.isChecked()

                    self.interface.tabela_dados.clearContents()
                    self.interface.tabela_dados.setRowCount(0)
                    with sqlite3.connect(self.interface.evento_base.db_path) as conn:
                        cursor = conn.cursor()
                        registros = cursor.execute("""
                            SELECT id, tipo_operacao, dir_atual, dir_anterior, timestamp, nome 
                            FROM monitoramento ORDER BY id
                        """).fetchall()

                        for registro in registros:
                            evento = {
                                'id': registro[0],
                                'tipo_operacao': registro[1],
                                'caminho': registro[2],
                                'caminho_antigo': registro[3],
                                'data': registro[4],
                                'arquivo': registro[5] or os.path.basename(registro[2] or registro[3] or "")
                            }
                            self.interface.adicionar_evento(evento)

                    if hasattr(self.interface, 'painel_filtros') and hasattr(self.interface.painel_filtros, 'administrador_filtros'):
                        self.interface.painel_filtros.administrador_filtros.aplicar_filtros()

                except Exception as e:
                    logger.error(f"Erro ao recarregar dados da tabela: {e}", exc_info=True)

            rows_depois = self.interface.tabela_dados.rowCount()

            try:
                QApplication.processEvents()

            except Exception as e:
                logger.error(f"Erro ao processar eventos do Qt: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao reiniciar sistema de monitoramento: {e}", exc_info=True)
