from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_tipo_arquivo(self, valor):
    try:
        tipo_mapeamento = {
            "pasta": "file_folder",
            "vídeo": "file_video",
            "imagem": "file_image",
            "áudio": "file_audio",
            "audio": "file_audio",
            "código fonte": "file_source_code",
            "documento": "file_document",
            "planilha": "file_spreadsheet",
            "apresentação": "file_presentation",
            "banco de dados": "file_database",
            "executável": "file_executable",
            "temporário": "file_temp",
            "compactado": "file_compressed",
            "backup": "file_backup",
            "registro": "file_log",
            "configuração": "file_config",
            "desconhecido": "unknown",

            "folder": "file_folder",
            "video": "file_video",
            "image": "file_image",
            "audio": "file_audio",
            "source code": "file_source_code",
            "document": "file_document",
            "spreadsheet": "file_spreadsheet",
            "presentation": "file_presentation",
            "database": "file_database",
            "executable": "file_executable",
            "temporary": "file_temp",
            "compressed": "file_compressed",
            "backup": "file_backup",
            "registry": "file_log",
            "config": "file_config",
            "unknown": "unknown",

            "carpeta": "file_folder",
            "video": "file_video",
            "imagen": "file_image",
            "audio": "file_audio",
            "código fuente": "file_source_code",
            "documento": "file_document",
            "hoja de cálculo": "file_spreadsheet",
            "presentación": "file_presentation",
            "base de datos": "file_database",
            "ejecutable": "file_executable",
            "temporal": "file_temp",
            "comprimido": "file_compressed",
            "respaldo": "file_backup",
            "registro": "file_log",
            "configuración": "file_config",
            "desconocido": "unknown",

            "dossier": "file_folder",
            "vidéo": "file_video",
            "image": "file_image",
            "audio": "file_audio",
            "code source": "file_source_code",
            "document": "file_document",
            "tableur": "file_spreadsheet",
            "présentation": "file_presentation",
            "base de données": "file_database",
            "exécutable": "file_executable",
            "temporaire": "file_temp",
            "compressé": "file_compressed",
            "sauvegarde": "file_backup",
            "registre": "file_log",
            "configuration": "file_config",
            "inconnu": "unknown",

            "cartella": "file_folder",
            "video": "file_video",
            "immagine": "file_image",
            "audio": "file_audio",
            "codice sorgente": "file_source_code",
            "documento": "file_document",
            "foglio di calcolo": "file_spreadsheet",
            "presentazione": "file_presentation",
            "database": "file_database",
            "eseguibile": "file_executable",
            "temporaneo": "file_temp",
            "compresso": "file_compressed",
            "backup": "file_backup",
            "registro": "file_log",
            "configurazione": "file_config",
            "sconosciuto": "unknown",

            "ordner": "file_folder",
            "video": "file_video",
            "bild": "file_image",
            "audio": "file_audio",
            "quellcode": "file_source_code",
            "dokument": "file_document",
            "tabellenkalkulation": "file_spreadsheet",
            "präsentation": "file_presentation",
            "datenbank": "file_database",
            "ausführbar": "file_executable",
            "vorübergehend": "file_temp",
            "komprimiert": "file_compressed",
            "sicherung": "file_backup",
            "protokoll": "file_log",
            "konfiguration": "file_config",
            "unbekannt": "unknown"
        }

        valor_lower = valor.lower()
        for texto, chave in tipo_mapeamento.items():
            if texto in valor_lower:
                return self.loc.get_text(chave)

        return valor

    except Exception as e:
        logger.error(f"Error translating file type: {e}", exc_info=True)
        return valor
