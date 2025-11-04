from Observador.GerenciamentoMetadados import identificar_tipo_arquivo as _identificar

def identificar_tipo_arquivo(gc, caminho):
    return _identificar(caminho, gc.loc)
