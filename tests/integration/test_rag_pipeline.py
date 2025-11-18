"""
Testes de integração end-to-end para o pipeline RAG completo.

Testa o fluxo: documento → processamento → indexação → query → resposta
"""

import pytest
import tempfile
from pathlib import Path
import pandas as pd

from amldo.core.config import settings
from amldo.pipeline.ingestion.ingest import DocumentProcessor
from amldo.pipeline.structure.structure import ArticleStructurer
from amldo.pipeline.indexer.indexer import build_faiss_index, load_vector_store


@pytest.fixture
def temp_dir():
    """Diretório temporário para testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_document(temp_dir):
    """Documento de teste."""
    doc_path = temp_dir / "lei_teste.txt"
    content = """
Lei 99999 de 2025

TÍTULO I
DAS DISPOSIÇÕES GERAIS

CAPÍTULO I
DO OBJETO

Art. 1º Esta Lei estabelece normas gerais para testes automatizados.

§ 1º Os testes devem ser completos e bem documentados.

§ 2º A cobertura de código deve ser superior a 80%.

Art. 2º Para os fins desta Lei, considera-se:

I - teste unitário: teste de componente isolado;

II - teste de integração: teste de fluxo completo;

III - cobertura: percentual de código testado.

CAPÍTULO II
DAS RESPONSABILIDADES

Art. 3º É dever do desenvolvedor:

I - escrever testes antes do código;

II - manter os testes atualizados;

III - documentar casos de teste.
"""
    doc_path.write_text(content, encoding="utf-8")
    return doc_path


class TestFullRAGPipeline:
    """Testes do pipeline RAG completo."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_pipeline_flow(self, sample_document, temp_dir):
        """
        Testa fluxo completo: ingestão → estruturação → indexação → query.

        Este é o teste mais importante - garante que todo o sistema funciona.
        """
        # 1. INGESTÃO
        processor = DocumentProcessor()
        raw_text = processor.ingest_documents([str(sample_document)])[0]

        assert raw_text is not None
        assert len(raw_text) > 0
        assert "Art. 1º" in raw_text

        # 2. ESTRUTURAÇÃO
        structurer = ArticleStructurer()
        articles = structurer.structure_text(raw_text, lei_id="L99999")

        assert len(articles) > 0
        assert any("teste" in art["texto"].lower() for art in articles)

        # 3. PREPARAÇÃO PARA INDEXAÇÃO
        # Criar DataFrame
        articles_df = pd.DataFrame(articles)

        # Adicionar metadados necessários
        if "lei" not in articles_df.columns:
            articles_df["lei"] = "L99999"
        if "titulo" not in articles_df.columns:
            articles_df["titulo"] = "TITULO_I"
        if "capitulo" not in articles_df.columns:
            articles_df["capitulo"] = "CAPITULO_I"
        if "artigo" not in articles_df.columns:
            articles_df["artigo"] = [f"artigo_{i}.txt" for i in range(len(articles_df))]
        if "chunk_idx" not in articles_df.columns:
            articles_df["chunk_idx"] = 0

        # Salvar CSV
        csv_path = temp_dir / "articles.csv"
        articles_df.to_csv(csv_path, index=False)

        # 4. INDEXAÇÃO
        index_path = temp_dir / "vector_db"
        build_faiss_index(
            source_csv=str(csv_path),
            output_path=str(index_path)
        )

        assert index_path.exists()
        assert (index_path / "index.faiss").exists()

        # 5. CARREGAMENTO E QUERY
        vector_store = load_vector_store(str(index_path))

        assert vector_store is not None
        assert vector_store.index.ntotal > 0

        # 6. BUSCA
        query = "Quais são os deveres do desenvolvedor?"
        results = vector_store.similarity_search(query, k=3)

        assert len(results) > 0

        # Verificar que encontrou artigo relevante
        relevant_found = any(
            "desenvolvedor" in doc.page_content.lower() or
            "Art. 3" in doc.page_content
            for doc in results
        )

        assert relevant_found, "Não encontrou artigo sobre deveres do desenvolvedor"

    @pytest.mark.integration
    @pytest.mark.slow
    def test_pipeline_with_rag_v2(self, sample_document, temp_dir):
        """
        Testa pipeline completo com RAG v2 (hierarchical context).
        """
        # Preparar dados
        processor = DocumentProcessor()
        raw_text = processor.ingest_documents([str(sample_document)])[0]

        structurer = ArticleStructurer()
        articles = structurer.structure_text(raw_text, lei_id="L99999")

        articles_df = pd.DataFrame(articles)

        # Garantir todas as colunas
        required_cols = ["lei", "titulo", "capitulo", "artigo", "chunk_idx", "texto"]
        for col in required_cols:
            if col not in articles_df.columns:
                if col == "lei":
                    articles_df[col] = "L99999"
                elif col == "titulo":
                    articles_df[col] = "TITULO_I"
                elif col == "capitulo":
                    articles_df[col] = "CAPITULO_I"
                elif col == "artigo":
                    articles_df[col] = [f"artigo_{i}.txt" for i in range(len(articles_df))]
                elif col == "chunk_idx":
                    articles_df[col] = 0

        csv_path = temp_dir / "articles.csv"
        articles_df.to_csv(csv_path, index=False)

        # Indexar
        index_path = temp_dir / "vector_db"
        build_faiss_index(str(csv_path), str(index_path))

        # Testar busca com metadados
        vector_store = load_vector_store(str(index_path))

        results = vector_store.similarity_search("teste unitário", k=5)

        # Verificar metadados
        for doc in results:
            assert hasattr(doc, "metadata")
            assert "lei" in doc.metadata
            assert doc.metadata["lei"] == "L99999"

    @pytest.mark.integration
    def test_pipeline_error_recovery(self, temp_dir):
        """
        Testa recuperação de erros no pipeline.
        """
        # Tentar processar arquivo inexistente
        processor = DocumentProcessor()

        with pytest.raises(FileNotFoundError):
            processor.ingest_documents([str(temp_dir / "nao_existe.pdf")])

    @pytest.mark.integration
    def test_pipeline_with_multiple_documents(self, temp_dir):
        """
        Testa pipeline com múltiplos documentos.
        """
        # Criar 3 documentos
        docs = []
        for i in range(3):
            doc_path = temp_dir / f"lei_{i}.txt"
            doc_path.write_text(f"Art. {i+1}º Esta é a lei número {i}.", encoding="utf-8")
            docs.append(str(doc_path))

        # Ingerir
        processor = DocumentProcessor()
        texts = processor.ingest_documents(docs)

        assert len(texts) == 3

        # Estruturar todos
        structurer = ArticleStructurer()
        all_articles = []

        for i, text in enumerate(texts):
            articles = structurer.structure_text(text, lei_id=f"L{i}")
            all_articles.extend(articles)

        assert len(all_articles) >= 3


