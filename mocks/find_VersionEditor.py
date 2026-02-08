import sys
import re
from pathlib import Path

# garante que a raiz do projeto esteja no sys.path quando o script for executado diretamente
# (resolve o erro "ModuleNotFoundError: No module named 'source'")
_project_root = Path(__file__).resolve().parent.parent
_project_root_str = str(_project_root)
if _project_root_str not in sys.path:
    sys.path.insert(0, _project_root_str)

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                               QSpinBox, QComboBox, QPushButton, QTextEdit, QGroupBox, QFileDialog)
from PySide6.QtGui import QIcon
from source.utils.IconUtils import get_icon_path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

BASE_DIR = Path(__file__).resolve().parent.parent  # usar a raiz do projeto (um nível acima de tools)

FILES_REL = {
    "privacy_pt": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_pt_BR.txt",
    "privacy_en": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_en_US.txt",
    "privacy_es": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_es_ES.txt",
    "privacy_fr": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_fr_FR.txt",
    "privacy_it": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_it_IT.txt",
    "privacy_de": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_de_DE.txt",
    "eula_pt": Path("source") / "assets" / "EULA" / "EULA_pt_BR - Linceu Lighthouse.txt",
    "eula_en": Path("source") / "assets" / "EULA" / "EULA_en_US - Linceu Lighthouse.txt",
    "eula_es": Path("source") / "assets" / "EULA" / "EULA_es_ES - Linceu Lighthouse.txt",
    "eula_fr": Path("source") / "assets" / "EULA" / "EULA_fr_FR - Linceu Lighthouse.txt",
    "eula_it": Path("source") / "assets" / "EULA" / "EULA_it_IT - Linceu Lighthouse.txt",
    "eula_de": Path("source") / "assets" / "EULA" / "EULA_de_DE - Linceu Lighthouse.txt",
    "clc_pt": Path("source") / "assets" / "CLC" / "CLC_pt_BR - Linceu Lighthouse.txt",
    "clc_en": Path("source") / "assets" / "CLC" / "CLC_en_US - Linceu Lighthouse.txt",
    "clc_es": Path("source") / "assets" / "CLC" / "CLC_es_ES - Linceu Lighthouse.txt",
    "clc_fr": Path("source") / "assets" / "CLC" / "CLC_fr_FR - Linceu Lighthouse.txt",
    "clc_it": Path("source") / "assets" / "CLC" / "CLC_it_IT - Linceu Lighthouse.txt",
    "clc_de": Path("source") / "assets" / "CLC" / "CLC_de_DE - Linceu Lighthouse.txt",
    "about_pt": Path("source") / "assets" / "ABOUT" / "ABOUT_pt_BR.txt",
    "about_en": Path("source") / "assets" / "ABOUT" / "ABOUT_en_US.txt",
    "about_es": Path("source") / "assets" / "ABOUT" / "ABOUT_es_ES.txt",
    "about_fr": Path("source") / "assets" / "ABOUT" / "ABOUT_fr_FR.txt",
    "about_it": Path("source") / "assets" / "ABOUT" / "ABOUT_it_IT.txt",
    "about_de": Path("source") / "assets" / "ABOUT" / "ABOUT_de_DE.txt",
}

def get_files_for_base(base_dir: Path = BASE_DIR):
    files = {}
    base_dir = Path(base_dir)
    for key, rel_path in FILES_REL.items():
        candidate = base_dir / rel_path

        if candidate.exists():
            files[key] = candidate.resolve()
            continue

        rel_parts = rel_path.parts
        if rel_parts and rel_parts[0] == "source":
            alt = base_dir.joinpath(*rel_parts[1:])
            if alt.exists():
                files[key] = alt.resolve()
                continue

        files[key] = candidate.resolve()

    return files

