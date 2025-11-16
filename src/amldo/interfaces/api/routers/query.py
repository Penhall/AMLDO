"""
Router para consultas RAG.

Endpoints para fazer perguntas ao sistema RAG usando as versões v1, v2 ou v3.
"""

import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from amldo.interfaces.api.models.request import QueryRequest
from amldo.interfaces.api.models.response import QueryResponse
from amldo.interfaces.api.dependencies import SettingsDep
from amldo.core.exceptions import RetrievalError, LLMError, VectorStoreError
from amldo.utils.metrics import track_query_metrics

# Importar funções RAG
from amldo.rag.v1.tools import consultar_base_rag as rag_v1
from amldo.rag.v2.tools import consultar_base_rag as rag_v2
from amldo.rag.v3.tools import consultar_base_rag as rag_v3

router = APIRouter()


@router.post("/ask", response_model=QueryResponse, summary="Consulta RAG")
async def ask_question(payload: QueryRequest, settings: SettingsDep):
    """
    Consulta o sistema RAG com uma pergunta sobre licitações e compliance.

    **Parâmetros:**
    - question: Pergunta do usuário (obrigatório)
    - rag_version: Versão do RAG ("v1", "v2" ou "v3", opcional, default: "v2")

    **Versões RAG:**
    - **v1**: RAG básico com MMR search
    - **v2**: RAG avançado com MMR e contexto hierárquico (recomendado)
    - **v3**: RAG experimental com similarity search e contexto hierárquico

    **Exemplo de uso:**
    ```bash
    curl -X POST "http://localhost:8000/api/ask" \\
      -H "Content-Type: application/json" \\
      -d '{"question": "Qual é o limite para dispensa?", "rag_version": "v2"}'
    ```

    **Retorna:**
    - answer: Resposta gerada pelo LLM baseada no contexto recuperado
    - rag_version: Versão do RAG utilizada
    - question: Pergunta original
    - response_time_ms: Tempo de resposta em milissegundos
    """
    question = payload.question.strip()
    rag_version = payload.rag_version or settings.default_rag_version

    if not question:
        raise HTTPException(status_code=400, detail="Pergunta vazia")

    # Selecionar função RAG baseada na versão
    rag_functions = {"v1": rag_v1, "v2": rag_v2, "v3": rag_v3}

    if rag_version not in rag_functions:
        raise HTTPException(
            status_code=400, detail=f"Versão RAG inválida: {rag_version}. Use 'v1', 'v2' ou 'v3'"
        )

    try:
        start_time = time.time()
        answer = rag_functions[rag_version](question)
        response_time_ms = (time.time() - start_time) * 1000

        # Registrar métrica de sucesso
        track_query_metrics(
            rag_version=rag_version,
            question=question,
            response_time=response_time_ms,
            success=True,
        )

        return QueryResponse(
            answer=answer,
            rag_version=rag_version,
            question=question,
            response_time_ms=round(response_time_ms, 2),
        )

    except (RetrievalError, VectorStoreError) as e:
        # Registrar métrica de falha
        track_query_metrics(
            rag_version=rag_version,
            question=question,
            response_time=0,
            success=False,
            error_message=f"Retrieval error: {str(e)}",
        )
        raise HTTPException(
            status_code=500, detail=f"Erro ao recuperar documentos: {str(e)}"
        )
    except LLMError as e:
        # Registrar métrica de falha
        track_query_metrics(
            rag_version=rag_version,
            question=question,
            response_time=0,
            success=False,
            error_message=f"LLM error: {str(e)}",
        )
        raise HTTPException(status_code=500, detail=f"Erro no LLM: {str(e)}")
    except Exception as e:
        # Registrar métrica de falha
        track_query_metrics(
            rag_version=rag_version,
            question=question,
            response_time=0,
            success=False,
            error_message=str(e),
        )
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/health", summary="Health Check")
async def health_check():
    """
    Verifica se a API está funcionando.

    **Retorna:**
    - status: "ok" se a API estiver funcionando
    """
    return JSONResponse(content={"status": "ok", "service": "AMLDO API"})
