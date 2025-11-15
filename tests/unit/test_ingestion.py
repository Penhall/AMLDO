"""
Testes unitários para módulo de ingestão.
"""

from pathlib import Path

import pytest

from amldo.pipeline.ingestion.ingest import read_norma_file, ingest_norma
from amldo.core.exceptions import IngestionError


def test_read_norma_file_txt(sample_pdf_path: Path):
    """Testa leitura de arquivo TXT."""
    text = read_norma_file(str(sample_pdf_path))

    assert isinstance(text, str)
    assert len(text) > 0
    assert "Lei 99999" in text
    assert "Art. 1" in text


def test_read_norma_file_not_found():
    """Testa erro quando arquivo não existe."""
    with pytest.raises(FileNotFoundError):
        read_norma_file("/caminho/inexistente.txt")


def test_read_norma_file_unsupported_format(temp_dir: Path):
    """Testa erro com formato não suportado."""
    # Cria arquivo com extensão não suportada
    unsupported_file = temp_dir / "doc.docx"
    unsupported_file.write_bytes(b"fake docx content")

    with pytest.raises(IngestionError, match="Formato de arquivo não suportado"):
        read_norma_file(str(unsupported_file))


def test_ingest_norma(sample_pdf_path: Path, temp_dir: Path):
    """Testa ingestão completa de norma."""
    output_dir = temp_dir / "output"

    result_path = ingest_norma(
        input_path=str(sample_pdf_path), output_dir=str(output_dir), output_name="test_norma"
    )

    # Verifica que arquivo foi criado
    assert Path(result_path).exists()
    assert Path(result_path).suffix == ".txt"
    assert "test_norma" in result_path

    # Verifica conteúdo
    with open(result_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Lei 99999" in content
