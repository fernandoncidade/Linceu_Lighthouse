def extrair_metadados_em_lote(gc, lista_itens):
    futuros = []
    for item in lista_itens:
        futuros.append(gc.executor_metadados.submit(gc.get_metadados, item))

    for futuro in futuros:
        futuro.add_done_callback(gc._metadados_extraidos_callback)
