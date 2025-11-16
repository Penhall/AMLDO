# Comparação: AMLDO v0.2.0 vs AMLDO_W

**Última atualização:** 2025-11-15
**Autor:** Análise Técnica Comparativa
**Objetivo:** Documentar diferenças entre a versão oficial (v0.2.0) e a variante AMLDO_W

---

## 📋 Sumário Executivo

Este documento compara duas versões do projeto AMLDO:

- **AMLDO v0.2.0** (Principal): Versão oficialmente reestruturada com arquitetura moderna
- **AMLDO_W** (Derivada): Versão experimental com foco em interface web FastAPI

### Principais Diferenças

| Aspecto | AMLDO v0.2.0 | AMLDO_W |
|---------|-------------|---------|
| **Estrutura** | Pacote moderno `src/amldo/` | Estrutura flat com módulos raiz |
| **Interface Principal** | Google ADK + Streamlit | FastAPI Web App |
| **Configuração** | Pydantic Settings centralizado | Variáveis de ambiente diretas |
| **RAG Avançado** | v2 (contexto hierárquico) | v3_sim (similarity search) |
| **Pipeline** | Modular e extensível | Scripts notebook-based |
| **Testes** | Suite completa pytest | Não implementado |
| **Agentes** | CrewAI integrado | Não presente |
| **Deploy** | Docker, Cloud, systemd | Desenvolvimento local |

---

## 🏗️ Arquitetura e Estrutura

### AMLDO v0.2.0 — Arquitetura Moderna

```
AMLDO/
├── src/amldo/                      # Package principal (instalável)
│   ├── core/                       # Configuração centralizada
│   │   ├── config.py               # Pydantic Settings
│   │   └── exceptions.py           # Hierarquia de exceções
│   ├── rag/
│   │   ├── v1/                     # RAG básico
│   │   └── v2/                     # RAG hierárquico avançado
│   ├── pipeline/                   # Pipeline modular
│   │   ├── embeddings.py
│   │   ├── ingestion/
│   │   ├── structure/
│   │   └── indexer/
│   ├── agents/                     # Sistema CrewAI
│   │   └── specialized/
│   ├── interfaces/
│   │   ├── adk/                    # Google ADK
│   │   └── streamlit/              # Streamlit app
│   │       └── pages/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── pyproject.toml                  # Configuração moderna Python
├── setup.py
└── requirements/                   # Requirements organizados
    ├── base.txt
    ├── dev.txt
    ├── adk.txt
    └── streamlit.txt
```

**Características:**
- ✅ Estrutura de pacote Python moderna (`src/` layout)
- ✅ Instalável via `pip install -e .`
- ✅ Configuração centralizada com `pydantic-settings`
- ✅ Separação clara de responsabilidades
- ✅ Extensível e testável
- ✅ Seguindo PEP 517/518

### AMLDO_W — Estrutura Flat Experimental

```
AMLDO_W/AMLDO/
├── rag_v1/                         # RAG básico
│   ├── agent.py
│   ├── tools.py
│   └── __init__.py
├── rag_v2/                         # RAG v2 (similar ao principal)
│   ├── agent.py
│   └── tools.py
├── rag_v3_sim/                     # RAG v3 experimental (similarity)
│   ├── agent.py
│   └── tools.py
├── webapp/                         # FastAPI web application
│   ├── main.py
│   ├── templates/
│   └── static/
├── data/                           # Mesma estrutura de dados
│   ├── raw/
│   ├── split_docs/
│   ├── processed/
│   ├── vector_db/
│   └── metrics/                    # Métricas de embedding (novo)
├── get_v1_data.ipynb              # Notebook processamento
├── get_vectorial_bank_v1.ipynb    # Notebook indexação
├── order_rag_study.ipynb          # Análise experimental
├── requirements.txt               # Requirements flat
├── .env
└── README.md
```

**Características:**
- ✅ Estrutura simples e direta
- ✅ Foco em experimentação rápida
- ✅ Interface web personalizada (FastAPI)
- ✅ RAG v3 experimental
- ⚠️ Não é um pacote instalável
- ⚠️ Configuração via variáveis de ambiente diretas
- ⚠️ Sem testes automatizados

---

