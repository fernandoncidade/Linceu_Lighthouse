from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def resetar_colunas(self):
    try:
        colunas_padrao = {
            "tipo_operacao": True,
            "nome": True,
            "dir_anterior": True,
            "dir_atual": True,
            "data_criacao": False,
            "data_modificacao": True,
            "data_acesso": False,
            "tipo": True,
            "size_b": False,
            "size_kb": True,
            "size_mb": False,
            "size_gb": False,
            "size_tb": False,
            "atributos": False,
            "autor": False,
            "dimensoes": False,
            "duracao": False,
            "taxa_bits": False,
            "protegido": False,
            "paginas": False,
            "linhas": False,
            "palavras": False,
            "paginas_estimadas": False,
            "linhas_codigo": False,
            "total_linhas": False,
            "slides_estimados": False,
            "arquivos": False,
            "unzipped_b": False,
            "unzipped_kb": False,
            "unzipped_mb": False,
            "unzipped_gb": False,
            "unzipped_tb": False,
            "slides": False,
            "binary_file_b": False,
            "binary_file_kb": False,
            "binary_file_mb": False,
            "binary_file_gb": False,
            "binary_file_tb": False,
            "planilhas": False,
            "colunas": False,
            "registros": False,
            "tabelas": False,
            "timestamp": True
        }

        for coluna, visivel in colunas_padrao.items():
            if coluna in self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS:
                self.interface.gerenciador_colunas.COLUNAS_DISPONIVEIS[coluna]["visivel"] = visivel

        if hasattr(self.interface, 'gerenciador_menus_ui') and hasattr(self.interface.gerenciador_menus_ui, 'acoes_colunas'):
            for coluna, acao in self.interface.gerenciador_menus_ui.acoes_colunas.items():
                if coluna in colunas_padrao:
                    acao.setChecked(colunas_padrao[coluna])

                else:
                    acao.setChecked(False)

        self.interface.gerenciador_colunas.salvar_configuracoes()
        if hasattr(self.interface.gerenciador_tabela, 'atualizar_visibilidade_colunas'):
            self.interface.gerenciador_tabela.atualizar_visibilidade_colunas(atualizar_em_massa=True)

        else:
            self.interface.atualizar_visibilidade_colunas()

        QMessageBox.information(self.interface, self.loc.get_text("success"), self.loc.get_text("columns_reset_success"))

    except Exception as e:
        logger.error(f"Erro ao resetar colunas: {e}", exc_info=True)
        QMessageBox.warning(self.interface, self.loc.get_text("error"), self.loc.get_text("columns_reset_error").format(str(e)))
