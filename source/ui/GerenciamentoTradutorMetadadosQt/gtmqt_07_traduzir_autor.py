from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_autor(self, valor):
    try:
        autor_mapeamento = {
            "autor desconhecido": "unknown_author",
            "autor desconhecido - excel": "xls",
            "autor desconhecido - access": "access",
            "autor desconhecido - outlook": "outllok",
            "autor desconhecido - publisher": "publisher", 
            "autor desconhecido - visio": "visio",
            "autor desconhecido - project": "project",
            "autor desconhecido - arquivo comprimido": "compressed_file",

            "unknown author": "unknown_author",
            "unknown author - excel": "xls",
            "unknown author - access": "access",
            "unknown author - outlook": "outllok",
            "unknown author - publisher": "publisher",
            "unknown author - visio": "visio",
            "unknown author - project": "project",
            "unknown author - compressed file": "compressed_file",

            "autor desconocido": "unknown_author",
            "autor desconocido - excel": "xls",
            "autor desconocido - access": "access",
            "autor desconocido - outlook": "outllok",
            "autor desconocido - publisher": "publisher",
            "autor desconocido - visio": "visio",
            "autor desconocido - project": "project",
            "autor desconocido - archivo comprimido": "compressed_file",

            "auteur inconnu": "unknown_author",
            "auteur inconnu - excel": "xls",
            "auteur inconnu - access": "access",
            "auteur inconnu - outlook": "outllok",
            "auteur inconnu - publisher": "publisher",
            "auteur inconnu - visio": "visio",
            "auteur inconnu - project": "project",
            "auteur inconnu - fichier compressé": "compressed_file",

            "autore sconosciuto": "unknown_author",
            "autore sconosciuto - excel": "xls",
            "autore sconosciuto - access": "access",
            "autore sconosciuto - outlook": "outllok",
            "autore sconosciuto - publisher": "publisher",
            "autore sconosciuto - visio": "visio",
            "autore sconosciuto - project": "project",
            "autore sconosciuto - file compresso": "compressed_file",

            "unbekannter autor": "unknown_author",
            "unbekannter autor - excel": "xls",
            "unbekannter autor - access": "access",
            "unbekannter autor - outlook": "outllok",
            "unbekannter autor - publisher": "publisher",
            "unbekannter autor - visio": "visio",
            "unbekannter autor - project": "project",
            "unbekannter autor - komprimierte datei": "compressed_file"
        }

        valor_lower = valor.lower()
        for texto, chave in autor_mapeamento.items():
            if texto == valor_lower:
                return self.loc.get_text(chave)

        return valor

    except Exception as e:
        logger.error(f"Error translating author: {e}", exc_info=True)
        return valor