## 🔧 Configuração e Dependências

### AMLDO v0.2.0

**Gerenciamento de Configuração:**
```python
# src/amldo/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str
    embedding_model: str = "sentence-transformers/..."
    llm_model: str = "gemini-2.5-flash"
    search_k: int = 12
    search_type: str = "mmr"
    # ... muitos outros

    class Config:
        env_file = ".env"

settings = Settings()  # Singleton
```

**Vantagens:**
- ✅ Validação automática de tipos
- ✅ Valores padrão inteligentes
- ✅ Autocomplete IDE
- ✅ Fácil de testar
- ✅ Documentação via docstrings

**Dependências:**
```toml
# pyproject.toml
[project]
dependencies = [
    "langchain>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    # ...
]

[project.optional-dependencies]
adk = ["google-genai>=0.2.0"]
streamlit = ["streamlit>=1.28.0"]
agents = ["crewai>=0.1.0"]
dev = ["pytest>=7.4.0", "black>=23.0.0", ...]
```

### AMLDO_W

**Gerenciamento de Configuração:**
```python
# Diretamente nos módulos
from dotenv import load_dotenv
import os

load_dotenv()
# Uso direto: os.getenv("GOOGLE_API_KEY")
```

**Vantagens:**
- ✅ Simplicidade
- ✅ Menos overhead
- ⚠️ Sem validação
- ⚠️ Sem defaults centralizados

**Dependências:**
```txt
# requirements.txt (flat)
ipykernel==6.30.1
pandas==2.3.2
python-dotenv==1.0.1
google-cloud-aiplatform==1.122.0
langchain==1.0.2
sentence-transformers==5.1.2
faiss-cpu==1.12.0
google-adk==1.14.1
# Sem extras/dev separados
```

---

## 🤖 Sistemas RAG

### RAG v1 — Básico (Ambos)

**Implementação similar em ambas versões:**

```python
# Busca → Contexto → LLM → Resposta
def consultar_base_rag(pergunta: str) -> str:
    retriever = vector_db.as_retriever(search_type="mmr", k=12)
    # Contexto direto sem pós-processamento
    resposta = rag_chain.invoke(pergunta)
    return resposta
```

- 🟢 Ambas usam MMR search
- 🟢 Ambas retornam contexto direto
- 🟢 Performance similar

### RAG v2 — Hierárquico (Ambos, com diferenças)

**AMLDO v0.2.0:**
```python
# src/amldo/rag/v2/tools.py
def _get_retriever(...):
    return vector_db.as_retriever(
        search_type=settings.search_type,  # Configurável
        search_kwargs={
            "k": settings.search_k,
            "filter": {"artigo": {"$nin": ["artigo_0.txt"]}}
        }
    )

def get_pos_processed_context(df_resultados, df_art_0):
    # Hierarquia XML: <LEI> → <TITULO> → <CAPITULO> → <ARTIGO>
    # Injeta artigo_0 do CSV
    context = ''
    for law in df_cap['lei'].unique():
        context += f'\n\n<LEI {law}>\n'
        # ... processamento hierárquico complexo
    return context
```

**AMLDO_W (rag_v3_sim):**
```python
# rag_v3_sim/tools.py
SEARCH_TYPE = "similarity"  # Fixo (não MMR)

def _get_retriever(...):
    return vector_db.as_retriever(
        search_type="similarity",  # Hardcoded
        search_kwargs={
            "k": 12,
            "filter": {"artigo": {"$nin": ['artigo_0.txt']}}
        }
    )

# Mesma lógica de pós-processamento hierárquico
```

**Diferenças:**
- 🔴 AMLDO_W usa `similarity` search (não MMR)
- 🟢 AMLDO v0.2.0 é configurável via `settings`
- 🟢 Ambos implementam hierarquia XML
- 🟢 Ambos filtram artigo_0.txt

### RAG v3_sim — Experimental (AMLDO_W apenas)

**Exclusivo do AMLDO_W:**
- Teste de similarity search vs MMR
- Parâmetros fixos (não configuráveis)
- Objetivo: experimentação rápida

---

## 🖥️ Interfaces de Usuário

### AMLDO v0.2.0 — Múltiplas Interfaces

