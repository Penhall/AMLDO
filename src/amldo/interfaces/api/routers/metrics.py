"""
Router para métricas e estatísticas.

Endpoints para consultar métricas do sistema (queries, processamento, etc).
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from amldo.interfaces.api.models.response import MetricsResponse
from amldo.interfaces.api.dependencies import SettingsDep

# Importar FAISS para contar chunks
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

router = APIRouter()


@router.get("/stats", response_model=MetricsResponse, summary="Estatísticas gerais")
async def get_statistics(settings: SettingsDep = None):
    """
    Retorna estatísticas gerais do sistema.

    **Retorna:**
    - rag_stats: Estatísticas por versão RAG (placeholder por enquanto)
    - total_files_processed: Total de arquivos processados
    - total_chunks_indexed: Total de chunks no índice FAISS

    **Exemplo de uso:**
    ```bash
    curl "http://localhost:8000/api/metrics/stats"
    ```

    **Nota:**
    - As estatísticas de queries serão implementadas na Fase 4 (Sistema de Métricas)
    - Por enquanto, retorna apenas contagem de chunks no FAISS
    """
    # Contar chunks no FAISS
    vector_db_path = Path("data/vector_db/v1_faiss_vector_db")
    total_chunks = 0

    if vector_db_path.exists():
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                encode_kwargs={"normalize_embeddings": True},
            )
            vector_db = FAISS.load_local(
                str(vector_db_path), embeddings=embeddings, allow_dangerous_deserialization=True
            )
            total_chunks = len(vector_db.docstore._dict)
        except Exception:
            total_chunks = 0

    # Contar arquivos em data/raw
    raw_dir = Path("data/raw")
    total_files = len(list(raw_dir.glob("*.pdf"))) if raw_dir.exists() else 0

    # Placeholder para stats de RAG (será implementado na Fase 4)
    rag_stats = [
        {"version": "v1", "queries": 0, "avg_response_time_ms": 0},
        {"version": "v2", "queries": 0, "avg_response_time_ms": 0},
        {"version": "v3", "queries": 0, "avg_response_time_ms": 0},
    ]

    return MetricsResponse(
        rag_stats=rag_stats, total_files_processed=total_files, total_chunks_indexed=total_chunks
    )


@router.get("/processing-history", summary="Histórico de processamento")
async def get_processing_history(limit: int = 100):
    """
    Retorna histórico de processamento de documentos.

    **Parâmetros:**
    - limit: Número máximo de registros (default: 100)

    **Retorna:**
    - history: Lista de processamentos realizados

    **Exemplo de uso:**
    ```bash
    curl "http://localhost:8000/api/metrics/processing-history?limit=50"
    ```

    **Nota:**
    - Este endpoint será implementado completamente na Fase 4 com SQLite
    - Por enquanto, retorna lista vazia
    """
    # Placeholder - será implementado na Fase 4
    return JSONResponse(content={"history": []})


@router.get("/health", summary="Health Check das Métricas")
async def metrics_health():
    """
    Verifica se o sistema de métricas está funcionando.

    **Retorna:**
    - status: "ok" se o sistema estiver funcionando
    - metrics_enabled: Indica se as métricas estão habilitadas
    """
    return JSONResponse(
        content={"status": "ok", "metrics_enabled": False, "note": "Full metrics in Phase 4"}
    )
