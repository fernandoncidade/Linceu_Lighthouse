from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _executar_retraducao_agendada(gt):
    if not gt._retraducao_agendada:
        return

    if gt._retraducao_realizada_para_idioma and gt.loc.idioma_atual == gt._idioma_ultima_retraducao:
        return

    gt._retraducao_agendada = False
    gt._retraducao_em_andamento = True
    try:
        if not hasattr(gt.interface, 'tabela_dados'):
            return

        tabela = gt.interface.tabela_dados
        tabela.blockSignals(True)
        tabela.viewport().setUpdatesEnabled(False)
        if hasattr(gt.interface, 'gerenciador_progresso_ui'):
            gt.interface.gerenciador_progresso_ui.criar_barra_progresso()
            gt.interface.rotulo_resultado.setText(gt.loc.get_text("translating_table"))

        header_indices = gt._obter_indices_colunas(tabela)
        colunas_traduziveis = ["tipo_operacao","atributos","protegido"]
        mapa_colunas = {}
        for key, coluna in gt.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items():
            nome_coluna = coluna["nome"].replace('\n', ' ').strip()
            mapa_colunas[nome_coluna] = key

        total_linhas = tabela.rowCount()
        for row in range(total_linhas):
            tipo_operacao_valor = None
            for nome_coluna, indice_coluna in header_indices.items():
                key = mapa_colunas.get(nome_coluna)
                if key == "tipo_operacao":
                    item = tabela.item(row, indice_coluna)
                    if item:
                        valor_atual = item.text()
                        valor_retraduzido = gt.loc.traduzir_tipo_operacao(valor_atual)
                        if valor_atual != valor_retraduzido:
                            item.setText(valor_retraduzido)

                        tipo_operacao_valor = valor_retraduzido

                    break

            for nome_coluna, indice_coluna in header_indices.items():
                key = mapa_colunas.get(nome_coluna)
                if key and key in colunas_traduziveis and key != "tipo_operacao":
                    item = tabela.item(row, indice_coluna)
                    if item:
                        valor_atual = item.text()
                        if valor_atual:
                            valor_retraduzido = gt.loc.traduzir_metadados(valor_atual, key)
                            if valor_atual != valor_retraduzido:
                                item.setText(valor_retraduzido)

            if tipo_operacao_valor and gt.cores_visiveis:
                gt.aplicar_cores_linha_especifica(tabela, row, tipo_operacao_valor)

            if hasattr(gt.interface, 'gerenciador_progresso_ui') and row % 100 == 0:
                progresso = int((row + 1) * 100 / total_linhas) if total_linhas else 100
                gt.interface.gerenciador_progresso_ui.atualizar_progresso_traducao(progresso, row + 1, total_linhas)
                QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao retraduzir dados existentes: {e}", exc_info=True)

    finally:
        try:
            if hasattr(gt.interface, 'tabela_dados'):
                tabela = gt.interface.tabela_dados
                tabela.viewport().setUpdatesEnabled(True)
                tabela.blockSignals(False)
                tabela.viewport().update()
                QApplication.processEvents()

        except Exception as e:
            logger.error(f"Erro ao finalizar atualização da tabela: {e}", exc_info=True)

        try:
            if hasattr(gt.interface, 'gerenciador_progresso_ui'):
                from InterfaceCore.ic_05_GerenciadorProgresso import GerenciadorProgresso
                GerenciadorProgresso.esconder_barra_progresso(gt.interface)
                gt.interface.rotulo_resultado.setText(gt.loc.get_text("translation_complete"))

        except Exception as e:
            logger.error(f"Erro ao finalizar barra de progresso: {e}", exc_info=True)

        gt._idioma_ultima_retraducao = gt.loc.idioma_atual
        gt._retraducao_realizada_para_idioma = True
        gt._retraducao_em_andamento = False
        gt._retraducao_agendada = False
