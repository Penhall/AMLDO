"""
Modelos Pydantic para respostas da API.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    """Resposta de consulta RAG."""

    answer: str = Field(..., description="Resposta gerada pelo sistema RAG")
    rag_version: str = Field(..., description="Versão do RAG utilizada")
    question: str = Field(..., description="Pergunta original do usuário")
    response_time_ms: Optional[float] = Field(None, description="Tempo de resposta em ms")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "De acordo com a Lei 14.133/2021, o limite para dispensa...",
                "rag_version": "v2",
                "question": "Qual é o limite de valor para dispensa de licitação?",
                "response_time_ms": 1523.4,
            }
        }


class UploadResponse(BaseModel):
    """Resposta de upload de documentos."""

    saved: List[str] = Field(..., description="Lista de arquivos salvos com sucesso")
    failed: List[Dict[str, str]] = Field(
        default_factory=list, description="Lista de arquivos que falhar am no upload"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "saved": ["lei_14133.pdf", "decreto_10024.pdf"],
                "failed": [{"file": "arquivo.txt", "error": "Tipo inválido - apenas PDF"}],
            }
        }


class ProcessResponse(BaseModel):
    """Resposta de processamento de documentos."""

    processed: int = Field(..., description="Número de arquivos processados")
    total_chunks: int = Field(..., description="Total de chunks indexados")
    files: List[Dict[str, Any]] = Field(..., description="Detalhes dos arquivos processados")
    duration_seconds: Optional[float] = Field(None, description="Duração do processamento")

    class Config:
        json_schema_extra = {
            "example": {
                "processed": 3,
                "total_chunks": 450,
                "files": [
                    {"file": "lei.pdf", "chunks": 150},
                    {"file": "decreto.pdf", "chunks": 200},
                    {"file": "portaria.pdf", "chunks": 100},
                ],
                "duration_seconds": 45.5,
            }
        }


class MetricsResponse(BaseModel):
    """Resposta de métricas do sistema."""

    rag_stats: List[Dict[str, Any]] = Field(..., description="Estatísticas por versão RAG")
    total_files_processed: int = Field(..., description="Total de arquivos processados")
    total_chunks_indexed: int = Field(..., description="Total de chunks no índice FAISS")

    class Config:
        json_schema_extra = {
            "example": {
                "rag_stats": [
                    {"version": "v1", "queries": 50, "avg_response_time_ms": 1200},
                    {"version": "v2", "queries": 150, "avg_response_time_ms": 1500},
                    {"version": "v3", "queries": 25, "avg_response_time_ms": 1100},
                ],
                "total_files_processed": 12,
                "total_chunks_indexed": 5430,
            }
        }
