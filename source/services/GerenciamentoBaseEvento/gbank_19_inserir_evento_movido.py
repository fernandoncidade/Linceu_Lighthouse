from datetime import datetime
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _inserir_evento_movido(self, cursor, evento):
    if not evento or evento.get("tipo_operacao") != self.observador.loc.get_text("op_moved"):
        return False

    try:
        colunas = [
            'tipo_operacao', 
            'nome', 
            'dir_anterior', 
            'dir_atual', 
            'data_criacao', 
            'data_modificacao',
            'data_acesso',
            'tipo',
            'size_b',
            'size_kb',
            'size_mb',
            'size_gb',
            'size_tb',
            'atributos',
            'autor',
            'dimensoes',
            'duracao',
            'taxa_bits', 
            'protegido', 
            'paginas',
            'linhas',
            'palavras',
            'paginas_estimadas',
            'linhas_codigo',
            'total_linhas',
            'slides_estimados',
            'arquivos',
            'unzipped_b',
            'unzipped_kb',
            'unzipped_mb',
            'unzipped_gb',
            'unzipped_tb',
            'slides',
            'binary_file_b',
            'binary_file_kb',
            'binary_file_mb',
            'binary_file_gb',
            'binary_file_tb',
            'planilhas',
            'colunas',
            'registros',
            'tabelas',
            'timestamp'
        ]

        valores = []
        for coluna in colunas:
            if coluna == "tipo_operacao":
                valores.append(self.observador.loc.get_text("op_moved"))

            elif coluna == "timestamp" and "timestamp" not in evento:
                valores.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

            else:
                valores.append(evento.get(coluna, ""))

        placeholders = ", ".join(["?" for _ in colunas])
        colunas_str = ", ".join(colunas)
        cursor.execute(f"INSERT INTO movido ({colunas_str}) VALUES ({placeholders})", valores)
        cursor.execute(f"INSERT INTO monitoramento ({colunas_str}) VALUES ({placeholders})", valores)
        return True

    except Exception as e:
        logger.error(f"Erro ao inserir evento movido: {e}", exc_info=True)
        return False
