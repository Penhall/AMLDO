"""
Módulo de ingestão de normas e editais.

Lê documentos PDF/TXT e normaliza o texto para processamento posterior.
Refatorado do LicitAI POC com melhorias em type hints e error handling.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from amldo.core.exceptions import IngestionError


def _read_pdf(path: Path) -> str:
    """
    Lê um arquivo PDF e extrai todo o texto.

    Args:
        path: Caminho para o arquivo PDF

    Returns:
        Texto extraído de todas as páginas

    Raises:
        IngestionError: Se falhar ao ler o PDF
    """
    try:
        import PyPDF2  # type: ignore
    except ImportError as exc:
        raise IngestionError(
            "A leitura de PDF requer a biblioteca PyPDF2.\n"
            "Instale com: pip install PyPDF2"
        ) from exc

    try:
        text_parts = []
        with path.open("rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)

        return "\n".join(text_parts)
    except Exception as e:
        raise IngestionError(f"Falha ao ler PDF {path}: {e}") from e


def _read_txt(path: Path) -> str:
    """
    Lê um arquivo de texto.

    Args:
        path: Caminho para o arquivo TXT

    Returns:
        Conteúdo do arquivo

    Raises:
        IngestionError: Se falhar ao ler o arquivo
    """
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        raise IngestionError(f"Falha ao ler TXT {path}: {e}") from e


def read_norma_file(input_path: str) -> str:
    """
    Lê um arquivo de norma (PDF ou TXT) e retorna o texto normalizado.

    Args:
        input_path: Caminho para o arquivo

    Returns:
        Texto normalizado (sem espaços à direita nas linhas)

    Raises:
        FileNotFoundError: Se arquivo não existir
        IngestionError: Se formato não for suportado ou falhar na leitura
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        raw_text = _read_pdf(path)
    elif suffix in {".txt", ".md"}:
        raw_text = _read_txt(path)
    else:
        raise IngestionError(
            f"Formato de arquivo não suportado para ingestão: {suffix}. "
            "Use .pdf ou .txt."
        )

    # Normalização: remove espaços à direita de cada linha
    normalized = "\n".join(line.rstrip() for line in raw_text.splitlines())
    return normalized


def ingest_norma(
    input_path: str,
    output_dir: str = "data/normas_raw",
    output_name: Optional[str] = None,
) -> str:
    """
    Ingere um arquivo de norma e salva o texto normalizado.

    Args:
        input_path: Caminho para o arquivo de entrada (PDF ou TXT)
        output_dir: Diretório de saída (criado se não existir)
        output_name: Nome do arquivo de saída (sem extensão). Usa nome do input se None.

    Returns:
        Caminho do arquivo TXT de saída

    Raises:
        FileNotFoundError: Se arquivo de entrada não existir
        IngestionError: Se falhar na ingestão
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        text = read_norma_file(input_path)
        in_path = Path(input_path)

        if output_name is None:
            output_name = in_path.stem

        out_path = Path(output_dir) / f"{output_name}.txt"
        out_path.write_text(text, encoding="utf-8")

        return str(out_path)
    except FileNotFoundError:
        raise
    except IngestionError:
        raise
    except Exception as e:
        raise IngestionError(f"Falha ao ingerir norma de {input_path}: {e}") from e
