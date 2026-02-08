def aplicar_cores_todas_colunas_processamento(gt, dados):
    future = gt.executor.submit(gt._processar_cores_em_background, dados)
    future.add_done_callback(gt._on_cores_processadas)
