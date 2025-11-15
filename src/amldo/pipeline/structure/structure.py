"""
Módulo de estruturação e consolidação de artigos das normas.

Extrai artigos de normas usando regex e salva em formato JSONL.
Refatorado do LicitAI POC com melhorias em type hints e error handling.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

from amldo.core.exceptions import StructureError


# Regex para identificar início de artigos
ARTIGO_PATTERN = re.compile(
    r"""(?P<label>Art\.\s*\d+[^\n]*)""",
    flags=re.IGNORECASE,
)


def load_raw_text(path: str) -> str:
    """
    Carrega texto bruto de um arquivo.

    Args:
        path: Caminho para o arquivo TXT

    Returns:
        Conteúdo do arquivo

    Raises:
        FileNotFoundError: Se arquivo não existir
        StructureError: Se falhar ao ler o arquivo
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de texto não encontrado: {p}")

    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        raise StructureError(f"Falha ao carregar texto de {path}: {e}") from e


def split_in_artigos(raw_text: str) -> List[Dict]:
    """
    Divide texto bruto em artigos usando regex.

    Args:
        raw_text: Texto completo da norma

    Returns:
        Lista de dicionários, cada um com:
            - id: Identificador do artigo (Art-0, Art-1, ...)
            - label: Label do artigo (ex: "Art. 15. Das licitações")
            - text: Texto completo do artigo

    Raises:
        StructureError: Se falhar ao processar o texto
    """
    try:
        linhas = raw_text.splitlines()

        artigos: List[Dict] = []
        current_label = None
        current_lines: List[str] = []

        def flush(current_label, current_lines, idx: int):
            """Salva artigo atual e limpa buffer."""
            if current_label is None:
                return
            artigo_id = f"Art-{idx}"
            artigos.append(
                {
                    "id": artigo_id,
                    "label": current_label.strip(),
                    "text": "\n".join(current_lines).strip(),
                }
            )

        idx = 0
        for line in linhas:
            # Verifica se linha é início de novo artigo
            if ARTIGO_PATTERN.search(line):
                flush(current_label, current_lines, idx)
                idx += 1
                current_label = line
                current_lines = []
            else:
                current_lines.append(line)

        # Flush do último artigo
        flush(current_label, current_lines, idx)

        return artigos
    except Exception as e:
        raise StructureError(f"Falha ao dividir texto em artigos: {e}") from e


def save_artigos_to_jsonl(artigos: List[Dict], output_path: str) -> str:
    """
    Salva artigos em formato JSONL (um JSON por linha).

    Args:
        artigos: Lista de artigos (dicts)
        output_path: Caminho do arquivo JSONL de saída

    Returns:
        Caminho do arquivo salvo

    Raises:
        StructureError: Se falhar ao salvar o arquivo
    """
    try:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)

        with p.open("w", encoding="utf-8") as f:
            for artigo in artigos:
                f.write(json.dumps(artigo, ensure_ascii=False) + "\n")

        return str(p)
    except Exception as e:
        raise StructureError(f"Falha ao salvar artigos em {output_path}: {e}") from e


def estrutura_norma(
    raw_txt_path: str,
    output_jsonl_path: str = "data/normas_structured/artigos.jsonl",
) -> str:
    """
    Pipeline completo de estruturação: carrega texto → divide em artigos → salva JSONL.

    Args:
        raw_txt_path: Caminho do arquivo TXT bruto
        output_jsonl_path: Caminho do arquivo JSONL de saída

    Returns:
        Caminho do arquivo JSONL gerado

    Raises:
        FileNotFoundError: Se arquivo de entrada não existir
        StructureError: Se falhar em qualquer etapa do processamento
    """
    raw_text = load_raw_text(raw_txt_path)
    artigos = split_in_artigos(raw_text)
    return save_artigos_to_jsonl(artigos, output_jsonl_path)
