"""
Testes unitários para módulo de estruturação.
"""

from pathlib import Path

import pytest

from amldo.pipeline.structure.structure import split_in_artigos, estrutura_norma, load_raw_text
from amldo.core.exceptions import StructureError


def test_split_in_artigos(sample_text: str):
    """Testa divisão de texto em artigos."""
    artigos = split_in_artigos(sample_text)

    assert len(artigos) == 2  # Art. 1 e Art. 2

    # Verifica primeiro artigo
    assert artigos[0]["id"] == "Art-0"
    assert "Art. 1" in artigos[0]["label"]
    assert "diretrizes para testes" in artigos[0]["text"]

    # Verifica segundo artigo
    assert artigos[1]["id"] == "Art-1"
    assert "Art. 2" in artigos[1]["label"]


def test_load_raw_text(sample_pdf_path: Path):
    """Testa carregamento de texto bruto."""
    text = load_raw_text(str(sample_pdf_path))

    assert isinstance(text, str)
    assert len(text) > 0


def test_load_raw_text_not_found():
    """Testa erro quando arquivo não existe."""
    with pytest.raises(FileNotFoundError):
        load_raw_text("/caminho/inexistente.txt")


def test_estrutura_norma(sample_pdf_path: Path, temp_dir: Path):
    """Testa estruturação completa de norma."""
    output_path = temp_dir / "artigos.jsonl"

    result_path = estrutura_norma(
        raw_txt_path=str(sample_pdf_path), output_jsonl_path=str(output_path)
    )

    # Verifica que arquivo foi criado
    assert Path(result_path).exists()
    assert Path(result_path).suffix == ".jsonl"

    # Verifica conteúdo (deve ter 2 linhas, uma por artigo)
    with open(result_path, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]
    assert len(lines) == 2

    # Verifica formato JSON
    import json

    first_article = json.loads(lines[0])
    assert "id" in first_article
    assert "label" in first_article
    assert "text" in first_article
