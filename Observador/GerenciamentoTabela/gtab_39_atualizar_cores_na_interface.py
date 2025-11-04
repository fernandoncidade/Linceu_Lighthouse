from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_cores_na_interface(gt, resultado):
    try:
        tabela = gt.interface.tabela_dados
        tabela.blockSignals(True)
        try:
            for (row, col), (cor_fundo, cor_texto) in resultado.items():
                item = tabela.item(row, col)
                if item:
                    item.setBackground(cor_fundo)
                    item.setForeground(cor_texto)

            tabela.viewport().update()

        finally:
            tabela.blockSignals(False)
            QApplication.processEvents()

        gt.atualizacao_pendente = True

    except Exception as e:
        logger.error(f"Erro ao atualizar cores na interface: {e}", exc_info=True)
