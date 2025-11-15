"""
Configuração de fixtures pytest para AMLDO.

Este arquivo define fixtures reutilizáveis para testes.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Cria um diretório temporário para testes.

    Yields:
        Path do diretório temporário (automaticamente removido após o teste)
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text() -> str:
    """Retorna texto de exemplo de uma norma simplificada."""
    return """
Lei 99999 de 2025

Art. 1. Esta lei estabelece diretrizes para testes.

§1º Os testes devem ser completos.
§2º Os testes devem ser documentados.

Art. 2. Esta lei entra em vigor na data de sua publicação.
"""


@pytest.fixture
def sample_pdf_path(temp_dir: Path, sample_text: str) -> Path:
    """
    Cria um arquivo TXT temporário (simulando um documento).

    Args:
        temp_dir: Diretório temporário
        sample_text: Texto de exemplo

    Returns:
        Path para o arquivo criado
    """
    file_path = temp_dir / "sample_doc.txt"
    file_path.write_text(sample_text, encoding="utf-8")
    return file_path


@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    Define variáveis de ambiente mock para testes.

    Args:
        monkeypatch: Fixture do pytest para modificar env vars
    """
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key_12345")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")


@pytest.fixture(autouse=True)
def reset_settings():
    """
    Reseta settings após cada teste para evitar interferência.

    Este fixture roda automaticamente em todos os testes.
    """
    # Antes do teste: nada a fazer
    yield
    # Depois do teste: reload settings se necessário
    # (para testes que modificam config)
    from amldo.core.config import settings

    # Se você implementar um método reload, use aqui
    # settings.reload()
