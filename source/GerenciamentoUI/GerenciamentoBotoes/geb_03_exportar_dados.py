import json
import xml.etree.ElementTree as ET
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def exportar_dados(self, tabela_dados, formato, nome_arquivo=None):
    try:
        if tabela_dados.rowCount() == 0:
            QMessageBox.warning(None, self.loc.get_text("warning"), self.loc.get_text("no_data"))
            return False

        apenas_colunas_ativas = False
        apenas_filtros_ativos = False
        apenas_selecao = False
        for widget in QApplication.topLevelWidgets():
            if hasattr(widget, 'gerenciador_menus_ui'):
                apenas_colunas_ativas = widget.gerenciador_menus_ui.acao_exportar_colunas_ativas.isChecked()
                apenas_filtros_ativos = widget.gerenciador_menus_ui.acao_exportar_filtros_ativos.isChecked()
                apenas_selecao = widget.gerenciador_menus_ui.acao_exportar_selecao.isChecked()
                break

        dados = []
        colunas_para_exportar = []
        gerenciador_colunas = None
        for widget in QApplication.topLevelWidgets():
            if hasattr(widget, 'gerenciador_colunas'):
                gerenciador_colunas = widget.gerenciador_colunas
                break

        if apenas_colunas_ativas and gerenciador_colunas:
            headers_visiveis = {coluna["nome"]: key for key, coluna in gerenciador_colunas.COLUNAS_DISPONIVEIS.items() if coluna["visivel"]}
            for col in range(tabela_dados.columnCount()):
                header_item = tabela_dados.horizontalHeaderItem(col)
                if header_item and header_item.text() in headers_visiveis:
                    colunas_para_exportar.append(col)

        else:
            colunas_para_exportar = list(range(tabela_dados.columnCount()))

        if apenas_selecao:
            selecao = tabela_dados.selectedIndexes()
            if not selecao:
                QMessageBox.warning(None, self.loc.get_text("warning"), 
                    self.loc.get_text("no_selection") if "no_selection" in self.loc.traducoes.get(self.loc.idioma_atual, {}) 
                    else "Nenhuma célula selecionada para exportação.")

                return False

            selecao_mapa = {}
            for indice in selecao:
                row = indice.row()
                col = indice.column()
                if apenas_colunas_ativas and col not in colunas_para_exportar:
                    continue

                if row not in selecao_mapa:
                    selecao_mapa[row] = set()

                selecao_mapa[row].add(col)

            for row, cols in sorted(selecao_mapa.items()):
                if apenas_filtros_ativos and tabela_dados.isRowHidden(row):
                    continue

                linha = {}
                for col in range(tabela_dados.columnCount()):
                    header_item = tabela_dados.horizontalHeaderItem(col)
                    if header_item and col in cols:
                        header = header_item.text()
                        item = tabela_dados.item(row, col)
                        linha[header] = item.text() if item else ""

                if linha:
                    dados.append(linha)

        else:
            linhas_para_exportar = []
            if apenas_filtros_ativos:
                linhas_para_exportar = [row for row in range(tabela_dados.rowCount()) if not tabela_dados.isRowHidden(row)]

            else:
                linhas_para_exportar = list(range(tabela_dados.rowCount()))

            for row in linhas_para_exportar:
                linha = {}
                for col in colunas_para_exportar:
                    header = tabela_dados.horizontalHeaderItem(col).text()
                    item = tabela_dados.item(row, col)
                    linha[header] = item.text() if item else ""

                dados.append(linha)

        df = pd.DataFrame(dados)
        try:
            if not nome_arquivo:
                if formato in ['xlsx', 'csv', 'txt']:
                    nome_arquivo, _ = QFileDialog.getSaveFileName(None, f"Exportar para {formato.upper()}", "", f"{formato.upper()} Files (*.{formato})")

                elif formato == 'json':
                    nome_arquivo, _ = QFileDialog.getSaveFileName(None, "Exportar para JSON", "", "JSON Files (*.json)")

                elif formato == 'xml':
                    nome_arquivo, _ = QFileDialog.getSaveFileName(None, "Exportar para XML", "", "XML Files (*.xml)")

                elif formato == 'db':
                    nome_arquivo, _ = QFileDialog.getSaveFileName(None, "Exportar para SQLite", "", "DB Files (*.db)")

            if nome_arquivo:
                try:
                    if formato == 'xlsx':
                        import os
                        import tempfile
                        import openpyxl
                        temp_dir = tempfile.gettempdir()
                        temp_file = os.path.join(temp_dir, "temp_export.xlsx")
                        df.to_excel(temp_file, index=False)
                        import shutil
                        shutil.copy2(temp_file, nome_arquivo)
                        os.remove(temp_file)

                    elif formato == 'csv':
                        df.to_csv(nome_arquivo, index=False)

                    elif formato == 'txt':
                        df.to_csv(nome_arquivo, index=False, sep='\t')

                    elif formato == 'json':
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            json.dump(dados, f, ensure_ascii=False, indent=4)

                    elif formato == 'xml':
                        root = ET.Element("eventos")
                        for evento in dados:
                            evento_element = ET.SubElement(root, "evento")
                            for key, value in evento.items():
                                child = ET.SubElement(evento_element, key.lower().replace(" ", "_"))
                                child.text = str(value)

                        tree = ET.ElementTree(root)
                        tree.write(nome_arquivo, encoding='utf-8', xml_declaration=True)

                    elif formato == 'db':
                        self._exportar_para_sqlite(dados, nome_arquivo)

                    return True

                except Exception as e:
                    import traceback
                    error_details = traceback.format_exc()
                    logger.error(f"Erro ao exportar arquivo ({formato}): {e}\n{error_details}", exc_info=True)
                    QMessageBox.critical(None, self.loc.get_text("export_error"), 
                        self.loc.get_text("export_error_details").format(formato, str(e), error_details))

                    return False

            return False

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"Erro na preparação para exportação: {e}\n{error_details}", exc_info=True)
            QMessageBox.critical(None, self.loc.get_text("error"), 
                self.loc.get_text("export_preparation_error").format(str(e), error_details))

            return False

    except Exception as e:
        logger.error(f"Erro ao exportar dados: {e}", exc_info=True)
        return
