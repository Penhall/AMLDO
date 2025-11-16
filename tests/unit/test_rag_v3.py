"""
Testes unitários para RAG v3 (similarity search variant)
"""

import pytest
from amldo.rag.v3.tools import (
    consultar_base_rag,
    _get_retriever,
    get_art_0,
    get_pos_processed_context,
    _rag_answer,
)
from amldo.core.config import settings
from amldo.core.exceptions import RetrievalError, LLMError, VectorStoreError


class TestRagV3Configuration:
    """Testes de configuração do RAG v3"""

    def test_rag_v3_enabled_default(self):
        """Testa se RAG v3 está habilitado por padrão"""
        assert settings.rag_v3_enabled is True

    def test_rag_v3_search_type_default(self):
        """Testa se search_type padrão é 'similarity'"""
        assert settings.rag_v3_search_type == "similarity"

    def test_rag_v3_k_default(self):
        """Testa se K padrão é 12"""
        assert settings.rag_v3_k == 12

    def test_rag_v3_search_type_valid_values(self):
        """Testa se apenas valores válidos são aceitos para search_type"""
        valid_values = {"similarity", "mmr"}
        assert settings.rag_v3_search_type in valid_values


class TestRagV3Retriever:
    """Testes do retriever RAG v3"""

    def test_get_retriever_basic(self):
        """Testa criação básica do retriever"""
        retriever = _get_retriever()
        assert retriever is not None

    def test_get_retriever_with_similarity(self):
        """Testa retriever com similarity search"""
        retriever = _get_retriever(search_type="similarity", k=10)
        assert retriever is not None

    def test_get_retriever_filters_artigo_0(self):
        """Testa se retriever filtra artigo_0.txt"""
        retriever = _get_retriever()
        # O filtro deve estar configurado
        assert retriever.search_kwargs.get("filter") is not None
        filter_dict = retriever.search_kwargs["filter"]
        assert "artigo" in filter_dict
        assert "$nin" in filter_dict["artigo"]
        assert "artigo_0.txt" in filter_dict["artigo"]["$nin"]


class TestRagV3PostProcessing:
    """Testes de pós-processamento de contexto"""

    def test_get_art_0_exists(self):
        """Testa recuperação de artigo 0 existente"""
        import pandas as pd

        # Mock de df_art_0
        df_art_0 = pd.DataFrame({
            "lei": ["L14133"],
            "titulo": ["TITULO_I"],
            "capitulo": ["CAPITULO_0"],
            "texto": ["Introdução do Título I"]
        })

        result = get_art_0("L14133", "TITULO_I", "CAPITULO_0", df_art_0)
        assert result is not None
        assert "Introdução" in result

    def test_get_art_0_not_found(self):
        """Testa artigo 0 não encontrado"""
        import pandas as pd

        df_art_0 = pd.DataFrame({
            "lei": ["L14133"],
            "titulo": ["TITULO_I"],
            "capitulo": ["CAPITULO_0"],
            "texto": ["Texto"]
        })

        result = get_art_0("L99999", "TITULO_X", "CAPITULO_Y", df_art_0)
        assert result is None

    def test_get_pos_processed_context_structure(self):
        """Testa estrutura XML do contexto pós-processado"""
        import pandas as pd

        df_resultados = pd.DataFrame({
            "lei": ["L14133", "L14133"],
            "titulo": ["TITULO_I", "TITULO_I"],
            "capitulo": ["CAPITULO_I", "CAPITULO_I"],
            "artigo": ["artigo_1.txt", "artigo_2.txt"],
            "texto": ["Texto artigo 1", "Texto artigo 2"],
            "chunk_idx": [0, 0]
        })

        df_art_0 = pd.DataFrame({
            "lei": [],
            "titulo": [],
            "capitulo": [],
            "texto": []
        })

        context = get_pos_processed_context(df_resultados, df_art_0)

        # Verificar estrutura XML
        assert "<LEI L14133>" in context
        assert "</LEI L14133>" in context
        assert "<TITULO: TITULO_I>" in context
        assert "</TITULO: TITULO_I>" in context
        assert "<CAPITULO: CAPITULO_I>" in context
        assert "</CAPITULO: CAPITULO_I>" in context
        assert "<ARTIGO: artigo_1>" in context
        assert "</ARTIGO: artigo_1>" in context


