"""
Modelos Pydantic para requisições da API.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Requisição para consulta RAG."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Pergunta do usuário sobre licitações e compliance",
    )
    rag_version: Optional[Literal["v1", "v2", "v3"]] = Field(
        default="v2",
        description="Versão do RAG a ser utilizada (v1: básico, v2: MMR, v3: similarity)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Qual é o limite de valor para dispensa de licitação?",
                "rag_version": "v2",
            }
        }


class UploadRequest(BaseModel):
    """Requisição para upload de documentos (usado para documentação)."""

    # Nota: FastAPI usa File() para upload, este modelo é apenas para docs
    pass