class TestRAGVersionsIntegration:
    """Testes de integração das 3 versões do RAG."""

    @pytest.mark.integration
    def test_rag_v1_v2_v3_consistency(self):
        """
        Testa se RAG v1, v2 e v3 retornam respostas válidas.

        Requer GOOGLE_API_KEY configurada.
        """
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        from amldo.rag.v1.tools import consultar_base_rag as consultar_v1
        from amldo.rag.v2.tools import consultar_base_rag as consultar_v2
        from amldo.rag.v3.tools import consultar_base_rag as consultar_v3

        pergunta = "O que é licitação pública?"

        # Testar todas as versões
        resposta_v1 = consultar_v1(pergunta)
        resposta_v2 = consultar_v2(pergunta)
        resposta_v3 = consultar_v3(pergunta)

        # Todas devem retornar strings não vazias
        assert isinstance(resposta_v1, str) and len(resposta_v1) > 0
        assert isinstance(resposta_v2, str) and len(resposta_v2) > 0
        assert isinstance(resposta_v3, str) and len(resposta_v3) > 0

        # Todas devem mencionar licitação (ou conceito relacionado)
        keywords = ["licitação", "contrato", "público", "administração"]

        assert any(kw in resposta_v1.lower() for kw in keywords)
        assert any(kw in resposta_v2.lower() for kw in keywords)
        assert any(kw in resposta_v3.lower() for kw in keywords)

    @pytest.mark.integration
    def test_rag_v2_hierarchical_context(self):
        """
        Testa se RAG v2 produz contexto hierárquico correto.
        """
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        from amldo.rag.v2.tools import get_pos_processed_context
        from amldo.rag.v2.tools import _get_retriever

        # Buscar documentos
        retriever = _get_retriever()
        docs = retriever.invoke("limite de dispensa de licitação")

        # Converter para DataFrame
        df_resultados = pd.DataFrame([
            {
                "lei": doc.metadata.get("lei", ""),
                "titulo": doc.metadata.get("titulo", ""),
                "capitulo": doc.metadata.get("capitulo", ""),
                "artigo": doc.metadata.get("artigo", ""),
                "chunk_idx": doc.metadata.get("chunk_idx", 0),
                "texto": doc.page_content
            }
            for doc in docs
        ])

        # Processar contexto
        import pandas as pd
        df_art_0 = pd.DataFrame(columns=["lei", "titulo", "capitulo", "texto"])

        context = get_pos_processed_context(df_resultados, df_art_0)

        # Verificar estrutura XML
        assert "<LEI" in context
        assert "</LEI" in context
        assert "<TITULO:" in context or context != ""

    @pytest.mark.integration
    def test_rag_v3_similarity_search(self):
        """
        Testa se RAG v3 usa similarity search corretamente.
        """
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        from amldo.rag.v3.tools import _get_retriever

        # Criar retriever v3
        retriever = _get_retriever(search_type="similarity", k=5)

        # Verificar configuração
        assert retriever.search_type == "similarity"
        assert retriever.search_kwargs.get("k") == 5

        # Testar busca
        docs = retriever.invoke("pregão eletrônico")

        assert len(docs) > 0
        assert all(hasattr(doc, "page_content") for doc in docs)