EXPECTED = {
    "privacy_pt": [
        "Última atualização: 26 de novembro de 2025",
        "Versão: 2025.11.26.0",
    ],
    "privacy_en": [
        "Last updated: November 26, 2025",
        "Version: 2025.11.26.0",
    ],
    "eula_pt": [
        "Versão 2025.11.26.0, 26 de novembro de 2025",
    ],
    "eula_en": [
        "Version 2025.11.26.0, November 26, 2025",
    ],
    "clc_pt": [
        "Versão: 2025.11.26.0",
        "Data: 26 de novembro de 2025",
    ],
    "clc_en": [
        "Version: 2025.11.26.0",
        "Date: November 26, 2025",
    ],
    "about_pt": [
        "Versão: 2025.11.26.0",
    ],
    "about_en": [
        "Version: 2025.11.26.0",
    ],
}

PT_MONTHS = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
PT_MONTHS_LOWER = [m.lower() for m in PT_MONTHS]
EN_MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
ES_MONTHS = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
FR_MONTHS = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
IT_MONTHS = ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]
DE_MONTHS = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]

def read_file(path: Path):
    try:
        # tenta várias decodificações para evitar problemas com BOM/encodings diferentes
        try:
            return path.read_text(encoding="utf-8")

        except Exception:
            try:
                return path.read_text(encoding="utf-8-sig")

            except Exception:
                return path.read_text(encoding="latin-1")

    except Exception:
        return None

# padrões para extrair o que realmente está nos arquivos (não comparar com EXPECTED)
PATTERNS = {
    "privacy_pt": [
        r'^(Versão:?\s*.*)$',
        r'^(Última atualização:?\s*.*)$'
    ],
    "privacy_en": [
        r'^(Version:?\s*.*)$',
        r'^(Last updated:?\s*.*)$'
    ],
    "privacy_es": [
        r'^(Versión:?\s*.*)$',
        r'^(Última actualización:?\s*.*)$'
    ],
    "privacy_fr": [
        r'^(Version:?\s*.*)$',
        r'^(Dernière mise à jour\s*:?\s*.*)$'
    ],
    "privacy_it": [
        r'^(Versione:?\s*.*)$',
        r'^(Ultimo aggiornamento:?\s*.*)$'
    ],
    "privacy_de": [
        r'^(Version:?\s*.*)$',
        r'^(Letzte Aktualisierung:?\s*.*)$'
    ],
    "eula_pt": [
        r'^(Versão.*)$'
    ],
    "eula_en": [
        r'^(Version.*)$'
    ],
    "eula_es": [
        r'^(Versión.*)$'
    ],
    "eula_fr": [
        r'^(Version.*)$'
    ],
    "eula_it": [
        r'^(Versione.*)$'
    ],
    "eula_de": [
        r'^(Version.*)$'
    ],
    "clc_pt": [
        r'^(Versão.*)$'
    ],
    "clc_en": [
        r'^(Version.*)$'
    ],
    "clc_es": [
        r'^(Versión.*)$'
    ],
    "clc_fr": [
        r'^(Version.*)$'
    ],
    "clc_it": [
        r'^(Versione.*)$'
    ],
    "clc_de": [
        r'^(Version.*)$'
    ],
    "about_pt": [
        r'^(Versão:?\s*.*)$'
    ],
    "about_en": [
        r'^(Version:?\s*.*)$'
    ],
    "about_es": [
        r'^(Versión:?\s*.*)$'
    ],
    "about_fr": [
        r'^(Version:?\s*.*)$'
    ],
    "about_it": [
        r'^(Versione:?\s*.*)$'
    ],
    "about_de": [
        r'^(Version:?\s*.*)$'
    ],
}

def check_expected_lines(base_dir: Path = BASE_DIR):
    status = {}
    files = get_files_for_base(base_dir)
    for key, path in files.items():
        txt = read_file(path)
        if txt is None:
            status[key] = {"exists": False, "found": [], "missing": []}
            continue

        found = []
        missing = []

        # para cada padrão associado àquele arquivo, procurar a linha correspondente
        patterns = PATTERNS.get(key, [])
        for pat in patterns:
            m = re.search(pat, txt, flags=re.MULTILINE)
            if m:
                found.append(m.group(1).strip())

            else:
                missing.append(pat)

        # se não houver padrões definidos, devolve as 3 primeiras linhas do arquivo como fallback
        if not patterns:
            lines = [l.rstrip("\r\n") for l in txt.splitlines()]
            found = lines[:3] if lines else []
            missing = []

        status[key] = {"exists": True, "found": found, "missing": missing}

    return status

