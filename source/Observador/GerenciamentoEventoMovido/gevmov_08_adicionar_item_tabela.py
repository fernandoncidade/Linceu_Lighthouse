import os
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def normalizar_caminho(caminho):
    return os.path.normpath(caminho).replace('/', '\\')

def _adicionar_item_tabela(interfaceMonitor, evento, atualizar_interface=True):
    try:
        tipo_operacao_traduzido = interfaceMonitor.loc.get_text(evento["tipo_operacao"])
        if not interfaceMonitor.painel_filtros.verificar_filtro_operacao(tipo_operacao_traduzido):
            return

        row_position = 0
        interfaceMonitor.tabela_dados.insertRow(row_position)
        colunas_visiveis = [(key, col) for key, col in sorted(interfaceMonitor.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]) if col["visivel"]]
        cores = {
            interfaceMonitor.loc.get_text("op_renamed"): QColor(0, 255, 0),
            interfaceMonitor.loc.get_text("op_added"): QColor(0, 0, 255),
            interfaceMonitor.loc.get_text("op_deleted"): QColor(255, 0, 0),
            interfaceMonitor.loc.get_text("op_modified"): QColor(255, 98, 0),
            interfaceMonitor.loc.get_text("op_moved"): QColor(255, 0, 255),
            interfaceMonitor.loc.get_text("op_scanned"): QColor(128, 128, 128)
        }

        for col, (key, coluna) in enumerate(colunas_visiveis):
            try:
                valor = coluna["getter"](evento) if callable(coluna.get("getter")) else evento.get(key, "")
                if key == "tipo_operacao":
                    valor = interfaceMonitor.loc.get_text(valor)

                if key in ["dir_anterior", "dir_atual"] and valor:
                    valor = "" if not valor or valor == "." else normalizar_caminho(str(valor))

                valor_texto = str(valor)
                novo_item = QTableWidgetItem(valor_texto)
                if key == "tipo_operacao":
                    novo_item.setBackground(cores.get(valor, QColor(255, 255, 255)))

                interfaceMonitor.tabela_dados.setItem(row_position, col, novo_item)

            except Exception as e:
                logger.error(f"Erro ao adicionar item na coluna {key}: {e}", exc_info=True)
                interfaceMonitor.tabela_dados.setItem(row_position, col, QTableWidgetItem(""))

        if atualizar_interface:
            interfaceMonitor.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao adicionar item na tabela: {e}", exc_info=True)
