from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def traduzir_tipo_operacao(self, valor, idioma_origem=None):
    try:
        self._verificar_idioma_cache()
        valor_normalizado = str(valor).lower().strip()
        cache_key = f"{valor_normalizado}_{idioma_origem or self.loc.idioma_atual}"
        if cache_key in self._cache_traducoes_tipo_operacao:
            return self._cache_traducoes_tipo_operacao[cache_key]

        valor_traduzido_reverso = self._obter_chave_traducao_reversa(valor_normalizado)
        if valor_traduzido_reverso:
            traducao = self.loc.get_text(valor_traduzido_reverso)
            self._cache_traducoes_tipo_operacao[cache_key] = traducao
            return traducao

        mapeamento_operacoes = {
            "moved": "op_moved",
            "renamed": "op_renamed", 
            "added": "op_added",
            "deleted": "op_deleted",
            "modified": "op_modified",
            "scanned": "op_scanned",

            "movido": "op_moved",
            "renomeado": "op_renamed",
            "adicionado": "op_added", 
            "excluído": "op_deleted",
            "modificado": "op_modified",
            "escaneado": "op_scanned",

            "movido": "op_moved",
            "renombrado": "op_renamed",
            "añadido": "op_added",
            "eliminado": "op_deleted",
            "modificado": "op_modified",
            "escanneado": "op_scanned",

            "déplacé": "op_moved",
            "renommé": "op_renamed", 
            "ajouté": "op_added",
            "supprimé": "op_deleted",
            "modifié": "op_modified",
            "numérisé": "op_scanned",

            "spostato": "op_moved",
            "rinominato": "op_renamed",
            "aggiunto": "op_added",
            "eliminato": "op_deleted",
            "modificato": "op_modified",
            "scansionato": "op_scanned",

            "verschoben": "op_moved",
            "umbenannt": "op_renamed",
            "hinzugefügt": "op_added",
            "gelöscht": "op_deleted",
            "geändert": "op_modified",
            "gescannt": "op_scanned"
        }

        chave_traducao = mapeamento_operacoes.get(valor_normalizado)
        if chave_traducao:
            traducao = self.loc.get_text(chave_traducao)
            self._cache_traducoes_tipo_operacao[cache_key] = traducao
            return traducao

        if valor_normalizado.startswith("op_"):
            traducao = self.loc.get_text(valor_normalizado)
            self._cache_traducoes_tipo_operacao[cache_key] = traducao
            return traducao

        for texto, chave in mapeamento_operacoes.items():
            if texto in valor_normalizado or valor_normalizado in texto:
                traducao = self.loc.get_text(chave)
                self._cache_traducoes_tipo_operacao[cache_key] = traducao
                return traducao

        self._cache_traducoes_tipo_operacao[cache_key] = valor
        return valor

    except Exception as e:
        logger.error(f"Erro ao traduzir tipo de operação '{valor}': {e}", exc_info=True)
        self._cache_traducoes_tipo_operacao[cache_key] = valor
        return
