import re
from utils.LogManager import LogManager


class TradutorMetadadosQt:
    def __init__(self, localizador):
        self.loc = localizador
        self.logger = LogManager.get_logger()
        self._cache_traducoes_tipo_operacao = {}
        self._cache_traducoes_tipo = {}
        self._cache_traducoes_atributos = {}
        self._cache_traducoes_protegido = {}
        self._idioma_cache = self.loc.idioma_atual

    def _verificar_idioma_cache(self):
        if self._idioma_cache != self.loc.idioma_atual:
            self._cache_traducoes_tipo_operacao.clear()
            self._cache_traducoes_tipo.clear()
            self._cache_traducoes_atributos.clear()
            self._cache_traducoes_protegido.clear()
            self._idioma_cache = self.loc.idioma_atual

    def traduzir_tipo_operacao(self, valor, idioma_origem=None):
        self._verificar_idioma_cache()
        valor_normalizado = str(valor).lower().strip()
        cache_key = f"{valor_normalizado}_{idioma_origem or self.loc.idioma_atual}"
        if cache_key in self._cache_traducoes_tipo_operacao:
            return self._cache_traducoes_tipo_operacao[cache_key]

        try:
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
            self.logger.error(f"Erro ao traduzir tipo de operação '{valor}': {e}", exc_info=True)
            self._cache_traducoes_tipo_operacao[cache_key] = valor
            return valor

    def _obter_chave_traducao_reversa(self, valor):
        try:
            for chave in ["op_moved", "op_renamed", "op_added", "op_deleted", "op_modified", "op_scanned"]:
                traducao_atual = self.loc.get_text(chave).lower().strip()
                if traducao_atual == valor:
                    return chave

            return None

        except:
            return None

    def traduzir_metadados(self, valor, campo):
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

        try:
            campo_lower = campo.lower()

            if campo_lower in ["autor", "author"]:
                return self._traduzir_autor(valor)

            elif campo_lower in ["dimensoes", "dimensions", "tamanho", "size"]:
                return self._traduzir_dimensoes(valor)

            else:
                return valor

        except Exception as e:
            self.logger.error(f"Erro ao traduzir metadados '{valor}' do campo '{campo}': {e}", exc_info=True)
            return valor

    def _traduzir_tipo_arquivo(self, valor):
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

    def _traduzir_atributos(self, valor):
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

    def _traduzir_autor(self, valor):
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

    def _traduzir_protegido(self, valor):
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

    def _traduzir_dimensoes(self, valor):
        binary_patterns = ["binário:", "binary:", "binario:", "fichier binaire:", "binario:", "binär:"]
        for pattern in binary_patterns:
            if pattern in valor.lower():
                parts = valor.split(":", 1)
                if len(parts) == 2:
                    return f"{self.loc.get_text('binary_file')}: {parts[1].strip()}"

        unidades_mapeamento = {
            # Português
            "páginas": "pages",
            "páginas estimadas": "pages_estimated",
            "págs.": "pages",
            "págs. est.": "pages_estimated",
            "linhas": "lines",
            "linhas de código": "lines_code",
            "total de linhas": "total_lines",
            "palavras": "words",
            "colunas": "columns",
            "planilhas": "spreadsheets",
            "slides": "slides",
            "slides estimados": "slides_estimated",
            "descompactado": "unzipped",
            "descompactados": "unzipped",
            "e outros": "and_others",
            "arquivos": "files",
            "tabelas": "tables",
            "parágrafos": "paragraphs",
            "registros": "records",
            "registros estimados": "records_estimated",
            "bytes por registro": "bytes_per_record",
            "bytes": "bytes",
            "binário": "binary_file",
            "minutos": "minutes",
            "horas": "hours",
            "dias": "days",
            "tamanho": "size",

            # English
            "pages": "pages",
            "estimated pages": "pages_estimated",
            "est. pages": "pages_estimated",
            "lines": "lines",
            "lines of code": "lines_code",
            "total lines": "total_lines",
            "words": "words",
            "columns": "columns",
            "spreadsheets": "spreadsheets",
            "slides": "slides",
            "estimated slides": "slides_estimated",
            "unzipped": "unzipped",
            "and others": "and_others",
            "files": "files",
            "tables": "tables",
            "paragraphs": "paragraphs",
            "records": "records",
            "estimated records": "records_estimated",
            "bytes per record": "bytes_per_record",
            "bytes": "bytes",
            "binary": "binary_file",
            "minutes": "minutes",
            "hours": "hours",
            "days": "days",
            "size": "size",

            # Español
            "páginas": "pages",
            "páginas estimadas": "pages_estimated",
            "líneas": "lines",
            "líneas de código": "lines_code",
            "total de líneas": "total_lines",
            "palabras": "words",
            "columnas": "columns",
            "hojas de cálculo": "spreadsheets",
            "diapositivas": "slides",
            "diapositivas estimadas": "slides_estimated",
            "descomprimido": "unzipped",
            "descomprimidos": "unzipped",
            "y otros": "and_others",
            "archivos": "files",
            "tablas": "tables",
            "párrafos": "paragraphs",
            "registros": "records",
            "registros estimados": "records_estimated",
            "bytes por registro": "bytes_per_record",
            "bytes": "bytes",
            "binario": "binary_file",
            "minutos": "minutes",
            "horas": "hours",
            "días": "days",
            "tamaño": "size",

            # Français
            "pages": "pages",
            "pages estimées": "pages_estimated",
            "lignes": "lines",
            "lignes de code": "lines_code",
            "total des lignes": "total_lines",
            "mots": "words",
            "colonnes": "columns",
            "feuilles de calcul": "spreadsheets",
            "diapositives": "slides",
            "diapositives estimées": "slides_estimated",
            "décompressé": "unzipped",
            "décompressés": "unzipped",
            "et autres": "and_others",
            "fichiers": "files",
            "tables": "tables",
            "paragraphes": "paragraphs",
            "enregistrements": "records",
            "enregistrements estimés": "records_estimated",
            "octets par enregistrement": "bytes_per_record",
            "octets": "bytes",
            "fichier binaire": "binary_file",
            "minutes": "minutes",
            "heures": "hours",
            "jours": "days",
            "taille": "size",

            # Italiano
            "pagine": "pages",
            "pagine stimate": "pages_estimated",
            "righe": "lines",
            "righe di codice": "lines_code",
            "totale righe": "total_lines",
            "parole": "words",
            "colonne": "columns",
            "fogli di calcolo": "spreadsheets",
            "diapositive": "slides",
            "diapositive stimate": "slides_estimated",
            "decompresso": "unzipped",
            "decompressi": "unzipped",
            "e altri": "and_others",
            "file": "files",
            "tabelle": "tables",
            "paragrafi": "paragraphs",
            "record": "records",
            "record stimati": "records_estimated",
            "byte per record": "bytes_per_record",
            "byte": "bytes",
            "binario": "binary_file",
            "minuti": "minutes",
            "ore": "hours",
            "giorni": "days",
            "dimensioni": "size",

            # Alemão
            "seiten": "pages",
            "geschätzte seiten": "pages_estimated",
            "zeilen": "lines",
            "codezeilen": "lines_code",
            "gesamtzeilen": "total_lines",
            "wörter": "words",
            "spalten": "columns",
            "tabellenkalkulationen": "spreadsheets",
            "folien": "slides",
            "geschätzte folien": "slides_estimated",
            "entpackt": "unzipped",
            "und andere": "and_others",
            "dateien": "files",
            "tabellen": "tables",
            "absätze": "paragraphs",
            "datensätze": "records",
            "geschätzte datensätze": "records_estimated",
            "bytes pro datensatz": "bytes_per_record",
            "bytes": "bytes",
            "binär": "binary_file",
            "minuten": "minutes",
            "stunden": "hours",
            "tage": "days",
            "größe": "size"
        }

        arquivo_compactado_pattern = r'(\d+)\s+(files|arquivos|archivos|fichiers|file|dateien),\s+(.*?)\s+(unzipped|descompactados|descomprimidos|décompressés|decompressi|entpackt)'
        match = re.search(arquivo_compactado_pattern, valor, re.IGNORECASE)

        if match:
            num_arquivos = match.group(1)
            tamanho = match.group(3)
            return f"{num_arquivos} {self.loc.get_text('files')}, {tamanho} {self.loc.get_text('unzipped')}"

        pattern = r'(\d+|~\d+)\s+([a-zA-ZáàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\s.]+?)(?=,|\s+\d|\s*$)'
        matches = re.findall(pattern, valor)

        if matches:
            texto_traduzido = valor

            for numero, unidade in reversed(matches):
                unidade_trim = unidade.strip()
                unidade_traduzida = unidade_trim

                for texto, chave in unidades_mapeamento.items():
                    if texto.lower() == unidade_trim.lower():
                        unidade_traduzida = self.loc.get_text(chave)
                        break

                padrao_original = f"{numero} {unidade_trim}"
                substituicao = f"{numero} {unidade_traduzida}"
                texto_traduzido = texto_traduzido.replace(padrao_original, substituicao)

            return texto_traduzido

        return valor
