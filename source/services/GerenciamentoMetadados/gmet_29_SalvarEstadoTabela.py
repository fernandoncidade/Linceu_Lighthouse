from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def salvar_estado_tabela(gc, tabela):
    eventos = []
    for row in range(tabela.rowCount()):
        evento = {}
        for col in range(tabela.columnCount()):
            header = tabela.horizontalHeaderItem(col).text()
            item = tabela.item(row, col)
            if item:
                evento[header] = item.text()

        eventos.append(evento)

    return eventos
