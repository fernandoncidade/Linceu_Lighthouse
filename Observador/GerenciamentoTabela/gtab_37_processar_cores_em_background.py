from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _processar_cores_em_background(gt, dados):
    try:
        resultado = {}
        tabela = gt.interface.tabela_dados
        cores_operacao = gt._obter_cores_operacao()
        cor_padrao = cores_operacao.get(gt.loc.get_text("op_scanned"))
        cor_texto_padrao = gt.calcular_cor_texto_ideal(cor_padrao)
        header_indices = gt._obter_indices_colunas(tabela)
        colunas = list(gt.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS.items())
        for row in range(tabela.rowCount()):
            tipo_operacao_valor = ""
            indice_tipo_operacao = header_indices.get(
                gt.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS["tipo_operacao"]["nome"].replace('\n', ' ').strip()
            )

            if indice_tipo_operacao is not None:
                item_tipo = tabela.item(row, indice_tipo_operacao)
                tipo_operacao_valor = item_tipo.text() if item_tipo else ""

            for key, coluna in colunas:
                nome_coluna = coluna["nome"].replace('\n', ' ').strip()
                indice_coluna = header_indices.get(nome_coluna)
                if indice_coluna is None or indice_coluna >= tabela.columnCount():
                    continue

                if key != "tipo_operacao" and key not in gt.colunas_para_colorir:
                    cor_fundo = cor_padrao
                    cor_texto = cor_texto_padrao

                elif not gt.cores_visiveis:
                    cor_fundo = cor_padrao
                    cor_texto = cor_texto_padrao

                else:
                    cor_fundo = cores_operacao.get(tipo_operacao_valor, cor_padrao)
                    cor_texto = gt.calcular_cor_texto_ideal(cor_fundo, eh_coluna_personalizada=(key != "tipo_operacao"))

                resultado[(row, indice_coluna)] = (cor_fundo, cor_texto)

        return resultado

    except Exception as e:
        logger.error(f"Erro ao processar cores em background: {e}", exc_info=True)
