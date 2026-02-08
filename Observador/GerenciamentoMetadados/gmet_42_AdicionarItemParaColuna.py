def adicionar_item_para_coluna(gc, coluna_key, item):
    if coluna_key in gc.filas_colunas:
        gc.filas_colunas[coluna_key].put(item)
