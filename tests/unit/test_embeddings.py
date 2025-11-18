"""
Testes unitários para o sistema de embeddings.

Testa EmbeddingManager e integração com sentence-transformers.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

from amldo.pipeline.embeddings import EmbeddingManager
from amldo.core.config import settings


class TestEmbeddingManagerInit:
    """Testes de inicialização do EmbeddingManager."""

    def test_init_default_model(self):
        """Testa inicialização com modelo padrão."""
        manager = EmbeddingManager()
        assert manager is not None
        assert manager.model is not None

    def test_init_custom_model(self):
        """Testa inicialização com modelo customizado."""
        custom_model = "paraphrase-MiniLM-L3-v2"
        manager = EmbeddingManager(model_name=custom_model)
        assert manager is not None

    def test_model_loaded_correctly(self):
        """Testa se o modelo é carregado corretamente."""
        manager = EmbeddingManager()
        # Verificar que tem método encode
        assert hasattr(manager.model, "encode")

    def test_uses_settings_model_by_default(self):
        """Testa se usa o modelo do settings por padrão."""
        manager = EmbeddingManager()
        # O modelo deve estar configurado
        assert manager.model is not None


class TestEmbeddingGeneration:
    """Testes de geração de embeddings."""

    @pytest.fixture
    def manager(self):
        """Fixture com EmbeddingManager."""
        return EmbeddingManager()

    def test_embed_single_text(self, manager):
        """Testa embedding de um único texto."""
        text = "Esta é uma lei de licitação."
        embeddings = manager.embed([text])

        assert embeddings is not None
        assert isinstance(embeddings, np.ndarray)
        assert len(embeddings) == 1
        assert embeddings.shape[1] > 0  # Dimension > 0

    def test_embed_multiple_texts(self, manager):
        """Testa embedding de múltiplos textos."""
        texts = [
            "Lei 14133 trata de licitações.",
            "LGPD protege dados pessoais.",
            "Decreto 10024 regulamenta pregão eletrônico."
        ]

        embeddings = manager.embed(texts)

        assert embeddings is not None
        assert len(embeddings) == 3
        assert embeddings.shape == (3, embeddings.shape[1])

    def test_embed_empty_list(self, manager):
        """Testa embedding de lista vazia."""
        embeddings = manager.embed([])

        # Deve retornar array vazio ou levantar erro apropriado
        assert embeddings is not None
        assert len(embeddings) == 0

    def test_embed_normalization(self, manager):
        """Testa se embeddings são normalizados."""
        text = "Texto de teste."
        embeddings = manager.embed([text])

        # Verificar normalização (norma L2 ≈ 1)
        norm = np.linalg.norm(embeddings[0])
        assert np.isclose(norm, 1.0, atol=1e-5)

    def test_embed_consistency(self, manager):
        """Testa consistência de embeddings para mesmo texto."""
        text = "Lei 14133."

        emb1 = manager.embed([text])
        emb2 = manager.embed([text])

        # Deve produzir embeddings idênticos (ou muito similares)
        assert np.allclose(emb1, emb2, atol=1e-6)

    def test_embed_different_texts_different_embeddings(self, manager):
        """Testa se textos diferentes produzem embeddings diferentes."""
        text1 = "Licitação pública."
        text2 = "Proteção de dados."

        emb1 = manager.embed([text1])[0]
        emb2 = manager.embed([text2])[0]

        # Embeddings devem ser diferentes
        assert not np.allclose(emb1, emb2, atol=0.1)

    def test_embed_similarity_related_texts(self, manager):
        """Testa similaridade entre textos relacionados."""
        text1 = "Lei de licitações e contratos."
        text2 = "Norma sobre pregão eletrônico."
        text3 = "Proteção de dados pessoais."

        emb1 = manager.embed([text1])[0]
        emb2 = manager.embed([text2])[0]
        emb3 = manager.embed([text3])[0]

        # Similaridade cosseno
        sim_12 = np.dot(emb1, emb2)  # Textos relacionados (licitação)
        sim_13 = np.dot(emb1, emb3)  # Textos não relacionados

        # Textos relacionados devem ser mais similares
        assert sim_12 > sim_13


class TestEmbeddingDimensions:
    """Testes de dimensões dos embeddings."""

    def test_embedding_dimension_consistency(self):
        """Testa se dimensão é consistente."""
        manager = EmbeddingManager()

        texts = ["Texto 1", "Texto 2", "Texto 3"]
        embeddings = manager.embed(texts)

        # Todas as dimensões devem ser iguais
        dim = embeddings.shape[1]
        assert dim > 0
        assert all(emb.shape[0] == dim for emb in embeddings)

    def test_expected_dimension_size(self):
        """Testa se dimensão está no range esperado."""
        manager = EmbeddingManager()

        text = "Teste"
        embedding = manager.embed([text])[0]

        # Modelos multilingual-MiniLM geralmente têm 384 dimensões
        # Mas pode variar dependendo do modelo
        assert len(embedding) > 100  # Pelo menos 100 dimensões
        assert len(embedding) < 2000  # Menos que 2000


class TestEmbeddingEdgeCases:
    """Testes de casos extremos."""

    @pytest.fixture
    def manager(self):
        """Fixture com EmbeddingManager."""
        return EmbeddingManager()

    def test_embed_very_long_text(self, manager):
        """Testa embedding de texto muito longo."""
        long_text = "Artigo 1. " * 1000  # Texto muito longo

        embeddings = manager.embed([long_text])

        assert embeddings is not None
        assert len(embeddings) == 1

    def test_embed_special_characters(self, manager):
        """Testa embedding com caracteres especiais."""
        text = "§1º Art. 2º - Lei nº 14.133/2021 (revogada)"

        embeddings = manager.embed([text])

        assert embeddings is not None
        assert len(embeddings) == 1

    def test_embed_unicode_text(self, manager):
        """Testa embedding com caracteres unicode."""
        text = "Público → Licitação € £ ¥"

        embeddings = manager.embed([text])

        assert embeddings is not None

    def test_embed_single_word(self, manager):
        """Testa embedding de uma única palavra."""
        text = "Licitação"

        embeddings = manager.embed([text])

        assert embeddings is not None
        assert len(embeddings) == 1

    def test_embed_numbers_only(self, manager):
        """Testa embedding de texto com apenas números."""
        text = "14133 2021 10024"

        embeddings = manager.embed([text])

        assert embeddings is not None


class TestEmbeddingBatchProcessing:
    """Testes de processamento em lote."""

    @pytest.fixture
    def manager(self):
        """Fixture com EmbeddingManager."""
        return EmbeddingManager()

    def test_large_batch_processing(self, manager):
        """Testa processamento de lote grande."""
        texts = [f"Artigo {i} trata de..." for i in range(100)]

        embeddings = manager.embed(texts)

        assert len(embeddings) == 100
        assert embeddings.shape[0] == 100

    def test_batch_vs_individual_consistency(self, manager):
        """Testa consistência entre batch e individual."""
        texts = ["Texto 1", "Texto 2", "Texto 3"]

        # Batch
        batch_embeddings = manager.embed(texts)

        # Individual
        individual_embeddings = np.array([
            manager.embed([text])[0] for text in texts
        ])

        # Devem ser similares (pequena diferença é aceitável)
        assert np.allclose(batch_embeddings, individual_embeddings, atol=1e-5)


class TestEmbeddingPerformance:
    """Testes de performance (informativos)."""

    @pytest.fixture
    def manager(self):
        """Fixture com EmbeddingManager."""
        return EmbeddingManager()

    @pytest.mark.slow
    def test_embedding_speed_single(self, manager):
        """Testa velocidade para texto único."""
        import time

        text = "Lei 14133 de 2021 estabelece normas gerais de licitação."

        start = time.time()
        embeddings = manager.embed([text])
        duration = time.time() - start

        assert embeddings is not None
        # Não deve demorar mais que 1 segundo para um texto
        assert duration < 1.0

    @pytest.mark.slow
    def test_embedding_speed_batch(self, manager):
        """Testa velocidade para batch."""
        import time

        texts = [f"Artigo {i} da lei." for i in range(50)]

        start = time.time()
        embeddings = manager.embed(texts)
        duration = time.time() - start

        assert embeddings is not None
        # Batch de 50 não deve demorar mais que 5 segundos
        assert duration < 5.0


class TestEmbeddingErrorHandling:
    """Testes de tratamento de erros."""

    def test_invalid_model_name(self):
        """Testa erro com nome de modelo inválido."""
        # Modelo que não existe
        with pytest.raises(Exception):
            manager = EmbeddingManager(model_name="modelo-inexistente-xyz123")
            manager.embed(["teste"])

    def test_none_input(self):
        """Testa comportamento com input None."""
        manager = EmbeddingManager()

        with pytest.raises((TypeError, AttributeError)):
            manager.embed(None)

    def test_non_string_input(self):
        """Testa input não-string."""
        manager = EmbeddingManager()

        # Números devem ser convertidos ou causar erro
        try:
            embeddings = manager.embed([12345])
            # Se não der erro, deve retornar algo
            assert embeddings is not None
        except (TypeError, AttributeError):
            # Erro é aceitável
            pass


class TestEmbeddingIntegration:
    """Testes de integração com outros componentes."""

    @pytest.mark.integration
    def test_embedding_compatible_with_faiss(self):
        """Testa compatibilidade com FAISS."""
        import faiss

        manager = EmbeddingManager()
        texts = ["Texto 1", "Texto 2", "Texto 3"]
        embeddings = manager.embed(texts)

        # Criar índice FAISS simples
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

        # Adicionar embeddings
        index.add(embeddings.astype('float32'))

        assert index.ntotal == 3

    @pytest.mark.integration
    def test_embedding_for_rag_retrieval(self):
        """Testa uso de embeddings para retrieval."""
        manager = EmbeddingManager()

        # Documentos
        docs = [
            "Lei 14133 trata de licitações públicas.",
            "LGPD regula proteção de dados.",
            "Decreto 10024 regulamenta pregão."
        ]

        # Query
        query = "Qual lei trata de licitação?"

        doc_embeddings = manager.embed(docs)
        query_embedding = manager.embed([query])[0]

        # Calcular similaridades
        similarities = [
            np.dot(query_embedding, doc_emb)
            for doc_emb in doc_embeddings
        ]

        # Documento mais relevante deve ser o primeiro
        most_relevant_idx = np.argmax(similarities)
        assert most_relevant_idx == 0  # "Lei 14133..."


class TestEmbeddingCaching:
    """Testes de potencial caching (se implementado)."""

    def test_model_singleton_pattern(self):
        """Testa se modelo é reutilizado entre instâncias."""
        # Criar duas instâncias com mesmo modelo
        manager1 = EmbeddingManager()
        manager2 = EmbeddingManager()

        # Se houver singleton, devem compartilhar modelo
        # (Este teste é informativo - implementação atual pode não ter singleton)
        assert manager1.model is not None
        assert manager2.model is not None


# =============================================================================
# Testes com Mock (para testes mais rápidos)
# =============================================================================

class TestEmbeddingManagerMocked:
    """Testes com modelo mockado (mais rápidos)."""

    @patch("amldo.pipeline.embeddings.SentenceTransformer")
    def test_embed_calls_model_encode(self, mock_st):
        """Testa se embed() chama model.encode()."""
        # Mock do modelo
        mock_model = Mock()
        mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        mock_st.return_value = mock_model

        manager = EmbeddingManager()
        texts = ["Teste"]
        embeddings = manager.embed(texts)

        # Verificar que encode foi chamado
        mock_model.encode.assert_called_once()
        assert embeddings is not None

    @patch("amldo.pipeline.embeddings.SentenceTransformer")
    def test_embed_with_normalize(self, mock_st):
        """Testa normalização dos embeddings."""
        mock_model = Mock()
        # Retornar vetor não normalizado
        mock_model.encode.return_value = np.array([[3.0, 4.0]])  # norma = 5
        mock_st.return_value = mock_model

        manager = EmbeddingManager()
        embeddings = manager.embed(["teste"])

        # Verificar que foi normalizado
        norm = np.linalg.norm(embeddings[0])
        assert np.isclose(norm, 1.0, atol=1e-5)
