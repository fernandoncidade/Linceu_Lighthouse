from utils.LogManager import LogManager
logger = LogManager.get_logger()

def traduzir_metadados(self, valor, campo):
    try:
        self._verificar_idioma_cache()
        if not valor or not isinstance(valor, str):
            return valor

        campo_lower = campo.lower()
        cache_key = f"{valor}_{campo_lower}_{self.loc.idioma_atual}"

        if campo_lower in ["tipo", "type"]:
            if cache_key in self._cache_traducoes_tipo:
                return self._cache_traducoes_tipo[cache_key]

            resultado = self._traduzir_tipo_arquivo(valor)
            self._cache_traducoes_tipo[cache_key] = resultado
            return resultado

        elif campo_lower in ["atributos", "attributes"]:
            if cache_key in self._cache_traducoes_atributos:
                return self._cache_traducoes_atributos[cache_key]

            resultado = self._traduzir_atributos(valor)
            self._cache_traducoes_atributos[cache_key] = resultado
            return resultado

        elif campo_lower in ["protegido", "protected"]:
            if cache_key in self._cache_traducoes_protegido:
                return self._cache_traducoes_protegido[cache_key]

            resultado = self._traduzir_protegido(valor)
            self._cache_traducoes_protegido[cache_key] = resultado
            return resultado

        campo_lower = campo.lower()

        if campo_lower in ["autor", "author"]:
            return self._traduzir_autor(valor)

        elif campo_lower in ["dimensoes", "dimensions", "tamanho", "size"]:
            return self._traduzir_dimensoes(valor)

        else:
            return valor

    except Exception as e:
        logger.error(f"Erro ao traduzir metadados '{valor}' do campo '{campo}': {e}", exc_info=True)
        return
