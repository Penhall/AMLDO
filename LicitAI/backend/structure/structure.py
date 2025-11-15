
\"\"\"Módulo de estruturação e consolidação de artigos das normas.\"\"\"

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


ARTIGO_PATTERN = re.compile(
    r\"\"\"(?P<label>Art\\.\\s*\\d+[^\\n]*)\"\"\",
    flags=re.IGNORECASE,
)


def load_raw_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de texto não encontrado: {p}")
    return p.read_text(encoding="utf-8", errors="ignore")


def split_in_artigos(raw_text: str) -> List[Dict]:
    linhas = raw_text.splitlines()

    artigos: List[Dict] = []
    current_label = None
    current_lines: List[str] = []

    def flush(current_label, current_lines, idx: int):
        if current_label is None:
            return
        artigo_id = f"Art-{idx}"
        artigos.append(
            {
                "id": artigo_id,
                "label": current_label.strip(),
                "text": "\\n".join(current_lines).strip(),
            }
        )

    idx = 0
    for line in linhas:
        if ARTIGO_PATTERN.search(line):
            flush(current_label, current_lines, idx)
            idx += 1
            current_label = line
            current_lines = []
        else:
            current_lines.append(line)

    flush(current_label, current_lines, idx)

    return artigos


def save_artigos_to_jsonl(artigos: List[Dict], output_path: str) -> str:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", encoding="utf-8") as f:
        for artigo in artigos:
            f.write(json.dumps(artigo, ensure_ascii=False) + "\\n")

    return str(p)


def estrutura_norma(
    raw_txt_path: str,
    output_jsonl_path: str = "data/normas_structured/artigos.jsonl",
) -> str:
    raw_text = load_raw_text(raw_txt_path)
    artigos = split_in_artigos(raw_text)
    return save_artigos_to_jsonl(artigos, output_jsonl_path)
