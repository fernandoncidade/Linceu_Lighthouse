from PySide6.QtWidgets import QApplication

def _atualizar_cores_na_interface(gt, resultado):
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
