from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def set_idioma(self, idioma: str):
    try:
        if idioma not in self.idiomas_suportados:
            logger.warning(f"Idioma não suportado: {idioma}")
            return

        if idioma == self.idioma_atual:
            return

        if hasattr(self, 'tradutor_metadados') and self.tradutor_metadados:
            self.tradutor_metadados._cache_traducoes_tipo_operacao.clear()
            self.tradutor_metadados._cache_traducoes_atributos.clear()
            self.tradutor_metadados._cache_traducoes_protegido.clear()

        if self.carregar_tradutor(idioma):
            self.idioma_atual = idioma
            self.salvar_preferencia_idioma(idioma)
            self.idioma_alterado.emit(idioma)
            self.traducoes_carregadas.emit(idioma)
            QApplication.processEvents()

    except Exception as e:
        logger.error(f"Erro ao alterar idioma: {e}", exc_info=True)
