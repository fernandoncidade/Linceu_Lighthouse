import os
import sqlite3
from PySide6.QtWidgets import QTableWidgetItem, QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def atualizar_linha_mais_recente(self, tabela_dados):
    try:
        db_path = self.interface.evento_base.db_path
        with self.lock_db:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM monitoramento ORDER BY id DESC LIMIT 1")
                registro = cursor.fetchone()

                if not registro:
                    return

                colunas_db = [desc[0] for desc in cursor.description]
                evento = dict(zip(colunas_db, registro))

                tabela_dados.insertRow(0)

                colunas_visiveis = [(key, col) for key, col in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]) if col["visivel"]]

                getters = {key: getattr(self.interface.gerenciador_colunas, f"get_{key}", None)
                            for key, _ in colunas_visiveis}

                tipo_operacao_valor = None

                for col, (key, _) in enumerate(colunas_visiveis):
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
                            "tamanho",
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
                            "slides_estimadas",
                            "arquivos",
                            "descompactados",
                            "slides",
                            "binario",
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
                        print(f"Erro ao processar coluna {key}: {e}")
                        if not tabela_dados.item(0, col):
                            tabela_dados.setItem(0, col, QTableWidgetItem(""))

                if tipo_operacao_valor:
                    self.aplicar_cores_linha_especifica(tabela_dados, 0, tipo_operacao_valor)

                if hasattr(self.interface, 'atualizar_contador_eventos'):
                    cursor.execute("SELECT COUNT(*) FROM monitoramento")
                    total = cursor.fetchone()[0]
                    self.interface.atualizar_contador_eventos(total)

    except Exception as e:
        print(f"Erro crítico ao atualizar linha mais recente: {e}")

    finally:
        tabela_dados.viewport().update()
        QApplication.processEvents()
        self.atualizacao_pendente = True
