from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def retraduzir_dados_existentes(gt):
    try:
        if gt._retraducao_realizada_para_idioma and gt.loc.idioma_atual == gt._idioma_ultima_retraducao:
            return

        if gt._retraducao_em_andamento:
            gt._retraducao_agendada = True
            return

        if gt._timer_retraducao.isActive():
            return

        gt._retraducao_agendada = True
        gt._timer_retraducao.start(50)

    except Exception as e:
        logger.error(f"Erro ao agendar retradução: {e}", exc_info=True)
