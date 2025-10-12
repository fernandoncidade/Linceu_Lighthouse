from datetime import datetime
from source.Observador.GerenciamentoMetadados import identificar_tipo_arquivo
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _criar_evento_exclusao(self, nome_base, dir_anterior):
    try:
        metadados = self.obter_metadados_arquivo_excluido(nome_base)
        tipo_arquivo = None
        if metadados:
            return {
                "tipo_operacao": self.observador.loc.get_text("op_deleted"),
                "nome": nome_base,
                "dir_anterior": dir_anterior,
                "dir_atual": "",
                "data_criacao": metadados.get("data_criacao", ""),
                "data_modificacao": metadados.get("data_modificacao", ""),
                "data_acesso": metadados.get("data_acesso", ""),
                "tipo": metadados.get("tipo", ""),
                "size_b": metadados.get("size_b", ""),
                "size_kb": metadados.get("size_kb", ""),
                "size_mb": metadados.get("size_mb", ""),
                "size_gb": metadados.get("size_gb", ""),
                "size_tb": metadados.get("size_tb", ""),
                "atributos": metadados.get("atributos", ""),
                "autor": metadados.get("autor", ""),
                "dimensoes": metadados.get("dimensoes", ""),
                "duracao": metadados.get("duracao", ""),
                "taxa_bits": metadados.get("taxa_bits", ""),
                "protegido": metadados.get("protegido", ""),
                "paginas": metadados.get("paginas", ""),
                "linhas": metadados.get("linhas", ""),
                "palavras": metadados.get("palavras", ""),
                "paginas_estimadas": metadados.get("paginas_estimadas", ""),
                "linhas_codigo": metadados.get("linhas_codigo", ""),
                "total_linhas": metadados.get("total_linhas", ""),
                "slides_estimados": metadados.get("slides_estimados", ""),
                "arquivos": metadados.get("arquivos", ""),
                "unzipped_b": metadados.get("unzipped_b", ""),
                "unzipped_kb": metadados.get("unzipped_kb", ""),
                "unzipped_mb": metadados.get("unzipped_mb", ""),
                "unzipped_gb": metadados.get("unzipped_gb", ""),
                "unzipped_tb": metadados.get("unzipped_tb", ""),
                "slides": metadados.get("slides", ""),
                "binary_file_b": metadados.get("binary_file_b", ""),
                "binary_file_kb": metadados.get("binary_file_kb", ""),
                "binary_file_mb": metadados.get("binary_file_mb", ""),
                "binary_file_gb": metadados.get("binary_file_gb", ""),
                "binary_file_tb": metadados.get("binary_file_tb", ""),
                "planilhas": metadados.get("planilhas", ""),
                "colunas": metadados.get("colunas", ""),
                "registros": metadados.get("registros", ""),
                "tabelas": metadados.get("tabelas", "")
            }

        if tipo_arquivo is None:
            tipo_arquivo = identificar_tipo_arquivo(nome_base, self.observador.loc)

        return {
            "tipo_operacao": self.observador.loc.get_text("op_deleted"),
            "nome": nome_base,
            "dir_anterior": dir_anterior,
            "dir_atual": "",
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_modificacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_acesso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo_arquivo,
            "size_b": "",
            "size_kb": "",
            "size_mb": "",
            "size_gb": "",
            "size_tb": "",
            "atributos": "",
            "autor": "",
            "dimensoes": "",
            "duracao": "",
            "taxa_bits": "",
            "protegido": "",
            "paginas": "",
            "linhas": "",
            "palavras": "",
            "paginas_estimadas": "",
            "linhas_codigo": "",
            "total_linhas": "",
            "slides_estimados": "",
            "arquivos": "",
            "unzipped_b": "",
            "unzipped_kb": "",
            "unzipped_mb": "",
            "unzipped_gb": "",
            "unzipped_tb": "",
            "slides": "",
            "binary_file_b": "",
            "binary_file_kb": "",
            "binary_file_mb": "",
            "binary_file_gb": "",
            "binary_file_tb": "",
            "planilhas": "",
            "colunas": "",
            "registros": "",
            "tabelas": ""
        }

    except Exception as e:
        logger.error(f"Erro ao criar evento de exclusão: {e}", exc_info=True)
