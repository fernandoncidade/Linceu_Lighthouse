import os
import sqlite3
from PySide6.QtWidgets import QTableWidgetItem, QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def atualizar_dados_tabela(self, tabela_dados, row_especifico=None):
    try:
        db_path = self.interface.evento_base.db_path
        with self.lock_db:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                colunas_disponiveis = [(key, col) for key, col in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"])]
                try:
                    if row_especifico is not None:
                        cursor.execute("""
                            SELECT * FROM monitoramento 
                            WHERE id = (SELECT id FROM monitoramento ORDER BY id DESC LIMIT 1 OFFSET ?)
                        """, (row_especifico,))

                    else:
                        cursor.execute("CREATE INDEX IF NOT EXISTS idx_monitoramento_id ON monitoramento(id)")
                        cursor.execute("SELECT * FROM monitoramento ORDER BY id DESC")

                    registros = cursor.fetchall()
                    colunas_db = [desc[0] for desc in cursor.description]
                    total_registros = len(registros)
                    if hasattr(self.interface, 'atualizar_contador_eventos'):
                        self.interface.atualizar_contador_eventos(total_registros)

                    if not row_especifico:
                        tabela_dados.setRowCount(total_registros)

                    getters = {key: getattr(self.interface.gerenciador_colunas, f"get_{key}", None)
                                for key, _ in colunas_disponiveis}

                    for idx, registro in enumerate(registros):
                        row = idx if row_especifico is None else row_especifico
                        evento = dict(zip(colunas_db, registro))
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
                                item = tabela_dados.item(row, col)
                                if item is None:
                                    item = QTableWidgetItem(novo_texto)
                                    tabela_dados.setItem(row, col, item)

                                else:
                                    if item.text() != novo_texto:
                                        item.setText(novo_texto)

                            except Exception as e:
                                print(f"Erro ao processar coluna {key}: {e}")
                                if not tabela_dados.item(row, col):
                                    tabela_dados.setItem(row, col, QTableWidgetItem(""))

                        if tipo_operacao_valor:
                            self.aplicar_cores_linha_especifica(tabela_dados, row, tipo_operacao_valor)

                except Exception as e:
                    print(f"Erro durante processamento: {e}")
                    raise

    except Exception as e:
        print(f"Erro crítico ao atualizar dados da tabela: {e}")

    finally:
        tabela_dados.viewport().update()
        QApplication.processEvents()
        self.atualizacao_pendente = True
