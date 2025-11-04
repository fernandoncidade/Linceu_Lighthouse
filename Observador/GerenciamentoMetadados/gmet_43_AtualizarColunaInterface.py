def atualizar_coluna_interface(gc, coluna_key=None):
    with gc.lock_resultados:
        if coluna_key and coluna_key in gc.resultados_colunas:
            resultados = gc.resultados_colunas[coluna_key]
            for item, valor in resultados:
                pass

            gc.resultados_colunas[coluna_key] = []