#### 1. Google ADK (CLI)
```bash
adk web
# → http://localhost:8080
# Agentes: rag_v1, rag_v2
```

**Características:**
- ✅ Interface conversacional
- ✅ Integração nativa com Gemini
- ✅ Histórico de conversas
- ✅ Fácil de usar

#### 2. Streamlit (Web)
```bash
streamlit run src/amldo/interfaces/streamlit/app.py
# → http://localhost:8501
```

**Páginas:**
- **Home**: Overview
- **Pipeline**: Upload e processamento de PDFs
- **RAG Query**: Consultas à base

**Características:**
- ✅ Interface gráfica moderna
- ✅ Upload de documentos
- ✅ Processamento visual
- ✅ Fácil deploy

#### 3. Scripts CLI
```bash
amldo-process --input file.pdf --output data/processed/
amldo-build-index --source artigos.jsonl --output vector_db/
```

### AMLDO_W — FastAPI Web App

```bash
uvicorn webapp.main:app --reload
# → http://localhost:8000
```

**Endpoints:**

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Página inicial |
| `/consulta` | GET | Interface de chat |
| `/processamento` | GET | Interface de processamento |
| `/api/ask` | POST | API de consulta RAG |
| `/api/upload` | POST | Upload de PDFs |
| `/api/process` | POST | Processar PDFs e atualizar índice |
| `/api/metrics/embedding_history` | GET | Histórico de embeddings |

**Características:**
- ✅ Interface web personalizada (Jinja2 templates)
- ✅ API REST completa
- ✅ Upload de múltiplos PDFs
- ✅ Processamento em tempo real
- ✅ Métricas de embedding tracking
- ✅ Fallback inteligente (se RAG v1 falhar, usa retrieval direto)
- ⚠️ Não tem interface ADK
- ⚠️ Templates HTML customizados (não incluídos no código analisado)

**Código de processamento (AMLDO_W):**
```python
@app.post("/api/process")
def api_process():
    # Processa PDFs da pasta raw/
    # Cria chunks com RecursiveCharacterTextSplitter
    # Atualiza FAISS index em tempo real
    # Salva métricas de embedding
    fallback_db.add_documents(new_docs)
    fallback_db.save_local("data/vector_db/v1_faiss_vector_db")
    # Tracking de chunks
    record = {"ts": datetime.utcnow().isoformat(), "chunks": total_chunks}
    # Salva em embedding_history.json
    return {"processed": len(pdf_paths), "chunks": len(new_docs)}
```

**Diferencial:**
- 🟢 **Processamento dinâmico**: Permite adicionar documentos via web sem reiniciar sistema
- 🟢 **Métricas**: Tracking de crescimento do índice FAISS
- 🟢 **API REST**: Fácil integração com outros sistemas

---

## 📦 Pipeline de Processamento

### AMLDO v0.2.0 — Pipeline Modular

**Estrutura:**
```
src/amldo/pipeline/
├── embeddings.py           # Gerenciador de embeddings
├── ingestion/
│   └── ingest.py          # PDF → texto normalizado
├── structure/
│   └── structure.py       # Texto → artigos estruturados
└── indexer/
    └── indexer.py         # Artigos → FAISS index
```

**Uso programático:**
```python
from amldo.pipeline.embeddings import EmbeddingManager
from amldo.pipeline.ingestion.ingest import process_pdf
from amldo.pipeline.indexer.indexer import build_faiss_index

# 1. Processar PDF
articles = process_pdf("path/to/lei.pdf")

# 2. Criar embeddings
em = EmbeddingManager()
embeddings = em.embed([a.text for a in articles])

# 3. Construir índice
build_faiss_index(articles, embeddings, output_path="vector_db/")
```

**Uso via CLI:**
```bash
amldo-process --input data/raw/lei.pdf --output data/processed/
amldo-build-index --source data/processed/artigos.jsonl --output data/vector_db/
```

**Características:**
- ✅ Modular e testável
- ✅ Reutilizável
- ✅ CLI + API programática
- ✅ Tratamento de erros robusto

### AMLDO_W — Pipeline Notebook-Based

**Notebooks:**
1. **get_v1_data.ipynb**: Processamento de PDFs → artigos estruturados
2. **get_vectorial_bank_v1.ipynb**: Criação do índice FAISS
3. **order_rag_study.ipynb**: Análise e experimentação

