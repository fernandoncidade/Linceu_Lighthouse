def _get_size_unit(gc, item, unidade):
    tamanho_bytes = gc._get_tamanho_bytes(item)
    if unidade == "B":
        return int(tamanho_bytes)

    elif unidade == "KB":
        return round(tamanho_bytes / 1024, 2)

    elif unidade == "MB":
        return round(tamanho_bytes / 1024**2, 2)

    elif unidade == "GB":
        return round(tamanho_bytes / 1024**3, 2)

    elif unidade == "TB":
        return round(tamanho_bytes / 1024**4, 2)

    return 0
