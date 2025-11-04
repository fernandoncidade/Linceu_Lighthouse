def atualizar_interface_pos_processamento(gt, resultado):
    gt.atualizar_visualizacao_tabela()
    if hasattr(gt.interface, 'atualizar_status'):
        gt.interface.atualizar_status()

    if hasattr(gt.interface, 'atualizar_contador_eventos'):
        try:
            total_linhas = gt.interface.tabela_dados.rowCount()
            gt.interface.atualizar_contador_eventos(total_linhas)

        except Exception:
            pass

    if hasattr(gt, 'ajustar_cor_selecao'):
        gt.ajustar_cor_selecao()
