from __future__ import annotations
from typing import Dict, Tuple
from source.ui.Manual.common_Manual import ManualSection, ManualBlock

def normalize_language(lang: str | None) -> str:
	if not lang:
		return "pt_BR"

	v = lang.strip().replace("-", "_").lower()
	if v in ("pt_br", "pt"):
		return "pt_BR"

	if v in ("en_us", "en"):
		return "en_US"

	if v in ("es_es", "es"):
		return "es_ES"

	if v in ("fr_fr", "fr"):
		return "fr_FR"

	if v in ("it_it", "it"):
		return "it_IT"

	if v in ("de_de", "de"):
		return "de_DE"

	return "pt_BR"

def get_manual_title(lang: str | None = None) -> str:
	lang = normalize_language(lang)
	if lang == "pt_BR":
		return "Manual de Utilização — Linceu Lighthouse"

	if lang == "en_US":
		return "User Manual — Linceu Lighthouse"

	if lang == "es_ES":
		return "Manual de Uso — Linceu Lighthouse"

	if lang == "fr_FR":
		return "Manuel d'utilisation — Linceu Lighthouse"

	if lang == "it_IT":
		return "Manuale utente — Linceu Lighthouse"

	if lang == "de_DE":
		return "Benutzerhandbuch — Linceu Lighthouse"

	return "User Manual — Linceu Lighthouse"

def to_unicode_bold(s: str) -> str:
    out: list[str] = []
    for ch in s:
        if "A" <= ch <= "Z":
            out.append(chr(ord(ch) - ord("A") + 0x1D400))

        elif "a" <= ch <= "z":
            out.append(chr(ord(ch) - ord("a") + 0x1D41A))

        elif "0" <= ch <= "9":
            out.append(chr(ord(ch) - ord("0") + 0x1D7CE))

        else:
            out.append(ch)

    return "".join(out)

def get_manual_document(lang: str | None = None) -> tuple[ManualSection, ...]:
	lang = normalize_language(lang)
	if lang == "en_US":
		return _DOC_EN_US

	if lang == "es_ES":
		return _DOC_ES_ES

	if lang == "fr_FR":
		return _DOC_FR_FR

	if lang == "it_IT":
		return _DOC_IT_IT

	if lang == "de_DE":
		return _DOC_DE_DE

	return _DOC_PT_BR

