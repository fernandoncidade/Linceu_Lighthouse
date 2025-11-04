from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_atributos(self, valor):
    try:
        atributos_mapeamento = {
            # Português
            "somente leitura": "readonly",
            "oculto": "hidden",
            "sistema": "system",
            "arquivo": "archive",
            "criptografado": "encrypted",
            "compactado": "compressed",
            "pasta": "folder",

            # English
            "read only": "readonly",
            "readonly": "readonly",
            "hidden": "hidden",
            "system": "system",
            "archive": "archive",
            "encrypted": "encrypted",
            "compressed": "compressed",
            "folder": "folder",

            # Español
            "solo lectura": "readonly",
            "oculto": "hidden",
            "sistema": "system",
            "archivo": "archive",
            "cifrado": "encrypted",
            "comprimido": "compressed",
            "carpeta": "folder",

            # Français
            "lecture seule": "readonly",
            "caché": "hidden",
            "système": "system",
            "fichier": "archive",
            "chiffré": "encrypted",
            "compressé": "compressed",
            "dossier": "folder",

            # Italiano
            "sola lettura": "readonly",
            "nascosto": "hidden",
            "sistema": "system",
            "archivio": "archive",
            "cifrato": "encrypted",
            "compresso": "compressed",
            "cartella": "folder",

            # Deutsch
            "schreibgeschützt": "readonly",
            "versteckt": "hidden",
            "system": "system",
            "datei": "archive",
            "verschlüsselt": "encrypted",
            "komprimiert": "compressed",
            "ordner": "folder",
        }

        partes = [parte.strip() for parte in valor.split(",")]
        partes_traduzidas = []

        for parte in partes:
            if not parte:
                continue

            parte_traduzida = parte
            parte_lower = parte.lower().strip()

            for texto, chave in atributos_mapeamento.items():
                if texto == parte_lower:
                    parte_traduzida = self.loc.get_text(chave)
                    break

            else:
                for texto, chave in atributos_mapeamento.items():
                    if texto in parte_lower or parte_lower in texto:
                        parte_traduzida = self.loc.get_text(chave)
                        break

            partes_traduzidas.append(parte_traduzida)

        return ", ".join(partes_traduzidas)

    except Exception as e:
        logger.error(f"Error translating attributes: {e}", exc_info=True)
        return valor