**Características:**
- ✅ Interativo e visual
- ✅ Fácil experimentação
- ✅ Análise exploratória
- ⚠️ Não reutilizável programaticamente
- ⚠️ Difícil de versionar
- ⚠️ Não automatizável

**Diferencial (FastAPI `/api/process`):**
- 🟢 Processamento via API REST
- 🟢 Upload + processamento em uma única operação
- 🟢 Atualização dinâmica do índice FAISS

---

## 🧪 Testes e Qualidade de Código

### AMLDO v0.2.0

**Suite completa:**
```
tests/
├── unit/
│   ├── test_config.py          # Testes de configuração
│   ├── test_ingestion.py       # Testes de ingestão
│   ├── test_structure.py       # Testes de estruturação
│   └── test_indexer.py         # Testes de indexação
├── integration/
│   └── test_pipeline.py        # Testes end-to-end
└── conftest.py                 # Fixtures compartilhadas
```

**Execução:**
```bash
pytest                          # Todos os testes
pytest --cov=src/amldo         # Com coverage
pytest tests/unit/             # Apenas unit
pytest -v                      # Verbose
```

**Ferramentas de qualidade:**
- ✅ **Black**: Formatação automática
- ✅ **Ruff**: Linting rápido
- ✅ **mypy**: Type checking
- ✅ **pre-commit**: Hooks automáticos
- ✅ **pytest**: Framework de testes

**Configuração (pyproject.toml):**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-v", "--cov=src/amldo"]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
```

### AMLDO_W

**Testes:**
- ❌ Não implementado
- ❌ Sem pytest
- ❌ Sem coverage
- ❌ Sem linting configurado
- ❌ Sem pre-commit hooks

**Qualidade de código:**
- ⚠️ Código funcional mas não testado
- ⚠️ Sem garantias de regressão
- ⚠️ Validação manual apenas

---

## 🤝 Sistema Multi-Agente (CrewAI)

### AMLDO v0.2.0 — CrewAI Integrado

**Estrutura:**
```
src/amldo/agents/
├── base_agent.py
├── orchestrator.py
└── specialized/
    ├── ingestion_agent.py
    ├── structuring_agent.py
    ├── indexing_agent.py
    ├── compliance_agent.py
    ├── validation_agent.py
    └── company_docs_agent.py
```

**Uso:**
```python
from amldo.agents.orchestrator import build_all_agents

agents = build_all_agents()
compliance_agent = agents["compliance"]
validation_agent = agents["validation"]
```

**Status:** Integrado mas não totalmente conectado ao pipeline principal.

### AMLDO_W

**Sistema multi-agente:**
- ❌ Não implementado
- ❌ Sem CrewAI
- ⚠️ Foco em RAG single-agent

---

## 🚀 Deploy e Produção

### AMLDO v0.2.0

**Opções de deploy:**

1. **Docker**
   ```dockerfile
   FROM python:3.12-slim
   # ... instalação e configuração
   CMD ["streamlit", "run", "src/amldo/interfaces/streamlit/app.py"]
   ```

2. **Docker Compose**
   ```yaml
   services:
     streamlit:
       build: .
       ports: ["8501:8501"]
     adk:
       build: .
       command: ["adk", "web"]
   ```

3. **Cloud Platforms**
   - Google Cloud Run
   - AWS ECS/Fargate
   - Azure Container Apps

4. **Systemd Service**
   ```ini
   [Service]
   ExecStart=/path/to/venv/bin/streamlit run app.py
   ```

**Documentação:**
- ✅ Guia completo de deploy em `README.md`
- ✅ Exemplos de Dockerfile
- ✅ Docker Compose pronto
- ✅ Configurações Nginx
- ✅ Checklist de produção

### AMLDO_W

**Deploy:**
```bash
# Desenvolvimento local
uvicorn webapp.main:app --reload

# Produção (manual)
uvicorn webapp.main:app --host 0.0.0.0 --port 8000
```

**Características:**
- ✅ FastAPI é production-ready
- ⚠️ Sem documentação de deploy
- ⚠️ Sem Dockerfile
- ⚠️ Sem configuração de produção
- ⚠️ Métricas em arquivos JSON (não escalável)

**Recomendações para produção:**
```bash
# Usar gunicorn + uvicorn workers
gunicorn webapp.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 📊 Comparação de Funcionalidades

