from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_interface_pos_processamento(gt, resultado):
    try:
        gt.atualizar_visualizacao_tabela()
        if hasattr(gt.interface, 'atualizar_status'):
            gt.interface.atualizar_status()

        if hasattr(gt.interface, 'atualizar_contador_eventos'):
            try:
                total_linhas = gt.interface.tabela_dados.rowCount()
                gt.interface.atualizar_contador_eventos(total_linhas)

            except Exception as e:
                logger.error(f"Erro ao atualizar contador de eventos: {e}", exc_info=True)

        if hasattr(gt, 'ajustar_cor_selecao'):
            gt.ajustar_cor_selecao()

    except Exception as e:
        logger.error(f"Erro ao atualizar interface após processamento: {e}", exc_info=True)