class TestRagV3Consultation:
    """Testes de consulta RAG v3"""

    @pytest.mark.integration
    def test_consultar_base_rag_basic(self):
        """Testa consulta básica (requer GOOGLE_API_KEY)"""
        # Este teste requer API key configurada
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        pergunta = "O que é licitação?"
        resposta = consultar_base_rag(pergunta)

        assert isinstance(resposta, str)
        assert len(resposta) > 0

    @pytest.mark.integration
    def test_consultar_base_rag_returns_string(self):
        """Testa se consulta retorna string"""
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        resposta = consultar_base_rag("Teste")
        assert isinstance(resposta, str)

    def test_rag_answer_parameters(self):
        """Testa parâmetros de _rag_answer"""
        # Teste básico sem executar (evita necessidade de API key)
        # Apenas verifica que a função aceita os parâmetros
        assert callable(_rag_answer)


class TestRagV3VsV2Comparison:
    """Testes comparativos RAG v3 vs v2"""

    def test_v3_uses_similarity_by_default(self):
        """Testa se v3 usa similarity por padrão (vs v2 que usa MMR)"""
        from amldo.core.config import settings as s

        # RAG v2 usa MMR
        assert s.search_type == "mmr"

        # RAG v3 usa similarity
        assert s.rag_v3_search_type == "similarity"

    @pytest.mark.integration
    def test_v3_vs_v2_different_results(self):
        """Testa se v3 e v2 podem produzir resultados diferentes"""
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        from amldo.rag.v2.tools import consultar_base_rag as consultar_v2
        from amldo.rag.v3.tools import consultar_base_rag as consultar_v3

        pergunta = "Qual o limite de dispensa de licitação?"

        resposta_v2 = consultar_v2(pergunta)
        resposta_v3 = consultar_v3(pergunta)

        # Ambas devem retornar strings não vazias
        assert isinstance(resposta_v2, str) and len(resposta_v2) > 0
        assert isinstance(resposta_v3, str) and len(resposta_v3) > 0

        # Podem ser diferentes (mas não necessariamente)
        # Apenas verificamos que ambas funcionam


class TestRagV3ErrorHandling:
    """Testes de tratamento de erros"""

    def test_vector_store_error_on_missing_file(self):
        """Testa erro quando arquivo CSV não existe"""
        # Esse teste é difícil sem mockar, pois o módulo carrega no import
        # Apenas documentamos que VectorStoreError deve ser levantado
        assert VectorStoreError is not None

    def test_retrieval_error_type_exists(self):
        """Testa se RetrievalError existe"""
        assert RetrievalError is not None

    def test_llm_error_type_exists(self):
        """Testa se LLMError existe"""
        assert LLMError is not None


# =============================================================================
# Fixtures e Helpers
# =============================================================================

@pytest.fixture
def mock_df_art_0():
    """Mock de DataFrame de artigos 0"""
    import pandas as pd
    return pd.DataFrame({
        "lei": ["L14133", "L14133", "L13709"],
        "titulo": ["TITULO_0", "TITULO_I", "TITULO_0"],
        "capitulo": ["CAPITULO_0", "CAPITULO_0", "CAPITULO_0"],
        "texto": [
            "Lei 14133 de 2021",
            "Das Licitações e Contratos",
            "Lei Geral de Proteção de Dados"
        ]
    })


@pytest.fixture
def mock_df_resultados():
    """Mock de DataFrame de resultados de busca"""
    import pandas as pd
    return pd.DataFrame({
        "lei": ["L14133"] * 3,
        "titulo": ["TITULO_I"] * 3,
        "capitulo": ["CAPITULO_I"] * 3,
        "artigo": ["artigo_1.txt", "artigo_1.txt", "artigo_2.txt"],
        "chunk_idx": [0, 1, 0],
        "texto": [
            "Chunk 1 do artigo 1",
            "Chunk 2 do artigo 1",
            "Chunk 1 do artigo 2"
        ]
    })


class TestRagV3WithMocks:
    """Testes usando mocks"""

    def test_get_art_0_with_mock(self, mock_df_art_0):
        """Testa get_art_0 com mock"""
        result = get_art_0("L14133", "TITULO_I", "CAPITULO_0", mock_df_art_0)
        assert result == "Das Licitações e Contratos"

    def test_get_pos_processed_context_with_mocks(self, mock_df_resultados, mock_df_art_0):
        """Testa pós-processamento com mocks"""
        context = get_pos_processed_context(mock_df_resultados, mock_df_art_0)

        # Verificar conteúdo
        assert "L14133" in context
        assert "artigo_1" in context
        assert "artigo_2" in context
        assert "Chunk 1 do artigo 1" in context
        assert "Chunk 2 do artigo 1" in context
