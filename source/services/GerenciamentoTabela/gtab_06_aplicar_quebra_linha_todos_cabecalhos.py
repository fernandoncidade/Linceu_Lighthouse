from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def aplicar_quebra_linha_todos_cabecalhos(self, tabela):
    try:
        for i in range(tabela.columnCount()):
            self.aplicar_quebra_linha_cabecalho(tabela, i)

        self.ajustar_altura_cabecalho(tabela)

    except Exception as e:
        logger.error(f"Erro ao aplicar quebra de linha nos cabeçalhos: {e}", exc_info=True)
