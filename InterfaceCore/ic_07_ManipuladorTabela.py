from utils.LogManager import LogManager


class ManipuladorTabela:
    @staticmethod
    def configurar_tabela(interface):
        logger = LogManager.get_logger()
        try:
            logger.debug("Configurando tabela de dados")
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

            logger.debug("Tabela configurada com sucesso")

        except Exception as e:
            logger.error(f"Erro ao configurar tabela: {e}", exc_info=True)

    @staticmethod
    def atualizar_visibilidade_colunas(interface, atualizar_em_massa=False):
        logger = LogManager.get_logger()
        try:
            logger.debug("Atualizando visibilidade das colunas")
            if hasattr(interface, 'gerenciador_tabela'):
                interface.gerenciador_tabela.atualizar_visibilidade_colunas(atualizar_em_massa)
                if hasattr(interface, 'tabela_dados'):
                    interface.gerenciador_tabela.ajustar_altura_cabecalho(interface.tabela_dados)

                if (atualizar_em_massa and 
                    hasattr(interface.gerenciador_tabela, 'aplicar_cores_todas_colunas_processamento')):
                    dados_processamento = {'atualizar_visibilidade': True}
                    interface.gerenciador_tabela.aplicar_cores_todas_colunas_processamento(dados_processamento)

                interface.atualizar_status()
                logger.info("Visibilidade das colunas atualizada com sucesso")

            else:
                logger.warning("gerenciador_tabela não está disponível para atualizar visibilidade das colunas")

        except Exception as e:
            logger.error(f"Erro ao atualizar visibilidade das colunas: {e}", exc_info=True)

    @staticmethod
    def processar_cores_assincronamente(interface, dados=None):
        logger = LogManager.get_logger()
        try:
            if hasattr(interface, 'gerenciador_tabela'):
                if hasattr(interface.gerenciador_tabela, 'aplicar_cores_todas_colunas_processamento'):
                    dados_processamento = dados or {'processamento_manual': True}
                    interface.gerenciador_tabela.aplicar_cores_todas_colunas_processamento(dados_processamento)
                    logger.debug("Processamento assíncrono de cores iniciado")

                else:
                    logger.warning("Método de processamento assíncrono não disponível")

            else:
                logger.warning("GerenciadorTabela não disponível para processamento assíncrono")

        except Exception as e:
            logger.error(f"Erro ao iniciar processamento assíncrono de cores: {e}", exc_info=True)

    @staticmethod
    def aguardar_processamentos_pendentes(interface, timeout=5):
        logger = LogManager.get_logger()
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

                logger.debug("Aguarda de processamentos concluída")

        except Exception as e:
            logger.error(f"Erro ao aguardar processamentos: {e}", exc_info=True)
