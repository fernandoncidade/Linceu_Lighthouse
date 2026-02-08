from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_abas_graficos(self, graficos_atualizados, mapeamento_funcoes):
    try:
        if not self.tab_widget or self.tab_widget.count() == 0:
            return

        for i in range(self.tab_widget.count()):
            titulo_atual = self.tab_widget.tabText(i)

            func_correspondente = None
            for titulo_antigo, data in self.checkboxes_graficos.items():
                if titulo_antigo == titulo_atual:
                    func_correspondente = data['grafico_data']['func']
                    break

                elif titulo_atual in self.graficos_dados:
                    grafico_data = self.graficos_dados[titulo_atual]
                    if grafico_data.get('func'):
                        func_correspondente = grafico_data['func']
                        break

            if func_correspondente:
                novo_titulo = None
                for grafico in graficos_atualizados:
                    if grafico['func'] == func_correspondente:
                        novo_titulo = grafico['titulo']
                        break

                if novo_titulo and novo_titulo != titulo_atual:
                    self.tab_widget.setTabText(i, novo_titulo)
                    logger.debug(f"Aba atualizada de '{titulo_atual}' para '{novo_titulo}'")

    except Exception as e:
        logger.error(f"Erro ao atualizar abas dos gráficos: {e}", exc_info=True)
