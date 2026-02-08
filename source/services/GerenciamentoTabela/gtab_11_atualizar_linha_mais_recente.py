import os
import sqlite3
from PySide6.QtWidgets import QTableWidgetItem, QApplication, QTableView
from source.services.GerenciamentoTabela.gtab_47_event_table_model import EventTableModel
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_linha_mais_recente(self, tabela_dados, evento=None):
    try:
        if isinstance(tabela_dados, QTableView) and isinstance(tabela_dados.model(), EventTableModel) and evento:
            try:
                tabela_dados.model().prepend_event(evento)
                if hasattr(self.interface, 'atualizar_contador_eventos'):
                    try:
                        current = getattr(self.interface, "contador_eventos_local", None)
                        if current is None:
                            db_path = self.interface.evento_base.db_path
                            with sqlite3.connect(db_path) as conn:
                                cursor = conn.cursor()
                                cursor.execute("SELECT COUNT(*) FROM monitoramento")
                                total = cursor.fetchone()[0]
                                self.interface.atualizar_contador_eventos(total)

                        else:
                            self.interface.contador_eventos_local = current + 1
                            self.interface.atualizar_contador_eventos(self.interface.contador_eventos_local)

                    except Exception:
                        pass

                return

            except Exception as e:
                logger.error(f"Falha ao inserir no modelo (view): {e}", exc_info=True)

        if evento:
            try:
                tabela_dados.insertRow(0)
                colunas_disponiveis = [(key, col) for key, col in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"])]
                getters = {key: getattr(self.interface.gerenciador_colunas, f"get_{key}", None)
                            for key, _ in colunas_disponiveis}

                tipo_operacao_valor = None
                for col, (key, _) in enumerate(colunas_disponiveis):
                    try:
                        getter = getters[key]
                        valor = getter(evento) if getter else evento.get(key, "")
                        if key == "tipo_operacao" and valor:
                            valor = self.loc.traduzir_tipo_operacao(valor)
                            tipo_operacao_valor = valor

                        elif key in [
                            "tipo_operacao",
                            "nome",
                            "dir_anterior",
                            "dir_atual",
                            "data_criacao",
                            "data_modificacao",
                            "data_acesso",
                            "tipo",
                            "size_b",
                            "size_kb",
                            "size_mb",
                            "size_gb",
                            "size_tb",
                            "atributos",
                            "autor",
                            "dimensoes",
                            "duracao",
                            "taxa_bits",
                            "protegido",
                            "paginas",
                            "linhas",
                            "palavras",
                            "paginas_estimadas",
                            "linhas_codigo",
                            "total_linhas",
                            "slides_estimados",
                            "arquivos",
                            "unzipped_b",
                            "unzipped_kb",
                            "unzipped_mb",
                            "unzipped_gb",
                            "unzipped_tb",
                            "slides",
                            "binary_file_b",
                            "binary_file_kb",
                            "binary_file_mb",
                            "binary_file_gb",
                            "binary_file_tb",
                            "planilhas",
                            "colunas",
                            "registros",
                            "tabelas"]:
                            valor = self.loc.traduzir_metadados(valor, key)

                        if key in ["dir_anterior", "dir_atual"] and valor:
                            valor = os.path.normpath(str(valor)).replace('/', '\\')
                            if valor == ".":
                                valor = ""

                        novo_texto = str(valor)
                        item = QTableWidgetItem(novo_texto)
                        tabela_dados.setItem(0, col, item)

                    except Exception as e:
                        logger.error(f"Erro ao processar coluna {key}: {e}", exc_info=True)
                        if not tabela_dados.item(0, col):
                            tabela_dados.setItem(0, col, QTableWidgetItem(""))

                if tipo_operacao_valor:
                    self.aplicar_cores_linha_especifica(tabela_dados, 0, tipo_operacao_valor)

                if hasattr(self.interface, 'atualizar_contador_eventos'):
                    try:
                        current = getattr(self.interface, "contador_eventos_local", None)
                        if current is None:
                            db_path = self.interface.evento_base.db_path
                            with sqlite3.connect(db_path) as conn:
                                cursor = conn.cursor()
                                cursor.execute("SELECT COUNT(*) FROM monitoramento")
                                total = cursor.fetchone()[0]
                                self.interface.atualizar_contador_eventos(total)

                        else:
                            self.interface.contador_eventos_local = current + 1
                            self.interface.atualizar_contador_eventos(self.interface.contador_eventos_local)

                    except Exception:
                        pass

                return
            except Exception as e:
                logger.error(f"Erro ao inserir evento direto na interface: {e}", exc_info=True)

        db_path = self.interface.evento_base.db_path
        with self.lock_db:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM monitoramento ORDER BY id DESC LIMIT 1")
                    registro = cursor.fetchone()
                    if not registro:
                        return

                    colunas_db = [desc[0] for desc in cursor.description]
                    evento_db = dict(zip(colunas_db, registro))
                    tabela_dados.insertRow(0)
                    colunas_disponiveis = [(key, col) for key, col in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"])]
                    getters = {key: getattr(self.interface.gerenciador_colunas, f"get_{key}", None)
                                for key, _ in colunas_disponiveis}

                    tipo_operacao_valor = None
                    for col, (key, _) in enumerate(colunas_disponiveis):
                        try:
                            getter = getters[key]
                            valor = getter(evento_db) if getter else evento_db.get(key, "")
                            if key == "tipo_operacao" and valor:
                                valor = self.loc.traduzir_tipo_operacao(valor)
                                tipo_operacao_valor = valor

                            elif key in [
                                "tipo_operacao",
                                "nome",
                                "dir_anterior",
                                "dir_atual",
                                "data_criacao",
                                "data_modificacao",
                                "data_acesso",
                                "tipo",
                                "size_b",
                                "size_kb",
                                "size_mb",
                                "size_gb",
                                "size_tb",
                                "atributos",
                                "autor",
                                "dimensoes",
                                "duracao", 
                                "taxa_bits",
                                "protegido",
                                "paginas",
                                "linhas",
                                "palavras",
                                "paginas_estimadas",
                                "linhas_codigo",
                                "total_linhas",
                                "slides_estimados",
                                "arquivos",
                                "unzipped_b",
                                "unzipped_kb",
                                "unzipped_mb",
                                "unzipped_gb",
                                "unzipped_tb",
                                "slides",
                                "binary_file_b",
                                "binary_file_kb",
                                "binary_file_mb",
                                "binary_file_gb",
                                "binary_file_tb",
                                "planilhas",
                                "colunas",
                                "registros",
                                "tabelas"]:
                                valor = self.loc.traduzir_metadados(valor, key)

                            if key in ["dir_anterior", "dir_atual"] and valor:
                                valor = os.path.normpath(str(valor)).replace('/', '\\')
                                if valor == ".":
                                    valor = ""

                            novo_texto = str(valor)
                            item = QTableWidgetItem(novo_texto)
                            tabela_dados.setItem(0, col, item)

                        except Exception as e:
                            logger.error(f"Erro ao processar coluna {key}: {e}", exc_info=True)
                            if not tabela_dados.item(0, col):
                                tabela_dados.setItem(0, col, QTableWidgetItem(""))

                    if tipo_operacao_valor:
                        self.aplicar_cores_linha_especifica(tabela_dados, 0, tipo_operacao_valor)

                    if hasattr(self.interface, 'atualizar_contador_eventos'):
                        cursor.execute("SELECT COUNT(*) FROM monitoramento")
                        total = cursor.fetchone()[0]
                        self.interface.atualizar_contador_eventos(total)

            except Exception as e:
                logger.error(f"Erro ao atualizar linha mais recente a partir do DB: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro crítico ao atualizar linha mais recente: {e}", exc_info=True)

    finally:
        try:
            tabela_dados.viewport().update()
            QApplication.processEvents()
            self.atualizacao_pendente = True

        except Exception:
            pass
