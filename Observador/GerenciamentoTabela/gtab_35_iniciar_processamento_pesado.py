from Observador.GerenciamentoTabela.gtab_32_worker_thread import WorkerThread
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def iniciar_processamento_pesado(gt, dados, callback=None):
    try:
        def processamento_pesado(dados_):
            gt._invalidar_cache_cores()
            gt.aplicar_cores_todas_colunas()
            gt.redefinir_cores_todas_colunas()
            gt.atualizar_dados_tabela(gt.interface.tabela_dados)
            gt.atualizar_linha_mais_recente(gt.interface.tabela_dados)
            gt.atualizar_visualizacao_tabela()
            gt.atualizar_visibilidade_colunas(atualizar_em_massa=True)
            gt.atualizar_cores_colunas(aplicar_em_massa=True)
            gt.ajustar_cor_selecao()
            return True

        gt.worker = WorkerThread(dados, processamento_pesado)
        if callback:
            gt.worker.finished.connect(callback)

    except Exception as e:
        logger.error(f"Erro ao iniciar processamento pesado: {e}", exc_info=True)