| Funcionalidade | AMLDO v0.2.0 | AMLDO_W | Comentários |
|----------------|--------------|---------|-------------|
| **RAG v1 Básico** | ✅ | ✅ | Similar em ambos |
| **RAG v2 Hierárquico** | ✅ (MMR) | ✅ (similarity) | Diferença em search_type |
| **RAG v3 Experimental** | ❌ | ✅ | Apenas AMLDO_W |
| **Google ADK Interface** | ✅ | ❌ | Apenas v0.2.0 |
| **Streamlit Interface** | ✅ | ❌ | Apenas v0.2.0 |
| **FastAPI Web App** | ❌ | ✅ | Apenas AMLDO_W |
| **API REST** | ❌ | ✅ | AMLDO_W tem API completa |
| **Upload de PDFs Web** | ✅ (Streamlit) | ✅ (FastAPI) | Ambos permitem |
| **Processamento Dinâmico** | ⚠️ | ✅ | AMLDO_W atualiza índice em runtime |
| **Métricas de Embedding** | ❌ | ✅ | AMLDO_W tracking JSON |
| **Pipeline Modular** | ✅ | ❌ | v0.2.0 mais estruturado |
| **CLI Scripts** | ✅ | ❌ | v0.2.0 tem `amldo-*` commands |
| **Testes Automatizados** | ✅ | ❌ | v0.2.0 pytest completo |
| **Configuração Centralizada** | ✅ | ⚠️ | v0.2.0 pydantic-settings |
| **Sistema Multi-Agente** | ✅ | ❌ | v0.2.0 CrewAI |
| **Documentação** | ✅✅ | ⚠️ | v0.2.0 docs/ completa |
| **Docker/Deploy** | ✅ | ⚠️ | v0.2.0 production-ready |
| **Instalável (pip)** | ✅ | ❌ | v0.2.0 é pacote Python |

**Legenda:**
- ✅ Implementado e funcional
- ✅✅ Implementado com excelência
- ⚠️ Parcialmente implementado ou básico
- ❌ Não implementado

---

## 💡 Pontos Fortes de Cada Versão

### AMLDO v0.2.0 — Produção e Escala

**Excelente para:**
- ✅ **Produção**: Pronto para deploy em cloud
- ✅ **Manutenibilidade**: Código testado e bem estruturado
- ✅ **Escalabilidade**: Arquitetura modular e extensível
- ✅ **Colaboração**: Múltiplos desenvolvedores
- ✅ **Documentação**: Guias completos
- ✅ **Longo prazo**: Evoluir e adicionar features

**Casos de uso:**
- Projeto de longo prazo
- Equipe de desenvolvimento
- Deploy em produção
- Integração com outros sistemas
- Necessidade de testes e CI/CD

### AMLDO_W — Experimentação e Prototipagem

**Excelente para:**
- ✅ **Rapidez**: Prototipar features rapidamente
- ✅ **Experimentação**: Testar RAG v3, similarity search
- ✅ **API REST**: Interface web personalizada
- ✅ **Processamento Dinâmico**: Upload e processamento via web
- ✅ **Simplicidade**: Menos overhead de configuração
- ✅ **Métricas**: Tracking de embeddings

**Casos de uso:**
- Pesquisa e desenvolvimento
- Protótipos rápidos
- Demonstrações
- Testes de algoritmos RAG
- Interface web customizada

---

## 🔄 Migração e Sincronização

### Migrar Features de AMLDO_W para v0.2.0

**Features valiosas do AMLDO_W para integrar:**

#### 1. API REST FastAPI (ALTA PRIORIDADE)

```python
# Criar: src/amldo/interfaces/api/main.py
from fastapi import FastAPI
from amldo.rag.v2.tools import consultar_base_rag

app = FastAPI()

@app.post("/api/ask")
async def api_ask(payload: dict):
    q = payload.get("question", "").strip()
    resposta = consultar_base_rag(q)
    return {"answer": resposta}
```

