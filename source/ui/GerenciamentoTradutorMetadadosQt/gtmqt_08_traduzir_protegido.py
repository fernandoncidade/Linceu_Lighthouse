from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_protegido(self, valor):
    try:
        valores_sim = ["sim", "yes", "sí", "oui", "sì", "ja"]
        valores_nao = ["não", "no", "non", "nein"]

        valor_lower = valor.lower()

        if any(v in valor_lower for v in valores_sim):
            valor_sim_usado = next((v for v in valores_sim if valor_lower.startswith(v)), None)

            if valor_sim_usado:
                resto = valor[len(valor_sim_usado):].strip()

                if resto:
                    if resto.startswith(","):
                        resto = resto[1:].strip()

                    elif resto.startswith("("):
                        return f"{self.loc.get_text('yes')}{resto}"

                    if resto:
                        resto_traduzido = self._traduzir_atributos(resto)
                        return f"{self.loc.get_text('yes')}, {resto_traduzido}"

                return self.loc.get_text('yes')

        if any(v in valor_lower for v in valores_nao):
            return self.loc.get_text('no')

        return valor

    except Exception as e:
        logger.error(f"Erro ao traduzir protegido: {e}", exc_info=True)
        return valor
