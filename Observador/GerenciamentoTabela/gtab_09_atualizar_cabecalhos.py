from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def atualizar_cabecalhos(self, idioma: str):
    try:
        if hasattr(self.interface, 'tabela_dados'):
            tabela = self.interface.tabela_dados

            self.configurar_tabela(tabela)
            self.aplicar_quebra_linha_todos_cabecalhos(tabela)
            self.ajustar_altura_cabecalho(tabela)

            logger.info(f"Cabeçalhos atualizados para o idioma: {idioma}")

            tabela.viewport().update()
            QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao atualizar cabeçalhos: {e}", exc_info=True)