def get_manual_blocks(lang: str | None = None) -> tuple[tuple[ManualBlock, ...], Tuple[str, ...]]:
	lang = normalize_language(lang)
	sections = get_manual_document(lang)

	blocks: list[ManualBlock] = []
	order: list[str] = []

	def blank() -> None:
		blocks.append(ManualBlock(kind="blank"))

	def line(text: str) -> None:
		blocks.append(ManualBlock(kind="line", text=text))

	def toc_title(text: str) -> None:
		blocks.append(ManualBlock(kind="toc_title", text=text))

	def toc_item(text: str, section_id: str) -> None:
		blocks.append(ManualBlock(kind="toc_item", text=text, section_id=section_id))

	def section_title(text: str, section_id: str) -> None:
		blocks.append(ManualBlock(kind="section_title", text=text, section_id=section_id))

	def detail_title(text: str) -> None:
		blocks.append(ManualBlock(kind="detail_title", text=text))

	def paragraph(text: str) -> None:
		blocks.append(ManualBlock(kind="paragraph", text=text))

	def bullet(text: str) -> None:
		blocks.append(ManualBlock(kind="bullet", text=text))

	def divider() -> None:
		blocks.append(ManualBlock(kind="divider", text="-" * 60))

	line(get_manual_title(lang))
	line("=" * len(get_manual_title(lang)))
	blank()

	if lang == "pt_BR":
		paragraph(
			"Este manual descreve como operar o aplicativo Linceu Lighthouse (modo de uso), cobrindo funcionalidades, atalhos, "
			"fluxo de trabalho sugerido, solução de problemas e informações sobre persistência de dados."
		)
		paragraph("Não é um guia de desenvolvimento.")
		blank()
		toc_title("Indice")
		
	elif lang == "en_US":
		paragraph(
			"This manual describes how to operate the Linceu Lighthouse application (user guide), covering features, shortcuts, "
			"suggested workflows, troubleshooting, and information about data persistence."
		)
		paragraph("It is not a development guide.")
		blank()
		toc_title("Table of Contents")

	elif lang == "es_ES":
		paragraph(
			"Este manual describe cómo operar la aplicación Linceu Lighthouse (guía del usuario), cubriendo funcionalidades, atajos, "
			"flujos de trabajo sugeridos, solución de problemas e información sobre la persistencia de datos."
		)
		paragraph("No es una guía de desarrollo.")
		blank()
		toc_title("Índice")

	elif lang == "fr_FR":
		paragraph(
			"Ce manuel décrit comment utiliser l'application Linceu Lighthouse (guide de l'utilisateur), couvrant les fonctionnalités, "
			"raccourcis, flux de travail suggérés, dépannage et informations sur la persistance des données."
		)
		paragraph("Ce n'est pas un guide de développement.")
		blank()
		toc_title("Table des matières")

	elif lang == "it_IT":
		paragraph(
			"Questo manuale descrive come utilizzare l'applicazione Linceu Lighthouse (guida utente), coprendo funzionalità, scorciatoie, "
			"flussi di lavoro suggeriti, risoluzione dei problemi e informazioni sulla persistenza dei dati."
		)
		paragraph("Non è una guida per sviluppatori.")
		blank()
		toc_title("Indice")

	elif lang == "de_DE":
		paragraph(
			"Dieses Handbuch beschreibt, wie die Anwendung Linceu Lighthouse verwendet wird (Benutzerhandbuch) und behandelt Funktionen, "
			"Tastenkürzel, empfohlene Arbeitsabläufe, Fehlerbehebung und Informationen zur Datenpersistenz."
		)
		paragraph("Es ist kein Entwicklerhandbuch.")
		blank()
		toc_title("Inhaltsverzeichnis")

	else:
		paragraph(
			"This manual describes how to operate the Linceu Lighthouse application (user guide), covering features, shortcuts, "
			"suggested workflows, troubleshooting, and information about data persistence."
		)
		paragraph("It is not a development guide.")
		blank()
		toc_title("Table of Contents")

	for idx, s in enumerate(sections, start=1):
		toc_item(f"{idx}. {s.title}", section_id=s.id)

	blank()
	divider()
	blank()

	for s in sections:
		order.append(s.id)

		section_title(s.title, section_id=s.id)
		blank()

		for p in s.paragraphs:
			paragraph(p)
			blank()

		for b in s.bullets:
			bullet(b)

		if s.bullets:
			blank()

		for d in s.details:
			detail_title(d.summary)
			blank()

			for p in d.paragraphs:
				paragraph(p)
				blank()

			for b in d.bullets:
				bullet(b)

			if d.bullets:
				blank()

		divider()
		blank()

	return tuple(blocks), tuple(order)

def get_manual_text(lang: str | None = None) -> str:
	text, _positions, _order = get_manual_text_with_positions(lang)
	return text

