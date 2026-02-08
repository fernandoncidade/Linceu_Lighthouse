def adicionar_metadados_ao_item(gc, item):
    try:
        metadados = gc.get_metadados(item)
        if metadados:
            for campo, valor in metadados.items():
                if campo not in item or not item[campo]:
                    item[campo] = valor

        return item

    except Exception as e:
        print(f"Erro ao adicionar metadados ao item: {e}")
        return item
