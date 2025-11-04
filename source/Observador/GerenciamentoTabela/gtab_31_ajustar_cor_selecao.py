from PySide6.QtGui import QColor
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def ajustar_cor_selecao(self):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados
        tema = self.detectar_tema_windows()

        for item in getattr(self, "_itens_selecionados_anteriores", []):
            if item not in tabela.selectedItems():
                col = item.column()
                nome_coluna = tabela.horizontalHeaderItem(col).text().replace('\n', ' ').strip()
                key_coluna = None
                for key, coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items():
                    if coluna["nome"].replace('\n', ' ').strip() == nome_coluna:
                        key_coluna = key
                        break

                cor_fundo = item.background().color()
                eh_personalizada = self.eh_coluna_personalizada_colorida(key_coluna) if key_coluna else False
                cor_texto = self.calcular_cor_texto_ideal(cor_fundo, eh_personalizada)
                item.setForeground(cor_texto)

        for item in tabela.selectedItems():
            col = item.column()
            nome_coluna = tabela.horizontalHeaderItem(col).text().replace('\n', ' ').strip()
            key_coluna = None
            for key, coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items():
                if coluna["nome"].replace('\n', ' ').strip() == nome_coluna:
                    key_coluna = key
                    break

            cor_fundo = item.background().color()

            if tema == "claro":
                cor_texto_selecao = QColor(0, 0, 0)

            elif tema == "escuro":
                cor_texto_selecao = QColor(255, 255, 255)

            else:
                eh_personalizada = self.eh_coluna_personalizada_colorida(key_coluna) if key_coluna else False
                cor_texto_selecao = self.calcular_cor_texto_ideal(cor_fundo, eh_personalizada)

            item.setForeground(cor_texto_selecao)

        self._itens_selecionados_anteriores = list(tabela.selectedItems())

    except Exception as e:
        logger.error(f"Erro ao ajustar cor de seleção: {e}", exc_info=True)
