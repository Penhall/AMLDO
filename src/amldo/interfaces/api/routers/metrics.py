"""
Router para métricas e estatísticas.

Endpoints para consultar métricas do sistema (queries, processamento, etc).
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from amldo.interfaces.api.models.response import MetricsResponse
from amldo.interfaces.api.dependencies import SettingsDep
from amldo.utils.metrics import get_metrics_manager

# Importar FAISS para contar chunks
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

router = APIRouter()


@router.get("/stats", response_model=MetricsResponse, summary="Estatísticas gerais")
async def get_statistics(settings: SettingsDep = None):
    """
    Retorna estatísticas gerais do sistema baseadas no banco SQLite de métricas.

    **Retorna:**
    - rag_stats: Estatísticas por versão RAG (queries, tempos, sucessos/falhas)
    - total_files_processed: Total de arquivos processados
    - total_chunks_indexed: Total de chunks criados

    **Exemplo de uso:**
    ```bash
    curl "http://localhost:8000/api/metrics/stats"
    ```

    **Dados incluem:**
    - Contagem de queries por versão RAG
    - Tempo médio/mín/máx de resposta
    - Taxa de sucesso/falha
    - Total de processamentos
    - Atividade nas últimas 24h
    """
    # Obter estatísticas do banco SQLite
    manager = get_metrics_manager()
    stats = manager.get_stats()

    # Contar chunks no FAISS para validação cruzada
    vector_db_path = Path("data/vector_db/v1_faiss_vector_db")
    faiss_chunks = 0

    if vector_db_path.exists():
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                encode_kwargs={"normalize_embeddings": True},
            )
            vector_db = FAISS.load_local(
                str(vector_db_path), embeddings=embeddings, allow_dangerous_deserialization=True
            )
            faiss_chunks = len(vector_db.docstore._dict)
        except Exception:
            faiss_chunks = 0

    # Usar contagem do FAISS se maior (mais preciso)
    total_chunks = max(stats["total_chunks_indexed"], faiss_chunks)

    return MetricsResponse(
        rag_stats=stats["rag_stats"],
        total_files_processed=stats["total_files_processed"],
        total_chunks_indexed=total_chunks,
    )


@router.get("/processing-history", summary="Histórico de processamento")
async def get_processing_history(limit: int = 100):
    """
    Retorna histórico de processamento de documentos do banco SQLite.

    **Parâmetros:**
    - limit: Número máximo de registros (default: 100, max: 1000)

    **Retorna:**
    - history: Lista de processamentos realizados com:
      - timestamp: Data/hora do processamento
      - files_processed: Arquivos processados
      - total_chunks: Chunks criados
      - duration_seconds: Duração
      - details: Detalhes adicionais (JSON)

    **Exemplo de uso:**
    ```bash
    curl "http://localhost:8000/api/metrics/processing-history?limit=50"
    ```
    """
    limit = min(limit, 1000)  # Limitar para evitar sobrecarga
    manager = get_metrics_manager()
    history = manager.get_processing_history(limit=limit)

    return JSONResponse(content={"history": history})


@router.get("/query-history", summary="Histórico de consultas RAG")
async def get_query_history(limit: int = 100, rag_version: str = None):
    """
    Retorna histórico de consultas RAG do banco SQLite.

    **Parâmetros:**
    - limit: Número máximo de registros (default: 100, max: 1000)
    - rag_version: Filtrar por versão (v1, v2, v3) - opcional

    **Retorna:**
    - history: Lista de queries com:
      - timestamp: Data/hora
      - rag_version: Versão usada
      - question: Pergunta
      - response_time_ms: Tempo de resposta
      - success: Se foi bem-sucedida
      - error_message: Erro (se houver)

    **Exemplo de uso:**
    ```bash
    curl "http://localhost:8000/api/metrics/query-history?rag_version=v2&limit=50"
    ```
    """
    limit = min(limit, 1000)
    manager = get_metrics_manager()
    history = manager.get_query_history(limit=limit, rag_version=rag_version)

    return JSONResponse(content={"history": history})


@router.get("/health", summary="Health Check das Métricas")
async def metrics_health():
    """
    Verifica se o sistema de métricas está funcionando.

    **Retorna:**
    - status: "ok" se o sistema estiver funcionando
    - metrics_enabled: Indica se as métricas estão habilitadas
    - db_path: Caminho do banco SQLite
    - db_exists: Se o banco existe
    """
    manager = get_metrics_manager()
    db_exists = manager.db_path.exists()

    return JSONResponse(
        content={
            "status": "ok",
            "metrics_enabled": True,
            "db_path": str(manager.db_path),
            "db_exists": db_exists,
        }
    )