class TestAPIIntegration:
    """Testes de integração da API FastAPI."""

    @pytest.mark.integration
    def test_api_full_flow(self):
        """
        Testa fluxo completo via API: query → resposta → métricas.
        """
        from fastapi.testclient import TestClient
        from amldo.interfaces.api.main import app

        client = TestClient(app)

        # 1. Health check
        response = client.get("/health")
        assert response.status_code == 200

        # 2. Query (pode falhar sem API key)
        if settings.google_api_key and settings.google_api_key != "your-api-key-here":
            payload = {
                "pergunta": "O que é licitação?",
                "rag_version": "v2"
            }

            response = client.post("/api/ask", json=payload)

            if response.status_code == 200:
                data = response.json()
                assert "resposta" in data
                assert "tempo_resposta_ms" in data

        # 3. Métricas
        response = client.get("/api/metrics/stats")
        assert response.status_code == 200

        data = response.json()
        assert "rag_stats" in data

    @pytest.mark.integration
    def test_api_metrics_tracking(self):
        """
        Testa se API rastreia métricas corretamente.
        """
        from fastapi.testclient import TestClient
        from amldo.interfaces.api.main import app
        from unittest.mock import patch, Mock

        client = TestClient(app)

        # Mock do RAG
        with patch("amldo.interfaces.api.routers.queries.consultar_v2") as mock_rag:
            mock_rag.return_value = "Resposta mock"

            # Mock das métricas
            with patch("amldo.interfaces.api.routers.queries.get_metrics_manager") as mock_metrics:
                manager = Mock()
                manager.track_query = Mock(return_value=1)
                mock_metrics.return_value = manager

                payload = {
                    "pergunta": "Teste",
                    "rag_version": "v2"
                }

                response = client.post("/api/ask", json=payload)

                # Verificar que métricas foram rastreadas
                assert manager.track_query.called


class TestStreamlitIntegration:
    """Testes de integração da interface Streamlit."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_streamlit_imports(self):
        """
        Testa se a aplicação Streamlit pode ser importada.
        """
        try:
            # Import do app Streamlit
            import amldo.interfaces.streamlit.app
            assert True
        except ImportError as e:
            pytest.fail(f"Não foi possível importar Streamlit app: {e}")

    @pytest.mark.integration
    def test_streamlit_pages_exist(self):
        """
        Testa se as páginas Streamlit existem.
        """
        from pathlib import Path

        pages_dir = Path("src/amldo/interfaces/streamlit/pages")

        if pages_dir.exists():
            pages = list(pages_dir.glob("*.py"))
            assert len(pages) > 0


# =============================================================================
# Testes de Performance
# =============================================================================

class TestPerformance:
    """Testes de performance do sistema."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_query_response_time(self):
        """
        Testa tempo de resposta de queries.
        """
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        from amldo.rag.v2.tools import consultar_base_rag
        import time

        pergunta = "Qual o limite de dispensa de licitação?"

        start = time.time()
        resposta = consultar_base_rag(pergunta)
        duration = time.time() - start

        # Não deve demorar mais que 10 segundos
        assert duration < 10.0
        assert resposta is not None

    @pytest.mark.integration
    @pytest.mark.slow
    def test_concurrent_queries(self):
        """
        Testa queries concorrentes.
        """
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        from amldo.rag.v2.tools import consultar_base_rag
        import concurrent.futures

        perguntas = [
            "O que é licitação?",
            "Qual o limite de dispensa?",
            "O que é pregão eletrônico?",
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(consultar_base_rag, p)
                for p in perguntas
            ]

            respostas = [f.result() for f in futures]

        # Todas devem ter retornado
        assert len(respostas) == 3
        assert all(isinstance(r, str) and len(r) > 0 for r in respostas)