def get_manual_text_with_positions(lang: str | None = None,) -> tuple[str, Dict[str, int], Tuple[str, ...]]:
	lang = normalize_language(lang)
	sections = get_manual_document(lang)

	lines: list[str] = []
	positions: dict[str, int] = {}
	order: list[str] = []

	def add_line(s: str = "") -> None:
		lines.append(s)

	def current_offset() -> int:
		return sum(len(l) + 1 for l in lines)

	title = get_manual_title(lang)
	add_line(title)
	add_line("=" * len(title))
	add_line()

	if lang == "pt_BR":
		add_line(
			"Este manual descreve como operar o aplicativo Linceu Lighthouse (modo de uso), cobrindo funcionalidades, atalhos, "
			"fluxo de trabalho sugerido, solução de problemas e informações sobre persistência de dados."
		)
		add_line("Não é um guia de desenvolvimento.")
		add_line()
		add_line("Indice")
		add_line("----------")

	elif lang == "en_US":
		add_line(
			"This manual describes how to operate the Linceu Lighthouse application (user guide), covering features, shortcuts, "
			"suggested workflows, troubleshooting, and information about data persistence."
		)
		add_line("It is not a development guide.")
		add_line()
		add_line("Table of Contents")
		add_line("------------------------------")

	elif lang == "es_ES":
		add_line(
			"Este manual describe cómo operar la aplicación Linceu Lighthouse (guía del usuario), cubriendo funcionalidades, atajos, "
			"flujos de trabajo sugeridos, solución de problemas e información sobre la persistencia de datos."
		)
		add_line("No es una guía de desarrollo.")
		add_line()
		add_line("Índice")
		add_line("----------")

	elif lang == "fr_FR":
		add_line(
			"Ce manuel décrit comment utiliser l'application Linceu Lighthouse (guide de l'utilisateur), couvrant les fonctionnalités, "
			"raccourcis, flux de travail suggérés, dépannage et informations sur la persistance des données."
		)
		add_line("Ce n'est pas un guide de développement.")
		add_line()
		add_line("Table des matières")
		add_line("------------------------------")

	elif lang == "it_IT":
		add_line(
			"Questo manuale descrive come utilizzare l'applicazione Linceu Lighthouse (guida utente), coprendo funzionalità, scorciatoie, "
			"flussi di lavoro suggeriti, risoluzione dei problemi e informazioni sulla persistenza dei dati."
		)
		add_line("Non è una guida per sviluppatori.")
		add_line()
		add_line("Indice")
		add_line("----------")

	elif lang == "de_DE":
		add_line(
			"Dieses Handbuch beschreibt, wie die Anwendung Linceu Lighthouse verwendet wird (Benutzerhandbuch) und behandelt Funktionen, "
			"Tastenkürzel, empfohlene Arbeitsabläufe, Fehlerbehebung und Informationen zur Datenpersistenz."
		)
		add_line("Es ist kein Entwicklerhandbuch.")
		add_line()
		add_line("Inhaltsverzeichnis")
		add_line("------------------------------")

	else:
		add_line(
			"This manual describes how to operate the Linceu Lighthouse application (user guide), covering features, shortcuts, "
			"suggested workflows, troubleshooting, and information about data persistence."
		)
		add_line("It is not a development guide.")
		add_line()
		add_line("Table of Contents")
		add_line("------------------------------")

	for idx, s in enumerate(sections, start=1):
		add_line(f"{idx}. {s.title}")

	add_line()
	add_line("-" * 60)
	add_line()

	for s in sections:
		positions[s.id] = current_offset()
		order.append(s.id)

		add_line(s.title)
		add_line("-" * len(s.title))
		add_line()

		for p in s.paragraphs:
			add_line(p)
			add_line()

		for b in s.bullets:
			add_line(f"- {b}")

		if s.bullets:
			add_line()

		for d in s.details:
			add_line(d.summary)
			add_line("." * len(d.summary))
			add_line()

			for p in d.paragraphs:
				add_line(p)
				add_line()

			for b in d.bullets:
				add_line(f"- {b}")

			if d.bullets:
				add_line()

		add_line("-" * 60)
		add_line()

	return "\n".join(lines), positions, tuple(order)

try:
	from source.ui.Manual import DOC_PT_BR as _mod_DOC_PT_BR

except Exception:
	_mod_DOC_PT_BR = None

try:
	from source.ui.Manual import DOC_EN_US as _mod_DOC_EN_US

except Exception:
	_mod_DOC_EN_US = None

try:
	from source.ui.Manual import DOC_ES_ES as _mod_DOC_ES_ES

except Exception:
	_mod_DOC_ES_ES = None

try:
	from source.ui.Manual import DOC_FR_FR as _mod_DOC_FR_FR

except Exception:
	_mod_DOC_FR_FR = None

try:
	from source.ui.Manual import DOC_IT_IT as _mod_DOC_IT_IT

except Exception:
	_mod_DOC_IT_IT = None

try:
	from source.ui.Manual import DOC_DE_DE as _mod_DOC_DE_DE

except Exception:
	_mod_DOC_DE_DE = None

def _extract_doc(obj, names):
	if not obj:
		return ()

	for n in names:
		if hasattr(obj, n):
			return getattr(obj, n)

	return ()

_DOC_PT_BR = _extract_doc(_mod_DOC_PT_BR, ("_DOC_PT_BR", "_DOC", "DOC"))
_DOC_EN_US = _extract_doc(_mod_DOC_EN_US, ("_DOC_EN_US", "_DOC", "DOC"))
_DOC_ES_ES = _extract_doc(_mod_DOC_ES_ES, ("_DOC_ES_ES", "_DOC", "DOC"))
_DOC_FR_FR = _extract_doc(_mod_DOC_FR_FR, ("_DOC_FR_FR", "_DOC", "DOC"))
_DOC_IT_IT = _extract_doc(_mod_DOC_IT_IT, ("_DOC_IT_IT", "_DOC", "DOC"))
_DOC_DE_DE = _extract_doc(_mod_DOC_DE_DE, ("_DOC_DE_DE", "_DOC", "DOC"))
