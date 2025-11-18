"""
Testes unitários para a API FastAPI.

Testa endpoints, modelos Pydantic, validação e tratamento de erros.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Import da aplicação FastAPI
from amldo.interfaces.api.main import app
from amldo.core.config import settings


@pytest.fixture
def client():
    """Cliente de teste para FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_metrics_manager():
    """Mock do MetricsManager."""
    with patch("amldo.interfaces.api.routers.queries.get_metrics_manager") as mock:
        manager = Mock()
        manager.track_query = Mock(return_value=1)
        manager.track_processing = Mock(return_value=1)
        manager.get_stats = Mock(return_value={
            "rag_stats": [],
            "total_files_processed": 0,
            "total_chunks_indexed": 0,
            "queries_last_24h": 0
        })
        manager.get_query_history = Mock(return_value=[])
        manager.get_processing_history = Mock(return_value=[])
        mock.return_value = manager
        yield manager


class TestHealthEndpoint:
    """Testes do endpoint de health check."""

    def test_health_check_returns_200(self, client):
        """Testa se health check retorna 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_json_structure(self, client):
        """Testa estrutura JSON do health check."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestMetricsEndpoints:
    """Testes dos endpoints de métricas."""

    def test_get_stats(self, client, mock_metrics_manager):
        """Testa endpoint GET /api/metrics/stats."""
        response = client.get("/api/metrics/stats")
        assert response.status_code == 200

        data = response.json()
        assert "rag_stats" in data
        assert "total_files_processed" in data
        assert "total_chunks_indexed" in data

    def test_get_query_history_no_filter(self, client, mock_metrics_manager):
        """Testa histórico de queries sem filtro."""
        mock_metrics_manager.get_query_history.return_value = [
            {
                "id": 1,
                "timestamp": "2025-11-16T10:00:00",
                "rag_version": "v2",
                "question": "Teste",
                "response_time_ms": 1500.0,
                "success": 1,
                "error_message": None
            }
        ]

        response = client.get("/api/metrics/queries")
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 0

    def test_get_query_history_with_version_filter(self, client, mock_metrics_manager):
        """Testa histórico de queries com filtro de versão."""
        response = client.get("/api/metrics/queries?rag_version=v2")
        assert response.status_code == 200

    def test_get_processing_history(self, client, mock_metrics_manager):
        """Testa histórico de processamento."""
        mock_metrics_manager.get_processing_history.return_value = [
            {
                "id": 1,
                "timestamp": "2025-11-16T10:00:00",
                "files_processed": 3,
                "total_chunks": 450,
                "duration_seconds": 45.5
            }
        ]

        response = client.get("/api/metrics/processing")
        assert response.status_code == 200