def replace_file_content(path: Path, new_text: str):
    try:
        path.write_text(new_text, encoding="utf-8")
        return True, ""

    except Exception as e:
        return False, str(e)

def apply_updates(pt_version, pt_day, pt_month_index, pt_year,
                  en_version, en_day, en_month_index, en_year,
                  es_version, es_day, es_month_index, es_year,
                  fr_version, fr_day, fr_month_index, fr_year,
                  it_version, it_day, it_month_index, it_year,
                  de_version, de_day, de_month_index, de_year,
                  base_dir: Path = BASE_DIR):
    results = []
    files = get_files_for_base(base_dir)
    pt_month_name = PT_MONTHS_LOWER[pt_month_index]
    pt_date = f"{pt_day} de {pt_month_name} de {pt_year}"
    en_month_name = EN_MONTHS[en_month_index]
    en_date = f"{en_month_name} {en_day}, {en_year}"

    PRIVACY_MAP = {
        "privacy_es": ("Versión", ES_MONTHS, True, False, (es_version, es_day, es_month_index, es_year)),
        "privacy_fr": ("Version", FR_MONTHS, False, False, (fr_version, fr_day, fr_month_index, fr_year)),
        "privacy_it": ("Versione", IT_MONTHS, False, False, (it_version, it_day, it_month_index, it_year)),
        "privacy_de": ("Version", DE_MONTHS, False, True, (de_version, de_day, de_month_index, de_year)),
    }

    EULA_MAP = {
        "eula_es": ("Versión", ES_MONTHS, True, False, (es_version, es_day, es_month_index, es_year)),
        "eula_fr": ("Version", FR_MONTHS, False, False, (fr_version, fr_day, fr_month_index, fr_year)),
        "eula_it": ("Versione", IT_MONTHS, False, False, (it_version, it_day, it_month_index, it_year)),
        "eula_de": ("Version", DE_MONTHS, False, True, (de_version, de_day, de_month_index, de_year)),
    }

    CLC_MAP = {
        "clc_es": ("Versión", ES_MONTHS, True, False, (es_version, es_day, es_month_index, es_year)),
        "clc_fr": ("Version", FR_MONTHS, False, False, (fr_version, fr_day, fr_month_index, fr_year)),
        "clc_it": ("Versione", IT_MONTHS, False, False, (it_version, it_day, it_month_index, it_year)),
        "clc_de": ("Version", DE_MONTHS, False, True, (de_version, de_day, de_month_index, de_year)),
    }

    ABOUT_INPUTS = {
        "about_es": (es_version, es_day, es_month_index, es_year),
        "about_fr": (fr_version, fr_day, fr_month_index, fr_year),
        "about_it": (it_version, it_day, it_month_index, it_year),
        "about_de": (de_version, de_day, de_month_index, de_year),
    }

    for key, path in files.items():
        txt = read_file(path)
        if txt is None:
            results.append((key, False, "arquivo inexistente"))
            continue

        original = txt
        new_txt = txt

        try:
            if key == "privacy_pt":
                new_txt = re.sub(r'^(Versão:?\s*).*$', lambda m: m.group(1) + pt_version, new_txt, flags=re.MULTILINE)
                new_txt = re.sub(r'^(Última atualização:?\s*).*$', lambda m: m.group(1) + pt_date, new_txt, flags=re.MULTILINE)

            elif key == "privacy_en":
                new_txt = re.sub(r'^(Version:?\s*).*$', lambda m: m.group(1) + en_version, new_txt, flags=re.MULTILINE)
                new_txt = re.sub(r'^(Last updated:?\s*).*$', lambda m: m.group(1) + en_date, new_txt, flags=re.MULTILINE)

            elif key in PRIVACY_MAP:
                ver_label, months_list, use_de, dot_after_day, inputs = PRIVACY_MAP[key]
                lang_version, lang_day, lang_month_index, lang_year = inputs
                month_name = months_list[lang_month_index]
                if use_de:
                    localized_date = f"{lang_day} de {month_name} de {lang_year}"

                else:
                    if lang_label := ver_label:
                        localized_date = f"{lang_day} {month_name} {lang_year}"

                ver_pattern = rf'^({re.escape(ver_label)}:?\s*).*$'
                new_txt = re.sub(ver_pattern, lambda m: m.group(1) + lang_version, new_txt, flags=re.MULTILINE)

                upd_label = "Última actualización" if key == "privacy_es" else ("Dernière mise à jour" if key == "privacy_fr" else ("Ultimo aggiornamento" if key == "privacy_it" else "Letzte Aktualisierung"))
                upd_pattern = rf'^({re.escape(upd_label)}\s*:?\s*).*$'
                new_txt = re.sub(upd_pattern, lambda m: m.group(1) + localized_date, new_txt, flags=re.MULTILINE)

            elif key == "eula_pt":
                new_txt = re.sub(r'^(Versão\s*)([\d\.]+)\s*,\s*.*$', f"Versão {pt_version}, {pt_date}", new_txt, flags=re.MULTILINE)

            elif key == "eula_en":
                new_txt = re.sub(r'^(Version\s*)([\d\.]+)\s*,\s*.*$', f"Version {en_version}, {en_date}", new_txt, flags=re.MULTILINE)

            elif key in EULA_MAP:
                label, months_list, use_de, dot_after_day, inputs = EULA_MAP[key]
                lang_version, lang_day, lang_month_index, lang_year = inputs
                month_name = months_list[lang_month_index]
                if use_de:
                    localized_date = f"{lang_day} de {month_name} de {lang_year}"

                else:
                    if dot_after_day:
                        localized_date = f"{lang_day}. {month_name} {lang_year}"

                    else:
                        localized_date = f"{lang_day} {month_name} {lang_year}"

                pattern = rf'^({re.escape(label)}\s*)([\d\.]+)\s*,\s*.*$'
                new_txt = re.sub(pattern, lambda m: f"{m.group(1)}{lang_version}, {localized_date}", new_txt, flags=re.MULTILINE)

            elif key == "clc_pt":
                new_txt = re.sub(r'^(Versão\s*)([\d\.]+)\s*,\s*.*$', f"Versão {pt_version}, {pt_date}", new_txt, flags=re.MULTILINE)

            elif key == "clc_en":
                new_txt = re.sub(r'^(Version\s*)([\d\.]+)\s*,\s*.*$', f"Version {en_version}, {en_date}", new_txt, flags=re.MULTILINE)

            elif key in CLC_MAP:
                label, months_list, use_de, dot_after_day, inputs = CLC_MAP[key]
                lang_version, lang_day, lang_month_index, lang_year = inputs
                month_name = months_list[lang_month_index]
                if use_de:
                    localized_date = f"{lang_day} de {month_name} de {lang_year}"

                else:
                    if dot_after_day:
                        localized_date = f"{lang_day}. {month_name} {lang_year}"

                    else:
                        localized_date = f"{lang_day} {month_name} {lang_year}"

                pattern = rf'^({re.escape(label)}\s*)([\d\.]+)\s*,\s*.*$'
                new_txt = re.sub(pattern, lambda m: f"{m.group(1)}{lang_version}, {localized_date}", new_txt, flags=re.MULTILINE)

            elif key == "about_pt":
                new_txt = re.sub(r'^(Versão:?\s*).*$', lambda m: m.group(1) + pt_version, new_txt, flags=re.MULTILINE)

            elif key == "about_en":
                new_txt = re.sub(r'^(Version:?\s*).*$', lambda m: m.group(1) + en_version, new_txt, flags=re.MULTILINE)

            elif key in ABOUT_INPUTS:
                ABOUT_LABELS = {
                    "about_es": "Versión",
                    "about_fr": "Version",
                    "about_it": "Versione",
                    "about_de": "Version",
                }
                label = ABOUT_LABELS.get(key, "Version")
                lang_version, lang_day, lang_month_index, lang_year = ABOUT_INPUTS[key]
                pattern = rf'^({re.escape(label)}:?\s*).*$'
                new_txt = re.sub(pattern, lambda m: m.group(1) + lang_version, new_txt, flags=re.MULTILINE)

            if new_txt != original:
                ok, err = replace_file_content(path, new_txt)
                if ok:
                    results.append((key, True, "atualizado"))

                else:
                    results.append((key, False, f"erro escrita: {err}"))

            else:
                results.append((key, False, "padrões não encontrados / sem alteração"))

        except Exception as e:
            results.append((key, False, f"erro: {e}"))

    return results


class VersionEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Versões / Datas - Lúmen (PT/EN)")
        self.resize(820, 520)

        try:
            icon_path = get_icon_path("autismo.ico")
            if icon_path:
                self.setWindowIcon(QIcon(icon_path))

        except Exception as e:
            logger.error(f"Erro ao carregar ícone da aplicação: {e}", exc_info=True)

        layout = QVBoxLayout(self)

        # pasta base selecionada (por padrão raiz do projeto)
        self.selected_base_dir = BASE_DIR

        # pasta de arquivos: seleção pelo usuário
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Pasta dos arquivos:"))
        self.folder_path = QLineEdit(str(self.selected_base_dir))
        self.folder_path.setReadOnly(True)
        folder_layout.addWidget(self.folder_path)
        self.select_folder_btn = QPushButton("Selecionar...")
        self.select_folder_btn.clicked.connect(self.on_select_folder)
        folder_layout.addWidget(self.select_folder_btn)
        layout.addLayout(folder_layout)

        # PT group
        pt_group = QGroupBox("Português (pt-BR)")
        pt_layout = QHBoxLayout()
        pt_group.setLayout(pt_layout)

        pt_layout.addWidget(QLabel("Versão:"))
        self.pt_version = QLineEdit("2025.11.26.0")
        pt_layout.addWidget(self.pt_version)

        pt_layout.addWidget(QLabel("Dia:"))
        self.pt_day = QSpinBox()
        self.pt_day.setRange(1, 31)
        self.pt_day.setValue(26)
        pt_layout.addWidget(self.pt_day)

        pt_layout.addWidget(QLabel("Mês:"))
        self.pt_month = QComboBox()
        self.pt_month.addItems(PT_MONTHS)
        self.pt_month.setCurrentIndex(10)  # Novembro
        pt_layout.addWidget(self.pt_month)

        pt_layout.addWidget(QLabel("Ano:"))
        self.pt_year = QSpinBox()
        self.pt_year.setRange(1900, 3000)
        self.pt_year.setValue(2025)
        pt_layout.addWidget(self.pt_year)

        layout.addWidget(pt_group)

        # EN group
        en_group = QGroupBox("English (en-US)")
        en_layout = QHBoxLayout()
        en_group.setLayout(en_layout)

        en_layout.addWidget(QLabel("Version:"))
        self.en_version = QLineEdit("2025.11.26.0")
        en_layout.addWidget(self.en_version)

        en_layout.addWidget(QLabel("Day:"))
        self.en_day = QSpinBox()
        self.en_day.setRange(1, 31)
        self.en_day.setValue(26)
        en_layout.addWidget(self.en_day)

        en_layout.addWidget(QLabel("Month:"))
        self.en_month = QComboBox()
        self.en_month.addItems(EN_MONTHS)
        self.en_month.setCurrentIndex(10)  # November
        en_layout.addWidget(self.en_month)

        en_layout.addWidget(QLabel("Year:"))
        self.en_year = QSpinBox()
        self.en_year.setRange(1900, 3000)
        self.en_year.setValue(2025)
        en_layout.addWidget(self.en_year)

        layout.addWidget(en_group)

        # ES group
        es_group = QGroupBox("Español (es-ES)")
        es_layout = QHBoxLayout()
        es_group.setLayout(es_layout)

        es_layout.addWidget(QLabel("Versión:"))
        self.es_version = QLineEdit("2025.11.26.0")
        es_layout.addWidget(self.es_version)

        es_layout.addWidget(QLabel("Día:"))
        self.es_day = QSpinBox()
        self.es_day.setRange(1, 31)
        self.es_day.setValue(26)
        es_layout.addWidget(self.es_day)

        es_layout.addWidget(QLabel("Mes:"))
        self.es_month = QComboBox()
        self.es_month.addItems(ES_MONTHS)
        self.es_month.setCurrentIndex(10)  # Noviembre
        es_layout.addWidget(self.es_month)

        es_layout.addWidget(QLabel("Año:"))
        self.es_year = QSpinBox()
        self.es_year.setRange(1900, 3000)
        self.es_year.setValue(2025)
        es_layout.addWidget(self.es_year)

        layout.addWidget(es_group)

        # FR group
        fr_group = QGroupBox("Français (fr-FR)")
        fr_layout = QHBoxLayout()
        fr_group.setLayout(fr_layout)

        fr_layout.addWidget(QLabel("Version:"))
        self.fr_version = QLineEdit("2025.11.26.0")
        fr_layout.addWidget(self.fr_version)

        fr_layout.addWidget(QLabel("Jour:"))
        self.fr_day = QSpinBox()
        self.fr_day.setRange(1, 31)
        self.fr_day.setValue(26)
        fr_layout.addWidget(self.fr_day)

        fr_layout.addWidget(QLabel("Mois:"))
        self.fr_month = QComboBox()
        self.fr_month.addItems(FR_MONTHS)
        self.fr_month.setCurrentIndex(10)  # Novembre
        fr_layout.addWidget(self.fr_month)

        fr_layout.addWidget(QLabel("Année:"))
        self.fr_year = QSpinBox()
        self.fr_year.setRange(1900, 3000)
        self.fr_year.setValue(2025)
        fr_layout.addWidget(self.fr_year)

        layout.addWidget(fr_group)

        # IT group
        it_group = QGroupBox("Italiano (it-IT)")
        it_layout = QHBoxLayout()
        it_group.setLayout(it_layout)

        it_layout.addWidget(QLabel("Versione:"))
        self.it_version = QLineEdit("2025.11.26.0")
        it_layout.addWidget(self.it_version)

        it_layout.addWidget(QLabel("Giorno:"))
        self.it_day = QSpinBox()
        self.it_day.setRange(1, 31)
        self.it_day.setValue(26)
        it_layout.addWidget(self.it_day)

        it_layout.addWidget(QLabel("Mese:"))
        self.it_month = QComboBox()
        self.it_month.addItems(IT_MONTHS)
        self.it_month.setCurrentIndex(10)  # Novembre
        it_layout.addWidget(self.it_month)

        it_layout.addWidget(QLabel("Anno:"))
        self.it_year = QSpinBox()
        self.it_year.setRange(1900, 3000)
        self.it_year.setValue(2025)
        it_layout.addWidget(self.it_year)

        layout.addWidget(it_group)

        # DE group
        de_group = QGroupBox("Deutsch (de-DE)")
        de_layout = QHBoxLayout()
        de_group.setLayout(de_layout)

        de_layout.addWidget(QLabel("Version:"))
        self.de_version = QLineEdit("2025.11.26.0")
        de_layout.addWidget(self.de_version)

        de_layout.addWidget(QLabel("Tag:"))
        self.de_day = QSpinBox()
        self.de_day.setRange(1, 31)
        self.de_day.setValue(26)
        de_layout.addWidget(self.de_day)

        de_layout.addWidget(QLabel("Monat:"))
        self.de_month = QComboBox()
        self.de_month.addItems(DE_MONTHS)
        self.de_month.setCurrentIndex(10)  # November
        de_layout.addWidget(self.de_month)

        de_layout.addWidget(QLabel("Jahr:"))
        self.de_year = QSpinBox()
        self.de_year.setRange(1900, 3000)
        self.de_year.setValue(2025)
        de_layout.addWidget(self.de_year)

        layout.addWidget(de_group)

        # Buttons and status
        btn_layout = QHBoxLayout()
        self.check_btn = QPushButton("🔍 Verificar arquivos")
        self.check_btn.clicked.connect(self.on_check)
        btn_layout.addWidget(self.check_btn)

        self.save_btn = QPushButton("💾 Salvar alterações")
        self.save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(self.save_btn)

        self.refresh_btn = QPushButton("🔄 Recarregar verificação")
        self.refresh_btn.clicked.connect(self.on_check)
        btn_layout.addWidget(self.refresh_btn)

        layout.addLayout(btn_layout)

        self.status = QTextEdit()
        self.status.setReadOnly(True)
        layout.addWidget(self.status)

        self.on_check()

    def on_select_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Selecione a pasta onde os arquivos estão", str(self.selected_base_dir))
        if dir_path:
            self.selected_base_dir = Path(dir_path)
            self.folder_path.setText(str(self.selected_base_dir))
            self.on_check()

    def on_check(self):
        # passa a pasta selecionada para a verificação
        status = check_expected_lines(self.selected_base_dir)
        lines = [f"Base: {self.selected_base_dir}"]
        for key, info in status.items():
            lines.append(f"{key}: file {'exists' if info['exists'] else 'missing'}")
            if info['exists']:
                if info["found"]:
                    lines.append("  found:")
                    for f in info["found"]:
                        lines.append(f"    - {f}")

                if info["missing"]:
                    lines.append("  missing:")
                    for m in info["missing"]:
                        lines.append(f"    - {m}")

            lines.append("")

        self.status.setPlainText("\n".join(lines))

    def on_save(self):
        pt_version = self.pt_version.text().strip()
        pt_day = self.pt_day.value()
        pt_month_index = self.pt_month.currentIndex()
        pt_year = self.pt_year.value()

        en_version = self.en_version.text().strip()
        en_day = self.en_day.value()
        en_month_index = self.en_month.currentIndex()
        en_year = self.en_year.value()

        es_version = self.es_version.text().strip()
        es_day = self.es_day.value()
        es_month_index = self.es_month.currentIndex()
        es_year = self.es_year.value()

        fr_version = self.fr_version.text().strip()
        fr_day = self.fr_day.value()
        fr_month_index = self.fr_month.currentIndex()
        fr_year = self.fr_year.value()

        it_version = self.it_version.text().strip()
        it_day = self.it_day.value()
        it_month_index = self.it_month.currentIndex()
        it_year = self.it_year.value()

        de_version = self.de_version.text().strip()
        de_day = self.de_day.value()
        de_month_index = self.de_month.currentIndex()
        de_year = self.de_year.value()

        # passa a pasta selecionada para a atualização
        results = apply_updates(
            pt_version, pt_day, pt_month_index, pt_year,
            en_version, en_day, en_month_index, en_year,
            es_version, es_day, es_month_index, es_year,
            fr_version, fr_day, fr_month_index, fr_year,
            it_version, it_day, it_month_index, it_year,
            de_version, de_day, de_month_index, de_year,
            base_dir=self.selected_base_dir
        )
        lines = ["Resultados:"]
        for key, ok, msg in results:
            lines.append(f"{key}: {'OK' if ok else 'FAIL'} - {msg}")

        self.status.setPlainText("\n".join(lines))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VersionEditor()
    w.show()
    sys.exit(app.exec())
