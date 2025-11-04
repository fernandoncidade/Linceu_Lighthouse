def callback_metadados(gc, futuro):
    try:
        caminho, metadados = futuro.result()
        with gc.lock_cache:
            gc.cache_metadados[caminho] = metadados

        gc.interface.atualizar_status()

    except Exception as e:
        print(f"Erro no callback: {e}")