**Benefícios:**
- Permite integração com outros sistemas
- Interface REST padrão
- Útil para microserviços

#### 2. Processamento Dinâmico de PDFs

```python
# Integrar em: src/amldo/interfaces/api/endpoints/upload.py
@app.post("/api/upload")
async def upload_and_process(files: List[UploadFile]):
    # Salvar PDFs
    # Processar com pipeline/ingestion
    # Atualizar índice FAISS
    # Retornar métricas
```

**Benefícios:**
- Permite adicionar documentos sem reiniciar
- Útil para ambientes dinâmicos

#### 3. Métricas de Embedding

```python
# Criar: src/amldo/utils/metrics.py
class EmbeddingMetrics:
    def track_embedding_count(self, count: int):
        # Salvar em DB (não JSON)
        # Usar PostgreSQL ou SQLite
```

**Melhorias:**
- Usar banco de dados em vez de JSON
- Dashboard com Grafana/Prometheus
- Métricas de performance

#### 4. RAG v3 Similarity Search

```python
# Adicionar em: src/amldo/rag/v3/
# Permitir escolha entre MMR e similarity via settings
class RAGv3:
    def __init__(self):
        self.search_type = settings.rag_v3_search_type  # "mmr" ou "similarity"
```

**Benefícios:**
- Experimentação A/B
- Comparação de resultados

### Migrar Features de v0.2.0 para AMLDO_W

**Features valiosas para integrar:**

#### 1. Configuração Centralizada

```python
# Adicionar: config.py na raiz do AMLDO_W
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str
    search_type: str = "similarity"
    k: int = 12

settings = Settings()
```

#### 2. Testes Automatizados

```bash
# Criar: tests/ em AMLDO_W
mkdir tests
# Adicionar pytest
pip install pytest pytest-cov
# Criar testes básicos para webapp/main.py
```

#### 3. Pipeline Modular

```python
# Refatorar notebooks para módulos Python
# get_v1_data.ipynb → pipeline/ingestion.py
# get_vectorial_bank_v1.ipynb → pipeline/indexer.py
```

---

## 🎯 Recomendações

### Para Desenvolvimento Contínuo

**Se o objetivo é produção:**
- ✅ **Usar AMLDO v0.2.0** como base
- ✅ Integrar API REST do AMLDO_W
- ✅ Adicionar processamento dinâmico de PDFs
- ✅ Implementar tracking de métricas (com DB)

**Se o objetivo é experimentação:**
- ✅ **Usar AMLDO_W** para prototipagem
- ✅ Adicionar testes básicos
- ✅ Documentar experimentos
- ✅ Migrar features bem-sucedidas para v0.2.0

### Arquitetura Ideal Híbrida

```
AMLDO v0.3.0 (Futuro)
├── src/amldo/
│   ├── core/              # ← v0.2.0
│   ├── rag/
│   │   ├── v1/            # ← v0.2.0
│   │   ├── v2/            # ← v0.2.0
│   │   └── v3/            # ← AMLDO_W (similarity)
│   ├── pipeline/          # ← v0.2.0 (modular)
│   ├── agents/            # ← v0.2.0 (CrewAI)
│   ├── interfaces/
│   │   ├── adk/           # ← v0.2.0
│   │   ├── streamlit/     # ← v0.2.0
│   │   └── api/           # ← AMLDO_W (FastAPI) ✨ NOVO
│   │       ├── main.py
│   │       ├── endpoints/
│   │       │   ├── query.py
│   │       │   ├── upload.py
│   │       │   └── metrics.py
│   │       └── templates/
│   └── utils/
│       └── metrics.py     # ← AMLDO_W (melhorado) ✨ NOVO
├── tests/                 # ← v0.2.0
└── docs/                  # ← v0.2.0
```

**Benefícios:**
- 🟢 Melhor dos dois mundos
- 🟢 API REST + Google ADK + Streamlit
- 🟢 Experimentação (v3) + Produção (v1/v2)
- 🟢 Processamento dinâmico + Pipeline modular
- 🟢 Testes + Métricas

---

## 📈 Roadmap de Convergência

### Fase 1: Integração API (Curto Prazo)

