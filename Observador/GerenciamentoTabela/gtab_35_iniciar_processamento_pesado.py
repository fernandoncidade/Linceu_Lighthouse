from Observador.GerenciamentoTabela.gtab_32_worker_thread import WorkerThread

def iniciar_processamento_pesado(gt, dados, callback=None):
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
