import json

def salvar_configuracoes(gc):
    config = {k: {"visivel": v["visivel"], "ordem": v["ordem"]} for k, v in gc.COLUNAS_DISPONIVEIS.items()}
    try:
        with open(gc.config_path, 'w') as f:
            json.dump(config, f, indent=4)

    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
