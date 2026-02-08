from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_idioma_alterado(gt, idioma: str):
    try:
        if gt._retraducao_realizada_para_idioma and getattr(gt.loc, 'idioma_atual', None) == gt._idioma_ultima_retraducao:
            logger.debug("Retradução já realizada para este idioma; ignorando chamada.")
            return

        gt._idioma_alvo_retraducao = idioma
        gt._retraducao_realizada_para_idioma = False
        gt.retraduzir_dados_existentes()

    except Exception as e:
        logger.error(f"Erro no handler de idioma_alterado: {e}", exc_info=True)
