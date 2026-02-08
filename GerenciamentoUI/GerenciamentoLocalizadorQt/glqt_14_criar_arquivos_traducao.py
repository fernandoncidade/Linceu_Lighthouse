import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def criar_arquivos_traducao(self):
    try:
        os.makedirs(self.translations_dir, exist_ok=True)

        pro_content = f"""
SOURCES += ../InterfaceCore/*.py \\
        ../GerenciamentoUI/*.py \\
        ../Filtros/*.py \\
        ../Observador/*.py

TRANSLATIONS += {' '.join([f'linceu_{idioma}.ts' for idioma in self.idiomas_suportados.keys()])}

CODECFORTR = UTF-8
"""

        pro_file = os.path.join(self.translations_dir, "linceu.pro")
        with open(pro_file, 'w', encoding='utf-8') as f:
            f.write(pro_content)

    except Exception as e:
        logger.error(f"Erro ao criar arquivos de tradução: {e}", exc_info=True)
