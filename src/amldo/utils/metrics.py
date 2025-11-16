"""
Sistema de métricas para AMLDO usando SQLite.

Substitui o sistema JSON antigo do AMLDO_W por um banco SQLite estruturado
com melhor performance e capacidades de query.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from amldo.core.config import settings


class MetricsManager:
    """
    Gerenciador de métricas do sistema usando SQLite.

    Armazena métricas de:
    - Consultas RAG (queries)
    - Processamento de documentos
    - Performance do sistema
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Inicializa o gerenciador de métricas.

        Args:
            db_path: Caminho para o banco SQLite (opcional)
        """
        if db_path is None:
            db_path = settings.data_dir / "metrics" / "metrics.db"

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """
        Inicializa o banco de dados SQLite com as tabelas necessárias.

        Cria duas tabelas principais:
        - processing_history: Histórico de processamento de documentos
        - query_history: Histórico de consultas RAG
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de processamento de documentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                files_processed INTEGER NOT NULL,
                total_chunks INTEGER NOT NULL,
                duration_seconds REAL,
                details TEXT
            )
        """)

        # Tabela de consultas RAG
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rag_version TEXT NOT NULL,
                question TEXT NOT NULL,
                response_time_ms REAL,
                success BOOLEAN DEFAULT 1,
                error_message TEXT
            )
        """)

        # Índices para melhor performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_query_timestamp
            ON query_history(timestamp)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_query_rag_version
            ON query_history(rag_version)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_processing_timestamp
            ON processing_history(timestamp)
        """)

        conn.commit()
        conn.close()

    def track_processing(
        self, files: int, chunks: int, duration: float = 0, details: str = ""
    ) -> int:
        """
        Registra um evento de processamento de documentos.

        Args:
            files: Número de arquivos processados
            chunks: Total de chunks criados
            duration: Duração em segundos
            details: Detalhes adicionais (JSON string, opcional)

        Returns:
            ID do registro criado
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO processing_history
            (files_processed, total_chunks, duration_seconds, details)
            VALUES (?, ?, ?, ?)
            """,
            (files, chunks, duration, details),
        )

        row_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return row_id

    def track_query(
        self,
        rag_version: str,
        question: str,
        response_time: float,
        success: bool = True,
        error_message: str = "",
    ) -> int:
        """
        Registra uma consulta RAG.

        Args:
            rag_version: Versão do RAG utilizada (v1, v2, v3)
            question: Pergunta do usuário
            response_time: Tempo de resposta em milissegundos
            success: Se a query foi bem-sucedida
            error_message: Mensagem de erro (se houver)

        Returns:
            ID do registro criado
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO query_history
            (rag_version, question, response_time_ms, success, error_message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (rag_version, question, response_time, success, error_message),
        )

        row_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return row_id

    def get_processing_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retorna histórico de processamento de documentos.

        Args:
            limit: Número máximo de registros

        Returns:
            Lista de dicionários com histórico
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM processing_history
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_query_history(self, limit: int = 100, rag_version: str = None) -> List[Dict[str, Any]]:
        """
        Retorna histórico de consultas RAG.

        Args:
            limit: Número máximo de registros
            rag_version: Filtrar por versão RAG (opcional)

        Returns:
            Lista de dicionários com histórico
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if rag_version:
            cursor.execute(
                """
                SELECT * FROM query_history
                WHERE rag_version = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (rag_version, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM query_history
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas gerais do sistema.

        Returns:
            Dicionário com estatísticas agregadas
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Estatísticas de queries por versão RAG
        cursor.execute("""
            SELECT
                rag_version,
                COUNT(*) as count,
                AVG(response_time_ms) as avg_time,
                MIN(response_time_ms) as min_time,
                MAX(response_time_ms) as max_time,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed
            FROM query_history
            GROUP BY rag_version
        """)
        rag_stats = cursor.fetchall()

        # Total de documentos processados
        cursor.execute("""
            SELECT
                SUM(files_processed) as total_files,
                SUM(total_chunks) as total_chunks,
                COUNT(*) as processing_count
            FROM processing_history
        """)
        processing_stats = cursor.fetchone()

        # Queries nas últimas 24h
        cursor.execute("""
            SELECT COUNT(*) as count_24h
            FROM query_history
            WHERE timestamp >= datetime('now', '-1 day')
        """)
        queries_24h = cursor.fetchone()[0]

        # Processamentos nas últimas 24h
        cursor.execute("""
            SELECT COUNT(*) as count_24h
            FROM processing_history
            WHERE timestamp >= datetime('now', '-1 day')
        """)
        processing_24h = cursor.fetchone()[0]

        conn.close()

        # Formatar estatísticas de RAG
        rag_stats_list = []
        for stat in rag_stats:
            rag_stats_list.append({
                "version": stat[0],
                "queries": stat[1],
                "avg_response_time_ms": round(stat[2], 2) if stat[2] else 0,
                "min_response_time_ms": round(stat[3], 2) if stat[3] else 0,
                "max_response_time_ms": round(stat[4], 2) if stat[4] else 0,
                "successful": stat[5],
                "failed": stat[6],
            })

        return {
            "rag_stats": rag_stats_list,
            "total_files_processed": processing_stats[0] or 0,
            "total_chunks_indexed": processing_stats[1] or 0,
            "total_processing_events": processing_stats[2] or 0,
            "queries_last_24h": queries_24h,
            "processing_last_24h": processing_24h,
        }

    def clear_old_records(self, days: int = 90):
        """
        Remove registros antigos para manter o banco limpo.

        Args:
            days: Manter apenas registros dos últimos N dias
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM query_history
            WHERE timestamp < datetime('now', '-' || ? || ' days')
            """,
            (days,),
        )

        cursor.execute(
            """
            DELETE FROM processing_history
            WHERE timestamp < datetime('now', '-' || ? || ' days')
            """,
            (days,),
        )

        deleted = cursor.rowcount
        conn.commit()

        # Vacuum para recuperar espaço
        cursor.execute("VACUUM")
        conn.close()

        return deleted


# =============================================================================
# Singleton e Funções Helper
# =============================================================================

_metrics_manager: Optional[MetricsManager] = None


def get_metrics_manager() -> MetricsManager:
    """
    Retorna a instância singleton do MetricsManager.

    Returns:
        Instância do MetricsManager
    """
    global _metrics_manager
    if _metrics_manager is None:
        _metrics_manager = MetricsManager()
    return _metrics_manager


def track_processing_metrics(files: int, chunks: int, duration: float = 0, details: str = "") -> int:
    """
    Atalho para registrar processamento de documentos.

    Args:
        files: Número de arquivos
        chunks: Total de chunks
        duration: Duração em segundos
        details: Detalhes adicionais

    Returns:
        ID do registro
    """
    return get_metrics_manager().track_processing(files, chunks, duration, details)


def track_query_metrics(
    rag_version: str,
    question: str,
    response_time: float,
    success: bool = True,
    error_message: str = "",
) -> int:
    """
    Atalho para registrar consulta RAG.

    Args:
        rag_version: Versão RAG
        question: Pergunta
        response_time: Tempo de resposta (ms)
        success: Sucesso
        error_message: Erro (se houver)

    Returns:
        ID do registro
    """
    return get_metrics_manager().track_query(
        rag_version, question, response_time, success, error_message
    )
