from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _limpar_dados_interface(self):
    try:
        if hasattr(self.interface, 'tabela_dados'):
            self.interface.tabela_dados.clearContents()
            self.interface.tabela_dados.setRowCount(0)
            self.interface.tabela_dados.viewport().update()

        if (hasattr(self.interface, 'gerenciador_colunas') and 
            hasattr(self.interface.gerenciador_colunas, 'cache_metadados')):
            self.interface.gerenciador_colunas.cache_metadados.clear()

        if (hasattr(self.interface, 'painel_filtros') and 
            hasattr(self.interface.painel_filtros, 'administrador_filtros')):
            self.interface.painel_filtros.administrador_filtros.limpar_filtros()

        if hasattr(self.interface, 'ultimo_salvamento'):
            self.interface.ultimo_salvamento = None

        if hasattr(self.interface, 'diretorio_atual'):
            self.interface.diretorio_atual = None

        if hasattr(self.interface, 'excluidos_recentemente'):
            self.interface.excluidos_recentemente.clear()

        if hasattr(self.interface, 'atualizar_status'):
            self.interface.atualizar_status()

    except Exception as e:
        logger.error(f"Erro ao limpar interface: {e}", exc_info=True)
