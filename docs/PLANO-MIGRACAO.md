# Plano de Migração e Integração AMLDO v0.2.0 + AMLDO_W

**Data de Criação:** 2025-11-15
**Versão Alvo:** AMLDO v0.3.0
**Status:** Em Planejamento

---

## 📋 Sumário Executivo

Este documento detalha o plano de migração para integrar funcionalidades do AMLDO_W na estrutura moderna do AMLDO v0.2.0, mantendo duas aplicações web (Streamlit + FastAPI) e eliminando duplicações.

### Objetivos

1. ✅ Manter AMLDO v0.2.0 como base estrutural
2. ✅ Integrar FastAPI do AMLDO_W em `src/amldo/interfaces/api/`
3. ✅ Adicionar RAG v3 (similarity search) como opção configurável
4. ✅ Eliminar duplicações de código
5. ✅ Manter compatibilidade com Google ADK e Streamlit
6. ✅ Adicionar processamento dinâmico de PDFs via API
7. ✅ Simplificar estrutura de pastas

---

## 🗂️ Estrutura Alvo (v0.3.0)

```
AMLDO/
├── src/amldo/                      # Pacote principal (mantém)
│   ├── core/
│   │   ├── config.py               # ✨ ATUALIZAR: adicionar rag_v3_*
│   │   └── exceptions.py
│   │
│   ├── rag/
│   │   ├── v1/                     # ✅ Manter
│   │   ├── v2/                     # ✅ Manter
│   │   └── v3/                     # ✨ NOVO: migrar de AMLDO_W/rag_v3_sim
│   │       ├── __init__.py
│   │       ├── agent.py
│   │       └── tools.py
│   │
│   ├── pipeline/                   # ✅ Manter
│   │   ├── embeddings.py
│   │   ├── ingestion/
│   │   ├── structure/
│   │   └── indexer/
│   │
│   ├── agents/                     # ✅ Manter (CrewAI)
│   │   ├── base_agent.py
│   │   ├── orchestrator.py
│   │   └── specialized/
│   │
│   ├── interfaces/
│   │   ├── adk/                    # ✅ Manter
│   │   │   ├── __init__.py
│   │   │   └── agent_loader.py
│   │   │
│   │   ├── streamlit/              # ✅ Manter
│   │   │   ├── app.py
│   │   │   └── pages/
│   │   │       ├── 01_Pipeline.py
│   │   │       └── 02_RAG_Query.py
│   │   │
│   │   └── api/                    # ✨ NOVO: migrar webapp do AMLDO_W
│   │       ├── __init__.py
│   │       ├── main.py             # FastAPI app
│   │       ├── dependencies.py     # Shared dependencies
│   │       ├── routers/            # Organização modular
│   │       │   ├── __init__.py
│   │       │   ├── query.py        # /api/ask
│   │       │   ├── upload.py       # /api/upload, /api/process
│   │       │   └── metrics.py      # /api/metrics/*
│   │       ├── models/             # Pydantic models
│   │       │   ├── __init__.py
│   │       │   ├── request.py
│   │       │   └── response.py
│   │       ├── templates/          # HTML templates (Jinja2)
│   │       │   ├── index.html
│   │       │   ├── chat.html
│   │       │   └── process.html
│   │       └── static/             # CSS, JS, imagens
│   │           ├── css/
│   │           ├── js/
│   │           └── img/
│   │
│   └── utils/
│       ├── logger.py
│       └── metrics.py              # ✨ NOVO: sistema de métricas
│
├── tests/
│   ├── unit/
│   │   ├── test_rag_v3.py          # ✨ NOVO
│   │   └── test_api_endpoints.py  # ✨ NOVO
│   └── integration/
│       └── test_api_integration.py # ✨ NOVO
│
├── data/                           # ✅ Manter estrutura atual
│   ├── raw/
│   ├── split_docs/
│   ├── processed/
│   └── vector_db/
│
├── notebooks/                      # ✅ Manter
│
├── docs/                           # ✅ Manter + adicionar
│   ├── 09-comparacao-versoes.md   # ✅ Criado
│   ├── 10-api-fastapi.md          # ✨ NOVO
│   └── PLANO-MIGRACAO.md          # ✨ Este arquivo
│
├── AMLDO_W/                        # ⚠️ DEPRECAR após migração
│   └── AMLDO/                      # Fonte de migração
│
├── pyproject.toml                  # ✨ ATUALIZAR: adicionar fastapi
├── requirements/
│   ├── base.txt                    # ✅ Manter
│   ├── api.txt                     # ✨ NOVO: fastapi, jinja2, python-multipart
│   ├── streamlit.txt               # ✅ Manter
│   └── dev.txt                     # ✅ Manter
│
└── README.md                       # ✨ ATUALIZAR
```

