from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_cabecalhos(self):
    try:
        if not hasattr(self.interface, 'tabela_dados'):
            return

        tabela = self.interface.tabela_dados
        colunas_ordenadas = [(key, col) for key, col in sorted(self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items(), key=lambda x: x[1]["ordem"])]
        if tabela.columnCount() != len(colunas_ordenadas):
            self.configurar_tabela(tabela)
            return

        headers = []
        self.texto_original_cabecalhos = {}
        for i, (key, coluna) in enumerate(colunas_ordenadas):
            texto = coluna["nome"]
            self.texto_original_cabecalhos[i] = texto
            headers.append(texto)

        tabela.setHorizontalHeaderLabels(headers)
        try:
            self._cache_indices_colunas = {}

        except Exception:
            pass

        header = tabela.horizontalHeader()
        for i in range(tabela.columnCount()):
            item = tabela.horizontalHeaderItem(i)
            if item:
                texto = self.texto_original_cabecalhos.get(i, item.text()).replace('\n', ' ')
                item.setText(texto)
                item.setToolTip(texto)

        self._suspender_quebra_cabecalho = True
        try:
            self.ajustar_larguras_colunas(tabela, colunas_ordenadas)
            self.ajustar_altura_cabecalho(tabela)
            if not getattr(self, "_retraducao_realizada_para_idioma", False):
                self.retraduzir_dados_existentes()
                self.ajustar_larguras_colunas(tabela, colunas_ordenadas)
                self.ajustar_altura_cabecalho(tabela)

            for i in range(tabela.columnCount()):
                item = tabela.horizontalHeaderItem(i)
                if item:
                    texto = self.texto_original_cabecalhos.get(i, item.text()).replace('\n', ' ')
                    item.setText(texto)
                    item.setToolTip(texto)

        finally:
            self._suspender_quebra_cabecalho = False

        tabela.viewport().update()
        if hasattr(self, '_invalidar_cache_cores'):
            self._invalidar_cache_cores()

        QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao atualizar cabeçalhos: {e}", exc_info=True)
        raise