1. Criar `src/amldo/interfaces/api/` no v0.2.0
2. Implementar endpoints do AMLDO_W
3. Adicionar testes para API
4. Documentar OpenAPI/Swagger

**Estimativa:** 1-2 semanas

### Fase 2: Processamento Dinâmico (Médio Prazo)

1. Adicionar endpoint `/api/upload` e `/api/process`
2. Integrar com pipeline modular existente
3. Implementar tracking de métricas (PostgreSQL)
4. Dashboard de métricas

**Estimativa:** 2-3 semanas

### Fase 3: RAG v3 e Experimentação (Médio Prazo)

1. Adicionar `src/amldo/rag/v3/`
2. Permitir escolha de search_type via settings
3. A/B testing framework
4. Comparação de resultados

**Estimativa:** 1-2 semanas

### Fase 4: Testes AMLDO_W (Longo Prazo)

1. Adicionar testes ao AMLDO_W
2. Refatorar notebooks para módulos
3. Integração contínua

**Estimativa:** 2-3 semanas

---

## 🔍 Análise de Código Detalhada

### Diferença no RAG v2 Search Type

**AMLDO v0.2.0:**
```python
# src/amldo/rag/v2/tools.py:29-30
K = settings.search_k          # Configurável (default: 12)
SEARCH_TYPE = settings.search_type  # Configurável (default: "mmr")
```

**AMLDO_W (rag_v3_sim):**
```python
# rag_v3_sim/tools.py:14-15
K = 12
SEARCH_TYPE = "similarity"  # Fixo
```

**Impacto:**
- MMR (Maximal Marginal Relevance) reduz redundância
- Similarity retorna documentos mais similares (pode ter duplicatas)
- MMR geralmente melhor para RAG

**Recomendação:** Usar MMR como padrão, permitir similarity como opção.

### Processamento de PDFs

**AMLDO v0.2.0:**
```python
# src/amldo/pipeline/ingestion/ingest.py (modular)
def process_pdf(pdf_path: str) -> List[Article]:
    # Extração
    # Normalização
    # Estruturação
    # Validação
    return articles
```

**AMLDO_W:**
```python
# webapp/main.py:91-131 (inline)
@app.post("/api/process")
def api_process():
    # Extração com PyMuPDF (fitz)
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    # Split com RecursiveCharacterTextSplitter
    chunks = splitter.split_text(text)
    # Atualização do FAISS
    fallback_db.add_documents(new_docs)
    fallback_db.save_local("data/vector_db/v1_faiss_vector_db")
```

**Diferenças:**
- AMLDO_W usa PyMuPDF (fitz), v0.2.0 usa PyPDF2
- AMLDO_W chunk genérico, v0.2.0 estruturado (artigos)
- AMLDO_W inline, v0.2.0 modular

**Recomendação:** Integrar ambos — pipeline estruturado + endpoint API.

---

## 📝 Conclusão

### AMLDO v0.2.0
**✅ Escolha para produção, manutenção de longo prazo e trabalho em equipe**

**Pontos fortes:**
- Arquitetura moderna e escalável
- Testes e CI/CD
- Documentação completa
- Múltiplas interfaces
- CrewAI multi-agente
- Deploy production-ready

**Pontos a melhorar:**
- Adicionar API REST
- Processamento dinâmico de PDFs
- Métricas de sistema

### AMLDO_W
**✅ Escolha para experimentação rápida, protótipos e demos**

**Pontos fortes:**
- API REST funcional
- Processamento dinâmico
- Interface web customizada
- Métricas de embedding
- RAG v3 experimental

**Pontos a melhorar:**
- Adicionar testes
- Modularizar código
- Documentação
- Deploy para produção

### Próximos Passos Sugeridos

1. **Integrar FastAPI no v0.2.0** (ALTA PRIORIDADE)
2. **Adicionar testes ao AMLDO_W** (MÉDIA PRIORIDADE)
3. **Implementar métricas com DB no v0.2.0** (MÉDIA PRIORIDADE)
4. **Documentar experimentos RAG v3** (BAIXA PRIORIDADE)
5. **Criar versão v0.3.0 híbrida** (LONGO PRAZO)

---

**Documento criado:** 2025-11-15
**Próxima revisão:** Após integração de features
**Contato:** Equipe AMLDO