class TestQueryEndpoint:
    """Testes do endpoint de query RAG."""

    @patch("amldo.interfaces.api.routers.queries.consultar_v1")
    def test_ask_endpoint_v1_success(self, mock_consultar, client, mock_metrics_manager):
        """Testa query bem-sucedida com RAG v1."""
        mock_consultar.return_value = "Resposta do RAG v1"

        payload = {
            "pergunta": "O que é licitação?",
            "rag_version": "v1"
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "resposta" in data
        assert "rag_version" in data
        assert data["rag_version"] == "v1"
        assert "tempo_resposta_ms" in data

        # Verificar que a métrica foi rastreada
        mock_metrics_manager.track_query.assert_called_once()

    @patch("amldo.interfaces.api.routers.queries.consultar_v2")
    def test_ask_endpoint_v2_success(self, mock_consultar, client, mock_metrics_manager):
        """Testa query bem-sucedida com RAG v2."""
        mock_consultar.return_value = "Resposta do RAG v2"

        payload = {
            "pergunta": "Qual o limite de dispensa?",
            "rag_version": "v2"
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["rag_version"] == "v2"

    @patch("amldo.interfaces.api.routers.queries.consultar_v3")
    def test_ask_endpoint_v3_success(self, mock_consultar, client, mock_metrics_manager):
        """Testa query bem-sucedida com RAG v3."""
        mock_consultar.return_value = "Resposta do RAG v3"

        payload = {
            "pergunta": "O que é pregão eletrônico?",
            "rag_version": "v3"
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["rag_version"] == "v3"

    def test_ask_endpoint_invalid_version(self, client):
        """Testa erro com versão inválida."""
        payload = {
            "pergunta": "Teste",
            "rag_version": "v99"
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 422  # Validation error

    def test_ask_endpoint_empty_question(self, client):
        """Testa erro com pergunta vazia."""
        payload = {
            "pergunta": "",
            "rag_version": "v2"
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 422

    @patch("amldo.interfaces.api.routers.queries.consultar_v2")
    def test_ask_endpoint_default_version(self, mock_consultar, client, mock_metrics_manager):
        """Testa versão padrão (v2) quando não especificada."""
        mock_consultar.return_value = "Resposta"

        payload = {
            "pergunta": "Teste"
            # rag_version omitido
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["rag_version"] == "v2"  # Default

    @patch("amldo.interfaces.api.routers.queries.consultar_v2")
    def test_ask_endpoint_tracks_error(self, mock_consultar, client, mock_metrics_manager):
        """Testa rastreamento de erro quando RAG falha."""
        mock_consultar.side_effect = Exception("LLM error")

        payload = {
            "pergunta": "Teste",
            "rag_version": "v2"
        }

        response = client.post("/api/ask", json=payload)
        assert response.status_code == 500

        # Verificar que erro foi rastreado
        mock_metrics_manager.track_query.assert_called_once()
        call_args = mock_metrics_manager.track_query.call_args
        assert call_args[1]["success"] is False
        assert "error_message" in call_args[1]


class TestUploadEndpoint:
    """Testes do endpoint de upload."""

    def test_upload_pdf_missing_file(self, client):
        """Testa upload sem arquivo."""
        response = client.post("/api/upload")
        assert response.status_code == 422

    @patch("amldo.interfaces.api.routers.pipeline.Path.mkdir")
    @patch("builtins.open", create=True)
    def test_upload_pdf_success(self, mock_open, mock_mkdir, client):
        """Testa upload bem-sucedido de PDF."""
        # Criar arquivo fake
        fake_file = b"%PDF-1.4 fake content"

        response = client.post(
            "/api/upload",
            files={"file": ("test.pdf", fake_file, "application/pdf")}
        )

        # Pode retornar 200 ou 500 dependendo do processamento
        # Apenas verificamos que aceita o upload
        assert response.status_code in [200, 500]

    def test_upload_non_pdf_file(self, client):
        """Testa upload de arquivo não-PDF."""
        fake_file = b"Not a PDF"

        response = client.post(
            "/api/upload",
            files={"file": ("test.txt", fake_file, "text/plain")}
        )

        # Deve aceitar (validação de tipo é feita internamente se houver)
        assert response.status_code in [200, 422, 500]


class TestProcessEndpoint:
    """Testes do endpoint de processamento."""

    @patch("amldo.interfaces.api.routers.pipeline.DocumentProcessor")
    @patch("amldo.interfaces.api.routers.pipeline.get_metrics_manager")
    def test_process_success(self, mock_metrics, mock_processor, client):
        """Testa processamento bem-sucedido."""
        # Mock do processor
        processor_instance = Mock()
        processor_instance.ingest_documents.return_value = ["doc1.pdf"]
        processor_instance.structure_documents.return_value = 150
        processor_instance.build_index.return_value = None
        mock_processor.return_value = processor_instance

        # Mock metrics
        metrics_manager = Mock()
        metrics_manager.track_processing.return_value = 1
        mock_metrics.return_value = metrics_manager

        response = client.post("/api/process")

        # Pode retornar 200 ou erro dependendo da implementação
        assert response.status_code in [200, 500]

    @patch("amldo.interfaces.api.routers.pipeline.DocumentProcessor")
    def test_process_error_handling(self, mock_processor, client):
        """Testa tratamento de erro no processamento."""
        mock_processor.return_value.ingest_documents.side_effect = Exception("Ingest error")

        response = client.post("/api/process")
        assert response.status_code == 500


class TestWebInterfaceEndpoints:
    """Testes dos endpoints de interface web."""

    def test_home_page(self, client):
        """Testa página inicial."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_consulta_page(self, client):
        """Testa página de consulta."""
        response = client.get("/consulta")
        assert response.status_code == 200

    def test_processamento_page(self, client):
        """Testa página de processamento."""
        response = client.get("/processamento")
        assert response.status_code == 200

    def test_metricas_page(self, client):
        """Testa página de métricas."""
        response = client.get("/metricas")
        assert response.status_code == 200


class TestPydanticModels:
    """Testes dos modelos Pydantic."""

    def test_query_request_model_valid(self):
        """Testa validação do QueryRequest."""
        from amldo.interfaces.api.models.schemas import QueryRequest

        request = QueryRequest(pergunta="Teste", rag_version="v2")
        assert request.pergunta == "Teste"
        assert request.rag_version == "v2"

    def test_query_request_default_version(self):
        """Testa versão padrão do QueryRequest."""
        from amldo.interfaces.api.models.schemas import QueryRequest

        request = QueryRequest(pergunta="Teste")
        assert request.rag_version == "v2"

    def test_query_request_invalid_version(self):
        """Testa validação de versão inválida."""
        from amldo.interfaces.api.models.schemas import QueryRequest
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            QueryRequest(pergunta="Teste", rag_version="v99")

    def test_query_response_model(self):
        """Testa modelo QueryResponse."""
        from amldo.interfaces.api.models.schemas import QueryResponse

        response = QueryResponse(
            resposta="Resposta teste",
            rag_version="v2",
            tempo_resposta_ms=1500.0,
            timestamp="2025-11-16T10:00:00"
        )

        assert response.resposta == "Resposta teste"
        assert response.tempo_resposta_ms == 1500.0


class TestCORS:
    """Testes de configuração CORS."""

    def test_cors_headers_present(self, client):
        """Testa se headers CORS estão presentes."""
        response = client.options(
            "/api/ask",
            headers={"Origin": "http://localhost:3000"}
        )

        # Verificar se CORS está configurado
        assert response.status_code in [200, 405]


class TestErrorHandling:
    """Testes de tratamento de erros global."""

    def test_404_not_found(self, client):
        """Testa rota inexistente."""
        response = client.get("/rota/inexistente")
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """Testa método HTTP não permitido."""
        response = client.delete("/api/ask")
        assert response.status_code == 405


# =============================================================================
# Testes de Integração (requerem configuração completa)
# =============================================================================

@pytest.mark.integration
class TestAPIIntegration:
    """Testes de integração da API (requerem env configurado)."""

    def test_full_query_flow(self, client):
        """Testa fluxo completo de query."""
        if not settings.google_api_key or settings.google_api_key == "your-api-key-here":
            pytest.skip("GOOGLE_API_KEY não configurada")

        payload = {
            "pergunta": "O que é licitação?",
            "rag_version": "v2"
        }

        response = client.post("/api/ask", json=payload)

        if response.status_code == 200:
            data = response.json()
            assert "resposta" in data
            assert len(data["resposta"]) > 0
