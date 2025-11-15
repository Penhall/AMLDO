"""
Testes unitários para configuração centralizada.
"""

import pytest
from pathlib import Path

from amldo.core.config import Settings


def test_settings_with_env_vars(mock_env_vars):
    """Testa carregamento de settings com variáveis de ambiente."""
    settings = Settings()

    assert settings.google_api_key == "test_key_12345"
    assert settings.environment == "testing"
    assert settings.log_level == "DEBUG"


def test_settings_defaults(monkeypatch):
    """Testa valores padrão de settings."""
    # Define apenas a variável obrigatória
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key")

    settings = Settings()

    # Verifica defaults
    assert settings.embedding_model == "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    assert settings.llm_model == "gemini-2.5-flash"
    assert settings.search_k == 12
    assert settings.search_type == "mmr"
    assert settings.chunk_size == 1000


def test_settings_model_dump_safe(mock_env_vars):
    """Testa que model_dump_safe oculta secrets."""
    settings = Settings()

    dump = settings.model_dump_safe()

    # API key deve estar redacted
    assert dump["google_api_key"] == "***REDACTED***"

    # Outros valores devem estar presentes
    assert "llm_model" in dump
    assert "embedding_model" in dump


def test_settings_validate_paths(mock_env_vars):
    """Testa validação de paths."""
    settings = Settings()

    validation = settings.validate_paths()

    assert isinstance(validation, dict)
    assert "data_dir" in validation
    assert "vector_db" in validation
