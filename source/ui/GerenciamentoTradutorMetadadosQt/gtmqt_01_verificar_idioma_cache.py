from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _verificar_idioma_cache(self):
    try:
        if self._idioma_cache != self.loc.idioma_atual:
            self._cache_traducoes_tipo_operacao.clear()
            self._cache_traducoes_tipo.clear()
            self._cache_traducoes_atributos.clear()
            self._cache_traducoes_protegido.clear()
            self._idioma_cache = self.loc.idioma_atual

    except Exception as e:
        logger.error(f"Erro ao verificar idioma do cache: {e}", exc_info=True)
