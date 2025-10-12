import os
from datetime import datetime
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def aplicar_filtros(self):
    try:
        self.salvar_estado_checkboxes()

        for chave in self.contadores:
            self.contadores[chave] = 0
            self.contadores_originais[chave] = 0

        texto_busca = self.parent.campo_busca.text().lower()
        extensoes = [ext.strip().lower() for ext in self.parent.campo_extensao.text().split(',') if ext.strip()]
        data_inicial = self.parent.data_inicial.dateTime().toPython()
        data_final = self.parent.data_final.dateTime().toPython()

        from PySide6.QtWidgets import QApplication
        main_window = None
        gerenciador_colunas = None

        for widget in QApplication.topLevelWidgets():
            if hasattr(widget, 'gerenciador_colunas'):
                main_window = widget
                gerenciador_colunas = widget.gerenciador_colunas
                break

        tabela = self.parent.tabela_dados

        indices_colunas = {}

        if gerenciador_colunas and hasattr(gerenciador_colunas, 'COLUNAS_DISPONIVEIS'):
            colunas_visiveis = [(key, col) for key, col in sorted(
                gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), 
                key=lambda x: x[1]["ordem"]) if col["visivel"]]

            indices_colunas = {key: idx for idx, (key, _) in enumerate(colunas_visiveis)}

        else:
            num_colunas = tabela.columnCount()

            for col in range(num_colunas):
                header_item = tabela.horizontalHeaderItem(col)
                if header_item:
                    header_text = header_item.text().lower()

                    if "operação" in header_text or "operacao" in header_text:
                        indices_colunas["tipo_operacao"] = col

                    elif "nome" in header_text:
                        indices_colunas["nome"] = col

                    elif "anterior" in header_text:
                        indices_colunas["dir_anterior"] = col

                    elif "atual" in header_text:
                        indices_colunas["dir_atual"] = col

                    elif "modif" in header_text:
                        indices_colunas["data_modificacao"] = col

                    elif "cria" in header_text:
                        indices_colunas["data_criacao"] = col

            if "tipo_operacao" not in indices_colunas:
                indices_colunas["tipo_operacao"] = 0

            if "nome" not in indices_colunas:
                indices_colunas["nome"] = 1

            if "dir_anterior" not in indices_colunas:
                indices_colunas["dir_anterior"] = 2

            if "dir_atual" not in indices_colunas:
                indices_colunas["dir_atual"] = 3

        operacao_para_chave = {
            self.parent.loc.get_text("op_moved"): "op_moved",
            self.parent.loc.get_text("op_renamed"): "op_renamed",
            self.parent.loc.get_text("op_added"): "op_added", 
            self.parent.loc.get_text("op_deleted"): "op_deleted",
            self.parent.loc.get_text("op_modified"): "op_modified",
            self.parent.loc.get_text("op_scanned"): "op_scanned"
        }

        for row in range(tabela.rowCount()):
            tipo_op_item = tabela.item(row, indices_colunas.get("tipo_operacao", 0))
            if tipo_op_item:
                tipo_op = tipo_op_item.text()
                chave_operacao = operacao_para_chave.get(tipo_op)
                if chave_operacao in self.contadores_originais:
                    self.contadores_originais[chave_operacao] += 1

        for row in range(tabela.rowCount()):
            mostrar = True
            tipo_op = None

            tipo_op_item = tabela.item(row, indices_colunas.get("tipo_operacao", 0))
            if tipo_op_item:
                tipo_op = tipo_op_item.text()
                if not self.verificar_filtro_operacao(tipo_op):
                    mostrar = False

            chave_operacao = operacao_para_chave.get(tipo_op)

            if mostrar and texto_busca:
                texto_encontrado = False
                campos_busca = ["nome", "dir_anterior", "dir_atual"]

                for campo in campos_busca:
                    if campo in indices_colunas:
                        item = tabela.item(row, indices_colunas[campo])
                        if item and texto_busca in item.text().lower():
                            texto_encontrado = True
                            break

                if not texto_encontrado:
                    mostrar = False

            if mostrar and extensoes:
                extensao_encontrada = False

                nome_item = tabela.item(row, indices_colunas.get("nome", 1))
                if nome_item:
                    nome_arquivo = nome_item.text()
                    extensao = os.path.splitext(nome_arquivo)[1].lower().lstrip('.')

                    if extensao in extensoes:
                        extensao_encontrada = True

                if not extensao_encontrada:
                    mostrar = False

            if mostrar:
                if chave_operacao == "op_moved" and hasattr(self.parent, 'ignorar_mover') and self.parent.ignorar_mover.isChecked():
                    pass

                elif chave_operacao == "op_renamed" and hasattr(self.parent, 'ignorar_renomeados') and self.parent.ignorar_renomeados.isChecked():
                    pass

                elif chave_operacao == "op_added" and hasattr(self.parent, 'ignorar_adicionados') and self.parent.ignorar_adicionados.isChecked():
                    pass

                elif chave_operacao == "op_deleted" and hasattr(self.parent, 'ignorar_excluidos') and self.parent.ignorar_excluidos.isChecked():
                    pass

                elif chave_operacao == "op_modified" and hasattr(self.parent, 'ignorar_data_modificados') and self.parent.ignorar_data_modificados.isChecked():
                    pass

                elif chave_operacao == "op_scanned" and hasattr(self.parent, 'ignorar_escaneados') and self.parent.ignorar_escaneados.isChecked():
                    pass

                elif chave_operacao == "op_moved" or chave_operacao == "op_renamed" or chave_operacao == "op_added" or chave_operacao == "op_deleted" or chave_operacao == "op_modified" or chave_operacao == "op_scanned":
                    data_item = None
                    for campo_data in ["data_modificacao", "data_criacao"]:
                        if campo_data in indices_colunas:
                            data_item = tabela.item(row, indices_colunas[campo_data])
                            if data_item and data_item.text().strip():
                                break

                    if data_item and data_item.text().strip():
                        try:
                            data_texto = data_item.text().strip()
                            try:
                                data_evento = datetime.strptime(data_texto, "%Y-%m-%d %H:%M:%S")

                            except ValueError:
                                try:
                                    data_evento = datetime.strptime(data_texto, "%d/%m/%Y %H:%M:%S")

                                except ValueError:
                                    data_evento = datetime.strptime(data_texto.split()[0], "%Y-%m-%d")

                            if not (data_inicial <= data_evento <= data_final):
                                mostrar = False
                                nome = tabela.item(row, indices_colunas.get("nome", 1)).text() if tabela.item(row, indices_colunas.get("nome", 1)) else "Desconhecido"

                        except Exception as e:
                            nome = tabela.item(row, indices_colunas.get("nome", 1)).text() if tabela.item(row, indices_colunas.get("nome", 1)) else "Desconhecido"
                            mostrar = True

                else:
                    data_item = None
                    for campo_data in ["data_modificacao", "data_criacao"]:
                        if campo_data in indices_colunas:
                            data_item = tabela.item(row, indices_colunas[campo_data])
                            if data_item and data_item.text().strip():
                                break

                    if data_item and data_item.text().strip():
                        try:
                            data_texto = data_item.text().strip()
                            data_evento = datetime.strptime(data_texto, "%Y-%m-%d %H:%M:%S")

                            if not (data_inicial <= data_evento <= data_final):
                                mostrar = False

                        except (ValueError, TypeError):
                            nome = tabela.item(row, indices_colunas.get("nome", 1)).text() if tabela.item(row, indices_colunas.get("nome", 1)) else "Desconhecido"
                            mostrar = True

            if mostrar and chave_operacao and chave_operacao in self.contadores:
                self.contadores[chave_operacao] += 1

            tabela.setRowHidden(row, not mostrar)

        self.sincronizar_menu_principal_com_filtros()
        self.parent.filtroAplicado.emit()

    except Exception as e:
        logger.error(f"Erro ao aplicar filtros: {e}", exc_info=True)
        for row in range(self.parent.tabela_dados.rowCount()):
            self.parent.tabela_dados.setRowHidden(row, False)
