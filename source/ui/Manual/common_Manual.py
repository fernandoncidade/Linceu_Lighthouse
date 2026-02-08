from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente

try:
    _DATA_DIR = obter_caminho_persistente() or ""

except Exception:
    _DATA_DIR = ""


@dataclass(frozen=True)
class ManualDetails:
    summary: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManualSection:
    id: str
    title: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()
    details: tuple[ManualDetails, ...] = ()


@dataclass(frozen=True)
class ManualBlock:
    kind: str
    text: str = ""
    section_id: str | None = None


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
