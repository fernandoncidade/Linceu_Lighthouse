from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def restaurar_estado_tabela(gc, tabela, eventos):
    try:
        tabela.clearContents()
        tabela.setRowCount(len(eventos))
        colunas_visiveis = [(key, col) for key, col in sorted(gc.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"]) if col["visivel"]]
        for row, evento in enumerate(eventos):
            for col, (key, coluna) in enumerate(colunas_visiveis):
                valor = evento.get(coluna["nome"], "")
                item = QTableWidgetItem(str(valor))
                if key == "tipo_operacao":
                    cores = {
                        gc.loc.get_text("op_renamed"): QColor(0, 255, 0),
                        gc.loc.get_text("op_added"): QColor(0, 0, 255),
                        gc.loc.get_text("op_deleted"): QColor(255, 0, 0),
                        gc.loc.get_text("op_modified"): QColor(255, 98, 0),
                        gc.loc.get_text("op_moved"): QColor(255, 0, 255),
                        gc.loc.get_text("op_scanned"): QColor(128, 128, 128)
                    }
                    item.setBackground(cores.get(valor, QColor(255, 255, 255)))

                tabela.setItem(row, col, item)

    except Exception as e:
        logger.error(f"Erro ao restaurar estado da tabela: {e}", exc_info=True)
