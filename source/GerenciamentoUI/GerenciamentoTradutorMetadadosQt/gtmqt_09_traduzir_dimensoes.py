import re
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _traduzir_dimensoes(self, valor):
    try:
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

    except Exception as e:
        logger.error(f"Erro ao traduzir dimensões: {e}", exc_info=True)
        return valor
