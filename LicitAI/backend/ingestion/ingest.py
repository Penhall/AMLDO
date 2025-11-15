
"""Módulo de ingestão de normas e editais."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def _read_pdf(path: Path) -> str:
    try:
        import PyPDF2  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "A leitura de PDF requer a biblioteca PyPDF2.\n"
            "Instale com: pip install PyPDF2"
        ) from exc

    text_parts = []
    with path.open("rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    return "\n".join(text_parts)


def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_norma_file(input_path: str) -> str:
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        raw_text = _read_pdf(path)
    elif suffix in {".txt", ".md"}:
        raw_text = _read_txt(path)
    else:
        raise ValueError(
            f"Formato de arquivo não suportado para ingestão: {suffix}. "
            "Use .pdf ou .txt."
        )

    normalized = "\n".join(line.rstrip() for line in raw_text.splitlines())
    return normalized


def ingest_norma(
    input_path: str,
    output_dir: str = "data/normas_raw",
    output_name: Optional[str] = None,
) -> str:
    os.makedirs(output_dir, exist_ok=True)

    text = read_norma_file(input_path)
    in_path = Path(input_path)

    if output_name is None:
        output_name = in_path.stem

    out_path = Path(output_dir) / f"{output_name}.txt"
    out_path.write_text(text, encoding="utf-8")

    return str(out_path)
