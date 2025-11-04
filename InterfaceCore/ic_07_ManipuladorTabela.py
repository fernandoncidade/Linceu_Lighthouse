from utils.LogManager import LogManager
logger = LogManager.get_logger()


class ManipuladorTabela:
    @staticmethod
    def configurar_tabela(interface):
        try:
            if not hasattr(interface, 'gerenciador_tabela'):
                logger.error("GerenciadorTabela não foi inicializado")
                return

            if not hasattr(interface, 'tabela_dados'):
                logger.error("Tabela de dados não foi inicializada")
                return

            interface.gerenciador_tabela.configurar_tabela(interface.tabela_dados)
            if not hasattr(interface.gerenciador_tabela, '_conexoes_configuradas'):
                interface.gerenciador_tabela.cores_processadas.connect(interface._atualizar_cores_tabela)
                interface.gerenciador_tabela._conexoes_configuradas = True

        except Exception as e:
            logger.error(f"Erro ao configurar tabela: {e}", exc_info=True)

    @staticmethod
    def atualizar_visibilidade_colunas(interface, atualizar_em_massa=False):
        try:
            if hasattr(interface, 'gerenciador_tabela'):
                interface.gerenciador_tabela.atualizar_visibilidade_colunas(atualizar_em_massa)
                if hasattr(interface, 'tabela_dados'):
                    interface.gerenciador_tabela.ajustar_altura_cabecalho(interface.tabela_dados)

                if (atualizar_em_massa and 
                    hasattr(interface.gerenciador_tabela, 'aplicar_cores_todas_colunas_processamento')):
                    dados_processamento = {'atualizar_visibilidade': True}
                    interface.gerenciador_tabela.aplicar_cores_todas_colunas_processamento(dados_processamento)

                interface.atualizar_status()

            else:
                logger.warning("gerenciador_tabela não está disponível para atualizar visibilidade das colunas")

        except Exception as e:
            logger.error(f"Erro ao atualizar visibilidade das colunas: {e}", exc_info=True)

    @staticmethod
    def processar_cores_assincronamente(interface, dados=None):
        try:
            if hasattr(interface, 'gerenciador_tabela'):
                if hasattr(interface.gerenciador_tabela, 'aplicar_cores_todas_colunas_processamento'):
                    dados_processamento = dados or {'processamento_manual': True}
                    interface.gerenciador_tabela.aplicar_cores_todas_colunas_processamento(dados_processamento)

                else:
                    logger.warning("Método de processamento assíncrono não disponível")

            else:
                logger.warning("GerenciadorTabela não disponível para processamento assíncrono")

        except Exception as e:
            logger.error(f"Erro ao iniciar processamento assíncrono de cores: {e}", exc_info=True)

    @staticmethod
    def aguardar_processamentos_pendentes(interface, timeout=5):
        try:
            if hasattr(interface, 'gerenciador_tabela') and hasattr(interface.gerenciador_tabela, 'executor'):
                import time
                start_time = time.time()
                executor = interface.gerenciador_tabela.executor
                while time.time() - start_time < timeout:
                    if hasattr(executor, '_threads') and any(t.is_alive() for t in executor._threads):
                        time.sleep(0.1)
                        continue

                    break

        except Exception as e:
            logger.error(f"Erro ao aguardar processamentos: {e}", exc_info=True)
