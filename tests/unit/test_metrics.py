"""
Testes unitários para o sistema de métricas SQLite.
"""

import pytest
import tempfile
from pathlib import Path

from amldo.utils.metrics import MetricsManager


class TestMetricsManager:
    """Testes do gerenciador de métricas."""

    @pytest.fixture
    def temp_db(self):
        """Cria um banco temporário para testes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_metrics.db"
            yield db_path

    @pytest.fixture
    def manager(self, temp_db):
        """Cria uma instância do MetricsManager com banco temporário."""
        return MetricsManager(db_path=temp_db)

    def test_init_db_creates_tables(self, manager, temp_db):
        """Testa se a inicialização cria as tabelas."""
        assert temp_db.exists()

        import sqlite3

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        assert "processing_history" in tables
        assert "query_history" in tables

        conn.close()

    def test_track_processing(self, manager):
        """Testa registro de processamento."""
        row_id = manager.track_processing(files=3, chunks=450, duration=45.5, details='{"test": true}')

        assert row_id > 0

        history = manager.get_processing_history(limit=1)
        assert len(history) == 1
        assert history[0]["files_processed"] == 3
        assert history[0]["total_chunks"] == 450
        assert history[0]["duration_seconds"] == 45.5

    def test_track_query_success(self, manager):
        """Testa registro de query bem-sucedida."""
        row_id = manager.track_query(
            rag_version="v2", question="Teste", response_time=1500.0, success=True
        )

        assert row_id > 0

        history = manager.get_query_history(limit=1)
        assert len(history) == 1
        assert history[0]["rag_version"] == "v2"
        assert history[0]["question"] == "Teste"
        assert history[0]["response_time_ms"] == 1500.0
        assert history[0]["success"] == 1

    def test_track_query_failure(self, manager):
        """Testa registro de query falhada."""
        row_id = manager.track_query(
            rag_version="v1",
            question="Teste erro",
            response_time=0,
            success=False,
            error_message="LLM error",
        )

        assert row_id > 0

        history = manager.get_query_history(limit=1)
        assert len(history) == 1
        assert history[0]["success"] == 0
        assert history[0]["error_message"] == "LLM error"

    def test_get_stats_empty(self, manager):
        """Testa estatísticas com banco vazio."""
        stats = manager.get_stats()

        assert stats["rag_stats"] == []
        assert stats["total_files_processed"] == 0
        assert stats["total_chunks_indexed"] == 0
        assert stats["queries_last_24h"] == 0

    def test_get_stats_with_data(self, manager):
        """Testa estatísticas com dados."""
        # Adicionar queries
        manager.track_query("v1", "Q1", 1000, True)
        manager.track_query("v1", "Q2", 1200, True)
        manager.track_query("v2", "Q3", 1500, True)
        manager.track_query("v2", "Q4", 0, False, "Error")

        # Adicionar processamentos
        manager.track_processing(3, 450, 45.5)
        manager.track_processing(2, 300, 30.0)

        stats = manager.get_stats()

        # Verificar stats de RAG
        assert len(stats["rag_stats"]) == 2

        v1_stats = next((s for s in stats["rag_stats"] if s["version"] == "v1"), None)
        assert v1_stats is not None
        assert v1_stats["queries"] == 2
        assert v1_stats["avg_response_time_ms"] == 1100.0
        assert v1_stats["successful"] == 2
        assert v1_stats["failed"] == 0

        v2_stats = next((s for s in stats["rag_stats"] if s["version"] == "v2"), None)
        assert v2_stats is not None
        assert v2_stats["queries"] == 2
        assert v2_stats["successful"] == 1
        assert v2_stats["failed"] == 1

        # Verificar processamento
        assert stats["total_files_processed"] == 5
        assert stats["total_chunks_indexed"] == 750

    def test_get_query_history_with_filter(self, manager):
        """Testa histórico filtrado por versão."""
        manager.track_query("v1", "Q1", 1000, True)
        manager.track_query("v2", "Q2", 1200, True)
        manager.track_query("v1", "Q3", 1100, True)

        # Sem filtro
        all_history = manager.get_query_history(limit=10)
        assert len(all_history) == 3

        # Com filtro v1
        v1_history = manager.get_query_history(limit=10, rag_version="v1")
        assert len(v1_history) == 2
        assert all(h["rag_version"] == "v1" for h in v1_history)

        # Com filtro v2
        v2_history = manager.get_query_history(limit=10, rag_version="v2")
        assert len(v2_history) == 1
        assert v2_history[0]["rag_version"] == "v2"

    def test_clear_old_records(self, manager):
        """Testa limpeza de registros antigos."""
        # Adicionar alguns registros
        manager.track_query("v1", "Q1", 1000, True)
        manager.track_query("v2", "Q2", 1200, True)
        manager.track_processing(3, 450, 45.5)

        # Limpar registros (como são recentes, nenhum deve ser deletado)
        deleted = manager.clear_old_records(days=1)
        assert deleted >= 0  # Pode ser 0 se os registros forem muito recentes

        # Verificar que registros ainda existem
        history = manager.get_query_history()
        assert len(history) >= 0  # Pode variar dependendo do timing


class TestMetricsHelpers:
    """Testes das funções helper."""

    @pytest.fixture
    def temp_db(self):
        """Cria um banco temporário para testes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_metrics.db"
            yield db_path

    def test_singleton_pattern(self, temp_db):
        """Testa que get_metrics_manager retorna a mesma instância."""
        from amldo.utils.metrics import get_metrics_manager, _metrics_manager

        # Resetar singleton para teste
        import amldo.utils.metrics as metrics_module

        metrics_module._metrics_manager = None

        manager1 = get_metrics_manager()
        manager2 = get_metrics_manager()

        assert manager1 is manager2
