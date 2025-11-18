"""
Configuração de fixtures pytest para AMLDO.

Este arquivo define fixtures reutilizáveis para testes.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
import pandas as pd
import numpy as np


# =============================================================================
# Fixtures de Diretórios e Arquivos
# =============================================================================

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

TÍTULO I
DAS DISPOSIÇÕES GERAIS

CAPÍTULO I
DO OBJETO

Art. 1º Esta lei estabelece diretrizes para testes.

§1º Os testes devem ser completos.
§2º Os testes devem ser documentados.

Art. 2º Esta lei entra em vigor na data de sua publicação.
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
def sample_lei_completa() -> str:
    """Retorna texto completo de uma lei de teste."""
    return """
Lei 88888 de 2025

TÍTULO I
DAS LICITAÇÕES

CAPÍTULO I
DAS MODALIDADES

Art. 1º As licitações serão realizadas nas seguintes modalidades:

I - pregão;
II - concorrência;
III - concurso;
IV - leilão.

§1º O pregão é a modalidade preferencial.
§2º A concorrência é obrigatória para obras acima de R$ 3.300.000,00.

Art. 2º Fica dispensada a licitação quando o valor for inferior a R$ 50.000,00.

CAPÍTULO II
DOS PRAZOS

Art. 3º O prazo mínimo de publicação é de 8 dias úteis.

TÍTULO II
DOS CONTRATOS

CAPÍTULO I
DA FORMALIZAÇÃO

Art. 4º Todo contrato deve ser formalizado por escrito.
"""


# =============================================================================
# Fixtures de Dados (DataFrames)
# =============================================================================

@pytest.fixture
def sample_articles_df() -> pd.DataFrame:
    """DataFrame com artigos estruturados."""
    return pd.DataFrame({
        "lei": ["L14133", "L14133", "L13709", "L10024"],
        "titulo": ["TITULO_I", "TITULO_I", "TITULO_II", "TITULO_I"],
        "capitulo": ["CAPITULO_I", "CAPITULO_I", "CAPITULO_II", "CAPITULO_I"],
        "artigo": ["artigo_1.txt", "artigo_2.txt", "artigo_10.txt", "artigo_5.txt"],
        "chunk_idx": [0, 0, 0, 0],
        "texto": [
            "Art. 1º Esta Lei estabelece normas gerais de licitação.",
            "Art. 2º Para os fins desta Lei, considera-se licitação.",
            "Art. 10 Dados pessoais sensíveis são aqueles sobre origem racial.",
            "Art. 5º O pregão eletrônico é a modalidade preferencial."
        ]
    })


@pytest.fixture
def sample_art_0_df() -> pd.DataFrame:
    """DataFrame com artigos 0 (introduções de capítulos/títulos)."""
    return pd.DataFrame({
        "lei": ["L14133", "L14133", "L13709"],
        "titulo": ["TITULO_0", "TITULO_I", "TITULO_0"],
        "capitulo": ["CAPITULO_0", "CAPITULO_0", "CAPITULO_0"],
        "texto": [
            "Lei 14133 de 2021 - Nova Lei de Licitações",
            "TÍTULO I - Das Licitações e Contratos Administrativos",
            "Lei 13709 de 2018 - Lei Geral de Proteção de Dados"
        ]
    })


@pytest.fixture
def sample_metadata_list() -> list:
    """Lista de metadados de documentos."""
    return [
        {"lei": "L14133", "titulo": "TITULO_I", "capitulo": "CAPITULO_I", "artigo": "artigo_1.txt"},
        {"lei": "L14133", "titulo": "TITULO_I", "capitulo": "CAPITULO_II", "artigo": "artigo_5.txt"},
        {"lei": "L13709", "titulo": "TITULO_II", "capitulo": "CAPITULO_I", "artigo": "artigo_10.txt"},
    ]


# =============================================================================
# Fixtures de Configuração
# =============================================================================

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
    monkeypatch.setenv("VECTOR_DB_PATH", "/tmp/test_vector_db")


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


# =============================================================================
# Fixtures de Embeddings e Vector Store
# =============================================================================

@pytest.fixture
def mock_embeddings() -> np.ndarray:
    """Retorna embeddings mock (384 dimensões)."""
    np.random.seed(42)  # Seed para reprodutibilidade
    return np.random.rand(5, 384).astype('float32')


@pytest.fixture
def sample_csv_file(temp_dir: Path, sample_articles_df: pd.DataFrame) -> Path:
    """Cria arquivo CSV temporário com artigos."""
    csv_path = temp_dir / "artigos.csv"
    sample_articles_df.to_csv(csv_path, index=False)
    return csv_path


# =============================================================================
# Fixtures de Mocks
# =============================================================================

@pytest.fixture
def mock_llm_response():
    """Mock de resposta LLM."""
    return """
Com base na Lei 14133/2021, a licitação é o processo administrativo
de seleção da proposta mais vantajosa para a administração pública.
"""


@pytest.fixture
def mock_retriever_docs():
    """Mock de documentos retornados pelo retriever."""
    from unittest.mock import Mock

    doc1 = Mock()
    doc1.page_content = "Art. 1º Esta Lei estabelece normas gerais de licitação."
    doc1.metadata = {
        "lei": "L14133",
        "titulo": "TITULO_I",
        "capitulo": "CAPITULO_I",
        "artigo": "artigo_1.txt"
    }

    doc2 = Mock()
    doc2.page_content = "Art. 2º Para os fins desta Lei, considera-se licitação."
    doc2.metadata = {
        "lei": "L14133",
        "titulo": "TITULO_I",
        "capitulo": "CAPITULO_I",
        "artigo": "artigo_2.txt"
    }

    return [doc1, doc2]


# =============================================================================
# Fixtures de Métricas
# =============================================================================

@pytest.fixture
def temp_metrics_db(temp_dir: Path) -> Path:
    """Cria banco de métricas temporário."""
    db_path = temp_dir / "test_metrics.db"
    return db_path


@pytest.fixture
def metrics_manager(temp_metrics_db):
    """Cria MetricsManager com banco temporário."""
    from amldo.utils.metrics import MetricsManager
    return MetricsManager(db_path=temp_metrics_db)


# =============================================================================
# Fixtures de API
# =============================================================================

@pytest.fixture
def api_client():
    """Cliente de teste para FastAPI."""
    from fastapi.testclient import TestClient
    from amldo.interfaces.api.main import app

    return TestClient(app)


# =============================================================================
# Markers personalizados
# =============================================================================

def pytest_configure(config):
    """Configura markers personalizados."""
    config.addinivalue_line(
        "markers", "integration: marca testes de integração (lentos, requerem env completo)"
    )
    config.addinivalue_line(
        "markers", "slow: marca testes lentos (> 1 segundo)"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: marca testes que requerem GOOGLE_API_KEY"
    )
    config.addinivalue_line(
        "markers", "requires_vector_db: marca testes que requerem vector DB construído"
    )