---

## 🎯 Fases de Migração

### Fase 1: Preparação e Análise (CONCLUÍDO ✅)

**Duração:** 1 dia
**Status:** ✅ Completo

- [x] Analisar estrutura AMLDO_W
- [x] Identificar duplicações
- [x] Criar documento comparativo (docs/09-comparacao-versoes.md)
- [x] Criar este plano de migração

### Fase 2: Integração RAG v3 (2-3 dias)

**Status:** 🔄 Próxima

#### Tarefas

1. **Criar estrutura RAG v3**
   ```bash
   mkdir -p src/amldo/rag/v3
   touch src/amldo/rag/v3/{__init__.py,agent.py,tools.py}
   ```

2. **Migrar código de AMLDO_W/rag_v3_sim/**
   - Copiar `tools.py` e adaptar para usar `settings`
   - Copiar `agent.py` e integrar com Google ADK
   - Criar `__init__.py` com exports

3. **Atualizar configuração**
   ```python
   # src/amldo/core/config.py
   class Settings(BaseSettings):
       # ... existentes

       # RAG v3 (similarity search)
       rag_v3_enabled: bool = True
       rag_v3_search_type: str = "similarity"  # ou "mmr"
       rag_v3_k: int = 12
   ```

4. **Criar testes**
   ```bash
   # tests/unit/test_rag_v3.py
   def test_rag_v3_similarity_search()
   def test_rag_v3_vs_v2_comparison()
   ```

5. **Atualizar ADK**
   ```python
   # src/amldo/interfaces/adk/agent_loader.py
   # Registrar rag_v3 como agente disponível
   ```

**Resultado Esperado:** RAG v3 funcionando via `adk web` com seleção `rag_v3`

---

### Fase 3: Integração FastAPI (3-5 dias)

**Status:** 🔄 Após Fase 2

#### 3.1 Estrutura Base

```bash
mkdir -p src/amldo/interfaces/api/{routers,models,templates,static/{css,js,img}}
```

#### 3.2 Arquivos Principais

**a) src/amldo/interfaces/api/main.py**
```python
"""
FastAPI Application for AMLDO
Migrado de AMLDO_W/webapp/main.py com melhorias
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from amldo.core.config import settings
from amldo.interfaces.api.routers import query, upload, metrics

app = FastAPI(
    title="AMLDO API",
    description="API REST para sistema RAG de Licitações",
    version="0.3.0"
)

# Templates e arquivos estáticos
templates = Jinja2Templates(directory="src/amldo/interfaces/api/templates")
app.mount("/static", StaticFiles(directory="src/amldo/interfaces/api/static"), name="static")

# Routers
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])

# Página inicial
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

**b) src/amldo/interfaces/api/routers/query.py**
```python
"""Router para consultas RAG"""
from fastapi import APIRouter, HTTPException
from amldo.rag.v1.tools import consultar_base_rag as rag_v1
from amldo.rag.v2.tools import consultar_base_rag as rag_v2
from amldo.rag.v3.tools import consultar_base_rag as rag_v3
from amldo.core.config import settings
from amldo.interfaces.api.models.request import QueryRequest
from amldo.interfaces.api.models.response import QueryResponse

router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(payload: QueryRequest):
    """
    Consulta RAG com seleção de versão

    Exemplo:
        POST /api/ask
        {
            "question": "Qual o limite para dispensa?",
            "rag_version": "v2"  # opcional, default: v2
        }
    """
    question = payload.question.strip()
    rag_version = payload.rag_version or settings.default_rag_version

    if not question:
        raise HTTPException(status_code=400, detail="Pergunta vazia")

    try:
        if rag_version == "v1":
            answer = rag_v1(question)
        elif rag_version == "v2":
            answer = rag_v2(question)
        elif rag_version == "v3":
            answer = rag_v3(question)
        else:
            raise HTTPException(status_code=400, detail=f"Versão RAG inválida: {rag_version}")

        return QueryResponse(
            answer=answer,
            rag_version=rag_version,
            question=question
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**c) src/amldo/interfaces/api/routers/upload.py**
```python
"""Router para upload e processamento de documentos"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import os
from pathlib import Path

from amldo.core.config import settings
from amldo.pipeline.ingestion.ingest import process_pdf
from amldo.pipeline.indexer.indexer import update_faiss_index
from amldo.interfaces.api.models.response import UploadResponse, ProcessResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload de múltiplos PDFs"""
    saved = []
    failed = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            failed.append({"file": file.filename, "error": "Tipo inválido"})
            continue

        # Salvar em data/raw/
        dest = settings.raw_data_path / file.filename

        # Evitar sobrescrever
        counter = 1
        while dest.exists():
            stem = dest.stem
            dest = settings.raw_data_path / f"{stem}_{counter}.pdf"
            counter += 1

        content = await file.read()
        dest.write_bytes(content)
        saved.append(dest.name)

    return UploadResponse(saved=saved, failed=failed)

@router.post("/process", response_model=ProcessResponse)
async def process_documents():
    """
    Processa PDFs em data/raw/ e atualiza índice FAISS

    Workflow:
    1. Lê todos PDFs em data/raw/
    2. Processa com pipeline/ingestion
    3. Atualiza índice FAISS
    4. Retorna métricas
    """
    from amldo.utils.metrics import track_processing_metrics

    raw_path = settings.raw_data_path
    pdf_files = list(raw_path.glob("*.pdf"))

    if not pdf_files:
        raise HTTPException(status_code=404, detail="Nenhum PDF encontrado")

    try:
        total_chunks = 0
        processed_files = []

        for pdf_path in pdf_files:
            # Processar PDF
            articles = process_pdf(str(pdf_path))
            chunks = len(articles)
            total_chunks += chunks

            # Atualizar índice FAISS
            update_faiss_index(articles)

            processed_files.append({
                "file": pdf_path.name,
                "chunks": chunks
            })

        # Salvar métricas
        track_processing_metrics(len(pdf_files), total_chunks)

        return ProcessResponse(
            processed=len(pdf_files),
            total_chunks=total_chunks,
            files=processed_files
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar: {str(e)}")
```

**d) src/amldo/interfaces/api/models/request.py**
```python
"""Modelos Pydantic para requisições"""
from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Pergunta do usuário")
    rag_version: Optional[str] = Field("v2", regex="^(v1|v2|v3)$", description="Versão do RAG")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Qual é o limite de valor para dispensa de licitação?",
                "rag_version": "v2"
            }
        }
```

**e) src/amldo/interfaces/api/models/response.py**
```python
"""Modelos Pydantic para respostas"""
from pydantic import BaseModel
from typing import List, Dict, Any

class QueryResponse(BaseModel):
    answer: str
    rag_version: str
    question: str

class UploadResponse(BaseModel):
    saved: List[str]
    failed: List[Dict[str, str]]

class ProcessResponse(BaseModel):
    processed: int
    total_chunks: int
    files: List[Dict[str, Any]]
```

#### 3.3 Templates HTML

Migrar templates de `AMLDO_W/webapp/templates/` para `src/amldo/interfaces/api/templates/`

**Arquivos a migrar:**
- `index.html`
- `chat.html`
- `process.html`

**Melhorias a fazer:**
- Adicionar seletor de versão RAG (v1/v2/v3)
- Melhorar UI com Tailwind CSS ou Bootstrap
- Adicionar feedback visual de processamento

#### 3.4 Dependências

**Adicionar em requirements/api.txt:**
```txt
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.9
jinja2>=3.1.0
```

**Atualizar pyproject.toml:**
```toml
[project.optional-dependencies]
api = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "python-multipart>=0.0.9",
    "jinja2>=3.1.0",
]
```

#### 3.5 Scripts de Execução

**Criar: src/amldo/interfaces/api/run.py**
```python
"""Script para rodar FastAPI"""
import uvicorn
from amldo.core.config import settings

def main():
    uvicorn.run(
        "amldo.interfaces.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

if __name__ == "__main__":
    main()
```

**Adicionar script em pyproject.toml:**
```toml
[project.scripts]
amldo-api = "amldo.interfaces.api.run:main"
amldo-streamlit = "amldo.interfaces.streamlit.app:main"
```

**Resultado Esperado:** API funcionando em `http://localhost:8000`

---

### Fase 4: Sistema de Métricas (1-2 dias)

**Status:** 🔄 Após Fase 3

#### 4.1 Criar módulo de métricas

**src/amldo/utils/metrics.py**
```python
"""
Sistema de métricas para AMLDO
Substitui JSON por SQLite
"""
from datetime import datetime
from pathlib import Path
import sqlite3
from typing import List, Dict, Any

from amldo.core.config import settings

class MetricsManager:
    def __init__(self):
        self.db_path = settings.data_path / "metrics" / "metrics.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Inicializa banco de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de processamento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                files_processed INTEGER,
                total_chunks INTEGER,
                duration_seconds REAL
            )
        """)

        # Tabela de consultas RAG
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rag_version TEXT,
                question TEXT,
                response_time_ms REAL
            )
        """)

        conn.commit()
        conn.close()

    def track_processing(self, files: int, chunks: int, duration: float = 0):
        """Registra processamento de documentos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO processing_history (files_processed, total_chunks, duration_seconds) VALUES (?, ?, ?)",
            (files, chunks, duration)
        )
        conn.commit()
        conn.close()

    def track_query(self, rag_version: str, question: str, response_time: float):
        """Registra consulta RAG"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO query_history (rag_version, question, response_time_ms) VALUES (?, ?, ?)",
            (rag_version, question, response_time)
        )
        conn.commit()
        conn.close()

    def get_processing_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna histórico de processamento"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM processing_history ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total de consultas por versão RAG
        cursor.execute("""
            SELECT rag_version, COUNT(*) as count, AVG(response_time_ms) as avg_time
            FROM query_history
            GROUP BY rag_version
        """)
        rag_stats = cursor.fetchall()

        # Total de documentos processados
        cursor.execute("SELECT SUM(files_processed), SUM(total_chunks) FROM processing_history")
        total_files, total_chunks = cursor.fetchone()

        conn.close()

        return {
            "rag_stats": [
                {"version": r[0], "queries": r[1], "avg_response_time_ms": r[2]}
                for r in rag_stats
            ],
            "total_files_processed": total_files or 0,
            "total_chunks_indexed": total_chunks or 0
        }

# Singleton
_metrics = None

def get_metrics_manager() -> MetricsManager:
    global _metrics
    if _metrics is None:
        _metrics = MetricsManager()
    return _metrics

def track_processing_metrics(files: int, chunks: int, duration: float = 0):
    get_metrics_manager().track_processing(files, chunks, duration)

def track_query_metrics(rag_version: str, question: str, response_time: float):
    get_metrics_manager().track_query(rag_version, question, response_time)
```

#### 4.2 Integrar métricas na API

```python
# src/amldo/interfaces/api/routers/metrics.py
from fastapi import APIRouter
from amldo.utils.metrics import get_metrics_manager

router = APIRouter()

@router.get("/stats")
async def get_statistics():
    """Retorna estatísticas gerais"""
    manager = get_metrics_manager()
    return manager.get_stats()

@router.get("/processing-history")
async def get_processing_history(limit: int = 100):
    """Retorna histórico de processamento"""
    manager = get_metrics_manager()
    return {"history": manager.get_processing_history(limit)}
```

**Resultado Esperado:** Métricas em SQLite acessíveis via `/api/metrics/stats`

---

### Fase 5: Testes e Validação (2-3 dias)

**Status:** 🔄 Após Fase 4

#### 5.1 Testes Unitários

**tests/unit/test_rag_v3.py**
```python
import pytest
from amldo.rag.v3.tools import consultar_base_rag, _get_retriever

def test_rag_v3_retriever():
    """Testa criação do retriever RAG v3"""
    retriever = _get_retriever(search_type="similarity", k=12)
    assert retriever is not None

def test_rag_v3_consulta():
    """Testa consulta básica RAG v3"""
    resposta = consultar_base_rag("Qual o limite de dispensa?")
    assert isinstance(resposta, str)
    assert len(resposta) > 0
```

**tests/unit/test_api_endpoints.py**
```python
from fastapi.testclient import TestClient
from amldo.interfaces.api.main import app

client = TestClient(app)

def test_api_root():
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200

def test_api_ask():
    """Testa endpoint /api/ask"""
    response = client.post(
        "/api/ask",
        json={"question": "Teste", "rag_version": "v2"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["rag_version"] == "v2"

def test_api_ask_invalid_version():
    """Testa versão RAG inválida"""
    response = client.post(
        "/api/ask",
        json={"question": "Teste", "rag_version": "v99"}
    )
    assert response.status_code == 400
```

#### 5.2 Testes de Integração

**tests/integration/test_api_integration.py**
```python
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from amldo.interfaces.api.main import app

client = TestClient(app)

def test_full_workflow_upload_process_query():
    """Testa workflow completo: upload → process → query"""
    # 1. Upload
    test_pdf = Path("tests/fixtures/test_document.pdf")
    with open(test_pdf, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"files": ("test.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    assert len(response.json()["saved"]) > 0

    # 2. Process
    response = client.post("/api/process")
    assert response.status_code == 200
    assert response.json()["processed"] > 0

    # 3. Query
    response = client.post(
        "/api/ask",
        json={"question": "Resumo do documento", "rag_version": "v2"}
    )
    assert response.status_code == 200
```

#### 5.3 Executar Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=src/amldo --cov-report=html

# Apenas novos testes
pytest tests/unit/test_rag_v3.py tests/unit/test_api_endpoints.py

# Testes de integração
pytest tests/integration/
```

**Resultado Esperado:** Cobertura de testes > 80% para novos módulos

---

### Fase 6: Documentação e Finalização (1-2 dias)

**Status:** 🔄 Após Fase 5

#### 6.1 Documentação da API

**Criar: docs/10-api-fastapi.md**

```markdown
# API REST FastAPI - AMLDO v0.3.0

## Visão Geral

A API REST permite integração do AMLDO com outros sistemas via HTTP.

## Endpoints

### POST /api/ask
Consulta RAG

**Request:**
{
  "question": "Pergunta aqui",
  "rag_version": "v2"  // v1, v2 ou v3
}

**Response:**
{
  "answer": "Resposta...",
  "rag_version": "v2",
  "question": "Pergunta..."
}

[... continuar documentação ...]
```

#### 6.2 Atualizar README

```markdown
# AMLDO v0.3.0

## Interfaces Disponíveis

### 1. Google ADK (CLI)
```bash
adk web  # http://localhost:8080
```

### 2. Streamlit (Web)
```bash
streamlit run src/amldo/interfaces/streamlit/app.py  # http://localhost:8501
```

### 3. FastAPI (API REST) ✨ NOVO
```bash
amldo-api  # http://localhost:8000
# ou
uvicorn amldo.interfaces.api.main:app --reload
```

## Novidades v0.3.0

- ✨ API REST FastAPI completa
- ✨ RAG v3 com similarity search
- ✨ Processamento dinâmico de PDFs via API
- ✨ Sistema de métricas com SQLite
- ✨ Documentação API REST
```

#### 6.3 Atualizar CLAUDE.md

Adicionar seções sobre:
- Nova interface FastAPI
- RAG v3
- Sistema de métricas
- Novos comandos CLI

**Resultado Esperado:** Documentação completa e atualizada

---

### Fase 7: Limpeza e Deprecação (1 dia)

**Status:** 🔄 Após Fase 6

#### 7.1 Remover Duplicações

**Arquivos duplicados na raiz (fora de src/):**
- ❌ `rag_v1/` (raiz) → usar `src/amldo/rag/v1/`
- ❌ `rag_v2/` (raiz) → usar `src/amldo/rag/v2/`
- ❌ `LicitAI/backend/agents/` → usar `src/amldo/agents/`

**Ações:**
```bash
# Mover para backup antes de deletar
mkdir -p backup/deprecated
mv rag_v1 backup/deprecated/
mv rag_v2 backup/deprecated/
mv LicitAI/backend backup/deprecated/
```

#### 7.2 Deprecar AMLDO_W

**Opções:**
1. **Manter como referência** (recomendado)
   ```bash
   mv AMLDO_W AMLDO_W_DEPRECATED
   echo "⚠️ DEPRECATED: Migrado para src/amldo/interfaces/api/" > AMLDO_W_DEPRECATED/README.md
   ```

2. **Mover para backup**
   ```bash
   mv AMLDO_W backup/AMLDO_W_original
   ```

3. **Deletar** (após confirmar migração completa)
   ```bash
   rm -rf AMLDO_W
   ```

**Recomendação:** Opção 1 (manter como referência por 1-2 meses)

#### 7.3 Limpar arquivos não usados

```bash
# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Limpar notebooks checkpoint
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
```

**Resultado Esperado:** Estrutura limpa sem duplicações

---

## 📊 Cronograma

| Fase | Duração | Início | Fim | Status |
|------|---------|--------|-----|--------|
| 1. Preparação | 1 dia | 2025-11-15 | 2025-11-15 | ✅ Completo |
| 2. RAG v3 | 2-3 dias | 2025-11-16 | 2025-11-18 | 🔄 Próxima |
| 3. FastAPI | 3-5 dias | 2025-11-19 | 2025-11-23 | ⏳ Pendente |
| 4. Métricas | 1-2 dias | 2025-11-24 | 2025-11-25 | ⏳ Pendente |
| 5. Testes | 2-3 dias | 2025-11-26 | 2025-11-28 | ⏳ Pendente |
| 6. Documentação | 1-2 dias | 2025-11-29 | 2025-11-30 | ⏳ Pendente |
| 7. Limpeza | 1 dia | 2025-12-01 | 2025-12-01 | ⏳ Pendente |

**Total Estimado:** 11-17 dias úteis (~2-3 semanas)

---

## ✅ Checklist de Migração

### Fase 2: RAG v3
- [ ] Criar estrutura `src/amldo/rag/v3/`
- [ ] Migrar `tools.py` do AMLDO_W
- [ ] Migrar `agent.py` do AMLDO_W
- [ ] Atualizar `core/config.py` com settings de v3
- [ ] Criar testes `test_rag_v3.py`
- [ ] Registrar agente no ADK
- [ ] Testar via `adk web`

### Fase 3: FastAPI
- [ ] Criar estrutura `src/amldo/interfaces/api/`
- [ ] Implementar `main.py`
- [ ] Implementar routers (query, upload, metrics)
- [ ] Criar models Pydantic
- [ ] Migrar templates HTML
- [ ] Migrar arquivos estáticos (CSS, JS)
- [ ] Adicionar dependências em `requirements/api.txt`
- [ ] Criar script `amldo-api`
- [ ] Testar todos endpoints
- [ ] Documentar API com OpenAPI/Swagger

### Fase 4: Métricas
- [ ] Criar `src/amldo/utils/metrics.py`
- [ ] Implementar `MetricsManager` com SQLite
- [ ] Integrar no router `/api/metrics`
- [ ] Adicionar tracking em `/api/ask`
- [ ] Adicionar tracking em `/api/process`
- [ ] Testar persistência de métricas
- [ ] Criar dashboard básico (opcional)

### Fase 5: Testes
- [ ] Criar `tests/unit/test_rag_v3.py`
- [ ] Criar `tests/unit/test_api_endpoints.py`
- [ ] Criar `tests/integration/test_api_integration.py`
- [ ] Executar todos testes
- [ ] Gerar relatório de coverage
- [ ] Coverage > 80% para novos módulos

### Fase 6: Documentação
- [ ] Criar `docs/10-api-fastapi.md`
- [ ] Atualizar README.md
- [ ] Atualizar CLAUDE.md
- [ ] Atualizar docs/06-estado-atual.md
- [ ] Criar exemplos de uso da API
- [ ] Documentar mudanças de v0.2 → v0.3

### Fase 7: Limpeza
- [ ] Remover `rag_v1/` e `rag_v2/` da raiz
- [ ] Remover `LicitAI/backend/agents/`
- [ ] Deprecar `AMLDO_W/`
- [ ] Limpar cache e checkpoints
- [ ] Validar estrutura final
- [ ] Commit final de migração

---

## 🚨 Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Quebra de compatibilidade ADK | Média | Alto | Testes extensivos, manter v1 e v2 funcionais |
| Performance da API | Baixa | Médio | Benchmark, usar async onde possível |
| Bugs em RAG v3 | Média | Médio | Testes comparativos v2 vs v3 |
| Perda de funcionalidades AMLDO_W | Baixa | Alto | Checklist detalhado de migração |
| Dependências conflitantes | Baixa | Médio | Usar requirements separados |
| Documentação incompleta | Média | Baixo | Revisão de documentação em Fase 6 |

---

## 🎯 Critérios de Sucesso

1. ✅ **RAG v3 funcionando** via ADK e API
2. ✅ **API REST completa** com todos endpoints do AMLDO_W
3. ✅ **Duas aplicações web** (Streamlit + FastAPI) funcionando
4. ✅ **Testes > 80%** de cobertura para novos módulos
5. ✅ **Documentação completa** da API
6. ✅ **Zero duplicações** de código
7. ✅ **Performance mantida** ou melhorada vs v0.2.0
8. ✅ **Deploy funcional** via Docker

---

## 📞 Próximos Passos

1. **Revisar e aprovar** este plano de migração
2. **Iniciar Fase 2** (RAG v3)
3. **Executar checklist** fase por fase
4. **Reportar progresso** semanalmente
5. **Ajustar cronograma** conforme necessário

---

**Responsável:** Equipe AMLDO
**Revisão:** Semanal
**Próxima revisão:** 2025-11-22
