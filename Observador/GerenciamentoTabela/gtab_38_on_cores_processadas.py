def _on_cores_processadas(gt, future):
    resultado = future.result()
    gt.cores_processadas.emit(resultado)
