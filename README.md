# AMLDO — Sistema RAG para Legislação de Licitações

> **Sistema de Retrieval-Augmented Generation (RAG)** especializado em legislação brasileira de licitações, compliance e governança.

[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0-green.svg)](https://langchain.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Visão Geral

O **AMLDO** permite consultas em linguagem natural sobre legislação de licitações, retornando respostas precisas e fundamentadas exclusivamente nos documentos legais indexados.

### Principais Características

- ✅ **Busca Semântica Avançada** - Embeddings multilíngues + FAISS
- ✅ **Respostas Fundamentadas** - Cita artigos e leis (sem alucinações)
- ✅ **Múltiplas Interfaces** - REST API (FastAPI) + Google ADK (CLI) + Streamlit (Web)
- ✅ **3 Versões do RAG** - Básico (v1), Avançado (v2 - MMR) e Experimental (v3 - Similarity)
- ✅ **Pipeline Completo** - Ingestão → Estruturação → Indexação → Consulta
- ✅ **Sistema de Métricas** - Tracking de queries e processamento com SQLite
- ✅ **4 Documentos Indexados** - Lei 14.133, LGPD, LCP 123, Decreto 10.024

### Tecnologias

- **Python 3.11+** | **LangChain** | **FAISS** | **Sentence Transformers** | **Gemini 2.5 Flash** | **Google ADK** | **FastAPI** | **Streamlit**

---

## 🚀 Quick Start

### Pré-requisitos

- Python **3.11** ou superior
- API Key do Google Gemini ([Obter aqui](https://makersuite.google.com/app/apikey))

### Instalação Rápida (5 minutos)

```bash
# 1. Clonar repositório
git clone https://github.com/Penhall/AMLDO.git
cd AMLDO

# 2. Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install --upgrade pip
pip install -e ".[api,adk,streamlit]"

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY

# 5. Rodar sistema (escolha uma interface)

# Opção 1: REST API (Recomendado para produção)
amldo-api

# Opção 2: Google ADK (CLI)
adk web

# Opção 3: Streamlit (Web interativa)
streamlit run src/amldo/interfaces/streamlit/app.py
```

**REST API:** http://localhost:8000 (documentação automática em `/docs`)
**Google ADK:** http://localhost:8080 (selecione agente `rag_v2`)
**Streamlit:** http://localhost:8501

### Teste Rápido

**Via cURL (REST API):**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual é o limite de valor para dispensa de licitação em obras?", "rag_version": "v2"}'
```

**Via Interface Web:**
Acesse http://localhost:8000 e use o chat interativo

---

## 📁 Estrutura do Projeto (v0.3.0)

```
AMLDO/
├── src/
│   └── amldo/                      # Package principal
│       ├── core/                   # Configuração e exceções
│       │   ├── config.py           # Settings centralizadas (pydantic)
│       │   └── exceptions.py       # Hierarquia de exceções
│       │
│       ├── rag/                    # Sistemas RAG
│       │   ├── v1/                 # RAG básico
│       │   │   ├── agent.py        # Agente Google ADK
│       │   │   └── tools.py        # Pipeline RAG simples
│       │   ├── v2/                 # RAG avançado (MMR + contexto hierárquico)
│       │   │   ├── agent.py
│       │   │   └── tools.py
│       │   └── v3/                 # RAG experimental (Similarity search) ✨ NOVO
│       │       ├── agent.py
│       │       └── tools.py
│       │
│       ├── pipeline/               # Pipeline de processamento
│       │   ├── embeddings.py       # Gerenciador de embeddings REAIS
│       │   ├── ingestion/          # Ingestão (PDF/TXT → texto)
│       │   ├── structure/          # Estruturação (texto → artigos)
│       │   └── indexer/            # Indexação (artigos → FAISS)
│       │
│       ├── agents/                 # Sistema multi-agente (CrewAI)
│       │   ├── base_agent.py
│       │   ├── orchestrator.py
│       │   └── specialized/        # Agentes especializados
│       │
│       ├── interfaces/             # Interfaces do usuário
│       │   ├── api/                # REST API FastAPI ✨ NOVO
│       │   │   ├── main.py         # FastAPI app
│       │   │   ├── run.py          # Script de execução
│       │   │   ├── routers/        # Endpoints (query, upload, metrics)
│       │   │   ├── models/         # Pydantic models (request/response)
│       │   │   ├── templates/      # Templates HTML (Jinja2)
│       │   │   └── static/         # CSS e assets
│       │   ├── adk/                # Interface Google ADK
│       │   └── streamlit/          # Interface Streamlit
│       │       ├── app.py
│       │       └── pages/
│       │
│       └── utils/                  # Utilitários
│           └── metrics.py          # Sistema de métricas SQLite ✨ NOVO
│
├── data/                           # Dados e artefatos
│   ├── raw/                        # PDFs originais
│   ├── split_docs/                 # Documentos hierarquicamente divididos
│   ├── processed/                  # Artigos processados (CSV/JSONL)
│   ├── vector_db/                  # Índice FAISS
│   └── metrics/                    # Banco SQLite de métricas ✨ NOVO
│
├── tests/                          # Testes
│   ├── unit/                       # Testes unitários
│   │   ├── test_config.py
│   │   ├── test_metrics.py         # ✨ NOVO
│   │   ├── test_rag_v3.py          # ✨ NOVO
│   │   └── ...
│   └── integration/                # Testes de integração
│
├── docs/                           # Documentação completa
│   ├── 00-visao-geral.md
│   ├── 01-arquitetura-tecnica.md
│   ├── 02-pipeline-rag.md
│   ├── ...
│   ├── 10-api-fastapi.md           # ✨ NOVO
│   └── README.md                   # Índice da documentação
│
├── notebooks/                      # Jupyter notebooks
│   ├── 01_data_processing.ipynb
│   ├── 02_vector_bank.ipynb
│   └── 03_rag_study.ipynb
│
├── requirements/                   # Dependências modularizadas
│   ├── base.txt                    # Core
│   ├── api.txt                     # FastAPI ✨ NOVO
│   ├── dev.txt                     # Desenvolvimento
│   └── adk.txt                     # Google ADK
│
├── AMLDO_W/                        # ⚠️ DEPRECADO - código experimental (não usar)
│
├── .env.example                    # Template de variáveis de ambiente
├── pyproject.toml                  # Configuração do projeto
├── CLAUDE.md                       # Guia para Claude Code
├── MIGRATION.md                    # Guia de migração v0.1 → v0.2
└── README.md                       # Este arquivo
```

**Nota:** O diretório `AMLDO_W/` contém código experimental e foi mantido apenas para referência histórica. **Não deve ser usado.** Todo código relevante foi integrado em `src/amldo/`.

---

## 📚 Documentação Completa

A documentação técnica completa está disponível na pasta **`docs/`**:

### 🎯 Documentos Essenciais

- **[docs/README.md](docs/README.md)** - Índice completo da documentação
- **[docs/00-visao-geral.md](docs/00-visao-geral.md)** - Introdução, objetivos e contexto de negócio
- **[docs/04-guia-desenvolvedor.md](docs/04-guia-desenvolvedor.md)** - Setup, desenvolvimento e debugging
- **[docs/10-api-fastapi.md](docs/10-api-fastapi.md)** - Documentação completa da REST API ✨ NOVO

### 📖 Documentação Técnica

- **[docs/01-arquitetura-tecnica.md](docs/01-arquitetura-tecnica.md)** - Componentes, camadas e decisões
- **[docs/02-pipeline-rag.md](docs/02-pipeline-rag.md)** - Detalhamento do pipeline RAG v1, v2 e v3
- **[docs/03-estrutura-dados.md](docs/03-estrutura-dados.md)** - Organização de dados e metadados
- **[docs/05-comandos-fluxos.md](docs/05-comandos-fluxos.md)** - Comandos úteis e workflows

### 🗺️ Planejamento e Roadmap

- **[docs/06-estado-atual.md](docs/06-estado-atual.md)** - Status, funcionalidades e limitações
- **[docs/08-melhorias-roadmap.md](docs/08-melhorias-roadmap.md)** - Propostas de melhoria e roadmap
- **[docs/PLANO-MIGRACAO.md](docs/PLANO-MIGRACAO.md)** - Plano de migração v0.2 → v0.3

---

## 🎨 Novidades da v0.3.0

### ✨ REST API com FastAPI

API REST completa e moderna:

- **8+ endpoints** para queries, upload, processamento e métricas
- **Documentação automática** com OpenAPI/Swagger (`/docs`)
- **Interface web interativa** (chat, upload, processamento)
- **CORS habilitado** para integração com frontends
- **Validação robusta** com Pydantic

**Endpoints principais:**
- `POST /api/ask` - Consulta RAG (suporta v1, v2, v3)
- `POST /api/upload` - Upload de múltiplos PDFs
- `POST /api/process` - Processa PDFs e atualiza índice FAISS
- `GET /api/metrics/stats` - Estatísticas do sistema

**Exemplo de uso:**
```bash
# Fazer uma pergunta
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "O que é dispensa de licitação?", "rag_version": "v2"}'

# Upload de PDFs
curl -X POST "http://localhost:8000/api/upload" \
  -F "files=@lei_14133.pdf" \
  -F "files=@decreto_10024.pdf"

# Processar documentos
curl -X POST "http://localhost:8000/api/process"

# Ver estatísticas
curl "http://localhost:8000/api/metrics/stats"
```

**Documentação completa:** [docs/10-api-fastapi.md](docs/10-api-fastapi.md)

### ✨ Sistema de Métricas com SQLite

Tracking completo de uso e performance:

- **Histórico de queries** (pergunta, versão RAG, tempo de resposta, sucesso/erro)
- **Histórico de processamento** (arquivos processados, chunks criados, duração)
- **Estatísticas agregadas** (contagem, médias, min/max por versão RAG)
- **Banco SQLite** (`data/metrics/metrics.db`)
- **APIs REST** para consulta de métricas

**Exemplo de dados coletados:**
```json
{
  "rag_stats": [
    {
      "version": "v2",
      "queries": 150,
      "avg_response_time_ms": 2300.5,
      "successful": 148,
      "failed": 2
    }
  ],
  "total_files_processed": 4,
  "total_chunks_indexed": 4123,
  "queries_last_24h": 45
}
```

### ✨ RAG v3 (Experimental)

Nova versão do RAG com similarity search:

- **Similarity search** (vs MMR do v2)
- **Contexto hierárquico** (mantido do v2)
- **Configurável** via settings (`rag_v3_search_type`, `rag_v3_k`)

**Comparação das versões:**

| Versão | Busca | Contexto | Uso Recomendado |
|--------|-------|----------|-----------------|
| v1 | MMR | Simples | Testes rápidos |
| v2 | MMR | Hierárquico | **Produção (padrão)** |
| v3 | Similarity | Hierárquico | Experimentação |

---

## 💻 Desenvolvimento

### Instalação Completa (para desenvolvedores)

```bash
# Instalar com TODAS as dependências (dev + api + adk + streamlit)
pip install -e ".[all,dev]"

# Instalar hooks de pre-commit
pre-commit install

# Rodar testes
pytest

# Com coverage
pytest --cov=src/amldo --cov-report=html

# Linting e formatação
black src/
ruff check src/
mypy src/
```

### Scripts Disponíveis

Adicionados via `pyproject.toml`:

- `amldo-api` - Roda a REST API (FastAPI)
- `amldo-process` - Processa documentos (CLI)
- `amldo-build-index` - Constrói índice FAISS (CLI)

### Configuração (.env)

Principais variáveis de ambiente:

```bash
# LLM
GOOGLE_API_KEY=your_key_here
LLM_MODEL=gemini-2.5-flash
LLM_PROVIDER=google_genai

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False

# RAG
DEFAULT_RAG_VERSION=v2
SEARCH_K=12
SEARCH_TYPE=mmr

# Paths
DATA_DIR=data
VECTOR_DB_PATH=data/vector_db/v1_faiss_vector_db
```

**Veja `.env.example` para lista completa.**

### Testando Alterações

```bash
# Testar RAG v2
adk web  # Selecione rag_v2

# Testar API REST
amldo-api  # Acesse http://localhost:8000/docs

# Testar Streamlit
streamlit run src/amldo/interfaces/streamlit/app.py
```

---

## 🔧 Manutenção

### Adicionar Novo Documento

**Via API REST:**
```bash
# 1. Upload
curl -X POST "http://localhost:8000/api/upload" -F "files=@novo_doc.pdf"

# 2. Processar
curl -X POST "http://localhost:8000/api/process"
```

**Via notebooks:**
1. Colocar PDF em `data/raw/`
2. Executar `notebooks/01_data_processing.ipynb`
3. Executar `notebooks/02_vector_bank.ipynb`

### Backup do Banco Vetorial

```bash
# Criar backup
cp -r data/vector_db/v1_faiss_vector_db data/vector_db/v1_faiss_vector_db_backup_$(date +%Y%m%d)

# Verificar integridade
python -c "from langchain_community.vectorstores import FAISS; from langchain_huggingface import HuggingFaceEmbeddings; embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); db = FAISS.load_local('data/vector_db/v1_faiss_vector_db', embeddings=embeddings, allow_dangerous_deserialization=True); print(f'OK: {len(db.docstore._dict)} chunks')"
```

### Limpar Cache

```bash
# Limpar __pycache__ e .pyc
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Limpar notebooks checkpoints
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

# Limpar métricas antigas (30 dias)
python -c "from amldo.utils.metrics import get_metrics_manager; m = get_metrics_manager(); print(f'Deleted {m.clear_old_records(days=30)} records')"
```

---

## 📊 Métricas de Qualidade

### Performance

- ⚡ **Latência média**: 2-5 segundos (v2)
- 📊 **Taxa de sucesso**: >98% (baseado em métricas reais)
- 🎯 **Precisão**: >90% (avaliação subjetiva em casos de uso)

### Cobertura

- 📚 **4 documentos legais** indexados
- 📄 **~445 artigos** processados
- 🔢 **~4.123 chunks** no FAISS
- 🎯 **Zero alucinações** (respostas fundamentadas apenas em documentos)

---

## 🤝 Como Contribuir

Veja oportunidades de contribuição em:
- **[docs/06-estado-atual.md](docs/06-estado-atual.md)** - Pendências e TODOs
- **[docs/08-melhorias-roadmap.md](docs/08-melhorias-roadmap.md)** - Roadmap e melhorias propostas

### Workflow de Contribuição

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Faça suas alterações
4. Rode os testes (`pytest`)
5. Commit suas mudanças (`git commit -am 'feat: adiciona nova feature'`)
6. Push para a branch (`git push origin feature/minha-feature`)
7. Abra um Pull Request

---

## 📝 Histórico de Versões

### v0.3.0 (2025-11-16) - **ATUAL**

**Principais mudanças:**
- ✨ **REST API com FastAPI** (8+ endpoints, docs automática, interface web)
- ✨ **Sistema de métricas com SQLite** (tracking de queries e processamento)
- ✨ **RAG v3** (similarity search experimental)
- 🔧 Testes completos para métricas e RAG v3
- 📚 Documentação completa da API (docs/10-api-fastapi.md)

### v0.2.0 (2025-11-14)

**Principais mudanças:**
- 🏗️ Reestruturação completa para `src/` layout
- ⚙️ Configuração centralizada com pydantic-settings
- 🧪 Suite de testes com pytest
- 🎨 Interface Streamlit
- 📦 Pipeline de processamento integrado (REAL embeddings)
- 🤖 Sistema multi-agente CrewAI
- 📚 Documentação completa (8 documentos)

### v0.1.0 (2025-10-30)

**Release inicial:**
- ✅ RAG v1 e v2 funcionais
- ✅ Google ADK integration
- ✅ FAISS vector store
- ✅ 4 documentos legais indexados
- ✅ Notebooks de processamento

---

## 🔗 Links Úteis

- **Documentação:** [docs/README.md](docs/README.md)
- **API REST:** [docs/10-api-fastapi.md](docs/10-api-fastapi.md)
- **Claude Code:** [CLAUDE.md](CLAUDE.md)
- **Migração:** [MIGRATION.md](MIGRATION.md)
- **Repositório:** https://github.com/Penhall/AMLDO

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

- **Equipe AMLDO**
- **Claude Code** (co-author)

---

**Boa codificação! 🚀**

Se encontrar bugs ou tiver sugestões, abra uma issue no repositório.
