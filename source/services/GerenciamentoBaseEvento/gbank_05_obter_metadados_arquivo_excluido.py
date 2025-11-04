import sqlite3
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_metadados_arquivo_excluido(self, nome):
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    tipo_operacao,
                    nome,
                    dir_anterior,
                    dir_atual,
                    data_criacao,
                    data_modificacao,
                    data_acesso,
                    tipo,
                    size_b,
                    size_kb,
                    size_mb,
                    size_gb,
                    size_tb,
                    atributos,
                    autor,
                    dimensoes,
                    duracao,
                    taxa_bits,
                    protegido,
                    paginas,
                    linhas,
                    palavras,
                    paginas_estimadas,
                    linhas_codigo,
                    total_linhas,
                    slides_estimados,
                    arquivos,
                    unzipped_b,
                    unzipped_kb,
                    unzipped_mb,
                    unzipped_gb,
                    unzipped_tb,
                    slides,
                    binary_file_b,
                    binary_file_kb,
                    binary_file_mb,
                    binary_file_gb,
                    binary_file_tb,
                    planilhas,
                    colunas,
                    registros,
                    tabelas,
                    timestamp
                FROM monitoramento
                WHERE nome = ?
                ORDER BY id DESC
                LIMIT 1
            """, (nome,))

            resultado = cursor.fetchone()
            if resultado:
                colunas = ['tipo_operacao', 
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
                            'timestamp']
                return dict(zip(colunas, resultado))

            cursor.execute("""
                SELECT NULL as 
                        tipo_operacao,
                        nome,
                        diretorio as dir_anterior, 
                        diretorio as dir_atual, 
                        data_criacao,
                        data_modificacao,
                        data_acesso,
                        tipo,
                        size_b,
                        size_kb,
                        size_mb,
                        size_gb,
                        size_tb,
                        atributos,
                        autor,
                        dimensoes,
                        duracao,
                        taxa_bits,
                        protegido,
                        paginas,
                        linhas,
                        palavras,
                        paginas_estimadas,
                        linhas_codigo,
                        total_linhas,
                        slides_estimados,
                        arquivos,
                        unzipped_b,
                        unzipped_kb,
                        unzipped_mb,
                        unzipped_gb,
                        unzipped_tb,
                        slides,
                        binary_file_b,
                        binary_file_kb,
                        binary_file_mb,
                        binary_file_gb,
                        binary_file_tb,
                        planilhas,
                        colunas,
                        registros,
                        tabelas,
                        timestamp
                FROM snapshot
                WHERE nome = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (nome,))

            resultado = cursor.fetchone()
            if resultado:
                colunas = ['tipo_operacao', 
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
                        'timestamp']
                return dict(zip(colunas, resultado))

            return None

    except Exception as e:
        logger.error(f"Erro ao buscar metadados de arquivo excluído: {e}", exc_info=True)
        return None
