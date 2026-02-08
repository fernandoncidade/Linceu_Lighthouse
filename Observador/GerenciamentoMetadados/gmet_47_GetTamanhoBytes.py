import os

def _get_tamanho_bytes(gc, item):
    caminho = item.get("dir_atual") or item.get("dir_anterior")
    if caminho and os.path.exists(caminho):
        if os.path.isfile(caminho):
            return os.path.getsize(caminho)

        elif os.path.isdir(caminho):
            total = 0
            for root, dirs, files in os.walk(caminho):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))

                    except Exception:
                        pass

            return total

    return 0
