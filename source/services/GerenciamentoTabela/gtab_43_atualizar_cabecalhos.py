from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_cabecalhos(gt):
    if not hasattr(gt, 'interface') or not hasattr(gt.interface, 'tabela_dados') or not hasattr(gt.interface, 'gerenciador_colunas'):
        logger.warning("Interface ou atributos necessários não estão prontos para atualizar cabeçalhos.")
        return

    try:
        from source.services.GerenciamentoTabela.gtab_09_atualizar_cabecalhos import atualizar_cabecalhos as _atualizar_cabecalhos_impl
        _atualizar_cabecalhos_impl(gt)

    except Exception as e:
        logger.error(f"Erro ao atualizar cabeçalhos: {e}", exc_info=True)
