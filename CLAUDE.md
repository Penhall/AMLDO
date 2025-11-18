# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AMLDO v0.3.0** is a modern RAG (Retrieval-Augmented Generation) application specialized in Brazilian procurement law (licitação), compliance, governance, and internal regulations. The system uses FAISS vector store with multilingual embeddings to answer questions based on legal documents.

**Key Features:**
- **3 RAG versions** (v1: basic, v2: MMR, v3: similarity search)
- **3 Interfaces**: Google ADK, Streamlit, FastAPI REST API ✨ NEW
- **Modern architecture** with `src/` package structure
- **Centralized configuration** with pydantic-settings
- **Real embeddings** (sentence-transformers)
- **Metrics system** with SQLite ✨ NEW
- **Comprehensive tests** with pytest
- **Pre-commit hooks** and CI/CD
- **CrewAI multi-agent** system

## Environment Setup

**Required:** Python 3.11+

```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (modern approach with pyproject.toml)
pip install --upgrade pip
pip install -e ".[adk,streamlit,dev]"  # Editable install with extras

# Or install specific requirements
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

**Environment Variables:** Create a `.env` file in the root (copy from `.env.example`):
- `GOOGLE_API_KEY` (required for Gemini API)
- See `.env.example` for full list of configurable variables

**Pre-commit Hooks (optional but recommended):**
```bash
pre-commit install
```

## Running the Application

### 🚀 Quick Start - Use Python Script (RECOMMENDED)

The easiest way to run the applications is using the Python menu script:

```bash
# Interactive menu (recommended)
python scripts/run.py

# Or direct commands
python scripts/run.py --api         # FastAPI REST API (port 8000)
python scripts/run.py --streamlit   # Streamlit Web App (port 8501)
python scripts/run.py --adk         # Google ADK Interface (port 8080)
python scripts/run.py --all         # All apps simultaneously with logs
```

**Advantages:**
- ✅ Works on Windows, Linux, and Mac (no shell required)
- ✅ Interactive menu with numbered options
- ✅ Automatic prerequisite checking
- ✅ Process management and cleanup

**See `scripts/README.md` for detailed documentation.**

---

### Option 1: Google ADK Interface (Conversational RAG)

```bash
# Using Python script (recommended)
python scripts/run.py --adk

# Or direct command
adk web
```
Then access http://localhost:8080 and select agent:
- `rag_v2` (recommended - MMR search with hierarchical context)
- `rag_v3` (experimental - similarity search with hierarchical context) ✨ NEW
- `rag_v1` (basic - simple MMR search)

### Option 2: Streamlit Web Interface (Full pipeline)

```bash
# Using Python script (recommended)
python scripts/run.py --streamlit

# Or direct command
streamlit run src/amldo/interfaces/streamlit/app.py
```
Then access http://localhost:8501

**Pages available:**
- **Home**: Overview
- **Pipeline**: Upload and process new documents
- **RAG Query**: Query the knowledge base

### Option 3: FastAPI REST API ✨ (Recommended for integration)

```bash
# Using Python script (recommended)
python scripts/run.py --api

# Or direct command
amldo-api

# Or with custom settings
API_HOST=0.0.0.0 API_PORT=8000 amldo-api
```
Then access:
- http://localhost:8000 - Web interface
- http://localhost:8000/docs - Swagger API documentation
- http://localhost:8000/consulta - Chat interface
- http://localhost:8000/processamento - Document processing

**Key endpoints:**
- `POST /api/ask` - Query RAG (v1/v2/v3 selectable)
- `POST /api/upload` - Upload PDFs
- `POST /api/process` - Process documents
- `GET /api/metrics/stats` - System metrics

### Option 4: CLI Scripts

```bash
# Process a new document (PDF/TXT → structured articles)
amldo-process --input data/raw/nova_lei.pdf --output data/processed/

# Build FAISS index from processed articles
amldo-build-index --source data/processed/artigos.jsonl --output data/vector_db/
```

## Architecture

### Modern Package Structure (v0.2+)

```
src/amldo/                      # Main package
├── core/                       # Core configuration and exceptions
│   ├── config.py               # Centralized settings (pydantic-settings)
│   └── exceptions.py           # Exception hierarchy
│
├── rag/                        # RAG systems
│   ├── v1/                     # Basic RAG
│   │   ├── agent.py            # Google ADK agent
│   │   └── tools.py            # Simple RAG pipeline
│   ├── v2/                     # Advanced RAG (hierarchical context)
│   │   ├── agent.py
│   │   └── tools.py
│   └── v3/                     # RAG v3 (similarity search variant) ✨ NEW
│       ├── agent.py            # Google ADK agent
│       └── tools.py            # Similarity search RAG
│
├── pipeline/                   # Document processing pipeline
│   ├── embeddings.py           # Embedding manager (REAL, not dummy!)
│   ├── ingestion/              # PDF/TXT → text
│   ├── structure/              # Text → structured articles
│   └── indexer/                # Articles → FAISS index
│
├── agents/                     # Multi-agent system (CrewAI)
│   ├── base_agent.py
│   ├── orchestrator.py
│   └── specialized/            # Specialized agents
│
├── interfaces/                 # User interfaces
│   ├── adk/                    # Google ADK interface
│   ├── streamlit/              # Streamlit web app
│   │   ├── app.py
│   │   └── pages/
│   └── api/                    # FastAPI REST API ✨ NEW
│       ├── main.py
│       ├── run.py
│       ├── routers/            # Endpoints modulares
│       ├── models/             # Pydantic schemas
│       ├── templates/          # HTML (Jinja2)
│       └── static/             # CSS, JS
│
└── utils/                      # Shared utilities
    ├── logger.py
    └── metrics.py              # Metrics system (SQLite) ✨ NEW
```

### Centralized Configuration

**All settings are managed in `src/amldo/core/config.py`:**
- Uses pydantic-settings for validation
- Loads from `.env` file
- Provides defaults for all optional settings
- Access via `from amldo.core.config import settings`

**Key settings:**
- `google_api_key`: Gemini API key (required)
- `embedding_model`: Sentence transformer model
- `llm_model`: LLM model name
- `search_k`: Number of docs to retrieve (default: 12)
- `search_type`: Search strategy (default: "mmr")
- `vector_db_path`: Path to FAISS index

### RAG Pipeline (v1, v2, and v3)

Three versions available in `src/amldo/rag/`:

**rag_v1/**: Basic RAG implementation
- Simple retrieval from FAISS with MMR search
- Returns raw context directly to LLM
- Faster, simpler

**rag_v2/**: Enhanced RAG with context post-processing (MMR)
- Filters out `artigo_0.txt` from retrieval
- Restructures context hierarchically: Lei → Título → Capítulo → Artigo
- Injects "artigo 0" content (chapter/title introductions) from CSV
- Produces XML-tagged structure for LLM
- Uses MMR (Maximal Marginal Relevance) search
- Better for complex legal queries

**rag_v3/**: Similarity Search variant ✨ NEW
- Same hierarchical post-processing as v2
- Uses **similarity search** instead of MMR (configurable)
- Filters out `artigo_0.txt` from retrieval
- Produces same XML-tagged structure
- Experimental: may have different retrieval characteristics vs v2
- Configurable via `settings.rag_v3_search_type` and `settings.rag_v3_k`

All versions expose a `root_agent` (Google ADK agent) that uses `consultar_base_rag` tool.

**Key files:**
- `src/amldo/rag/v1/tools.py` - RAG v1 tool
- `src/amldo/rag/v2/tools.py` - RAG v2 tool
- `src/amldo/rag/v3/tools.py` - RAG v3 tool ✨ NEW

### Document Processing Pipeline

**NEW in v0.2:** Integrated from LicitAI POC with major improvements.

**Location:** `src/amldo/pipeline/`

**Modules:**
1. **ingestion/** (`ingest.py`): Reads PDF/TXT files, extracts and normalizes text
2. **structure/** (`structure.py`): Splits text into articles using regex
3. **indexer/** (`indexer.py`): Creates FAISS index from articles
4. **embeddings.py**: **CRITICAL** - Manages REAL embeddings (sentence-transformers)

**IMPORTANT:** The LicitAI POC originally used dummy embeddings. This has been replaced with real semantic embeddings using `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

### Embedding Model

**Location:** `src/amldo/pipeline/embeddings.py`

```python
from amldo.pipeline.embeddings import EmbeddingManager

# Usage
embedding_manager = EmbeddingManager()
embeddings = embedding_manager.embed(["text1", "text2"])  # Real embeddings!
```

**Features:**
- Uses sentence-transformers (same as RAG system)
- Normalized embeddings
- Configurable via settings
- Replaces dummy embeddings from LicitAI POC

### Vector Store

**FAISS index:** `data/vector_db/v1_faiss_vector_db`
- Pre-built index (included in repo)
- Deserialization uses `allow_dangerous_deserialization=True` (necessary for pickle-based FAISS)
- Only use with trusted sources

**Search Configuration:**
- Type: MMR (Maximal Marginal Relevance)
- K: 12 documents
- Configurable via settings

### LLM

**Model:** Gemini 2.5 Flash
**Provider:** `google_genai` (via LangChain)
**Configuration:** Centralized in `settings.llm_model`

### Data Structure

```
data/
├── raw/                    # Original PDF legal documents
│   ├── D10024.pdf          # Decreto 10024
│   ├── L13709.pdf          # Lei 13709 (LGPD)
│   ├── L14133.pdf          # Lei 14133 (Licitações)
│   └── Lcp123.pdf          # Lei Complementar 123
├── split_docs/             # Hierarchically split documents
│   └── {Lei}/TITULO_{X}/capitulos/CAPITULO_{Y}/artigos/artigo_{N}.txt
├── processed/              # Preprocessed data
│   ├── v1_artigos_0.csv           # Chapter/title introductions
│   └── v1_processed_articles.csv  # All processed articles
└── vector_db/
    └── v1_faiss_vector_db/        # FAISS index files
```

**Metadata for each chunk:**
- `lei`: Law identifier (e.g., "L14133")
- `titulo`: Title section (e.g., "TITULO_II")
- `capitulo`: Chapter section (e.g., "CAPITULO_III")
- `artigo`: Article filename (e.g., "artigo_15.txt")
- `chunk_idx`: Chunk index within article

## Development Workflow

### Testing Changes to RAG

1. Modify `src/amldo/rag/v1/tools.py` or `src/amldo/rag/v2/tools.py`
2. Run `adk web` and test with queries
3. Check response quality and context relevance

### Adding New Documents

**Option A: Using Notebooks (Original method)**
1. Place PDF in `data/raw/`
2. Use notebooks in `notebooks/`:
   - `01_data_processing.ipynb`: Extract and split documents
   - `02_vector_bank.ipynb`: Build FAISS index
3. Ensure metadata fields match existing structure

**Option B: Using CLI Scripts (New in v0.2)**
```bash
# 1. Process document
amldo-process --input data/raw/nova_lei.pdf --output data/processed/

# 2. Build index
amldo-build-index --source data/processed/nova_lei_artigos.jsonl --output data/vector_db/
```

**Option C: Using Streamlit Interface (New in v0.2)**
1. Go to http://localhost:8501
2. Navigate to "Pipeline" page
3. Upload document and follow the 3-step process

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src/amldo --cov-report=html

# Specific test file
pytest tests/unit/test_ingestion.py

# Specific test
pytest tests/unit/test_config.py::test_settings_with_env_vars
```

**Test structure:**
- `tests/unit/`: Unit tests
- `tests/integration/`: Integration tests
- `tests/conftest.py`: Shared fixtures

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/

# Type checking
mypy src/

# Run all checks (via pre-commit)
pre-commit run --all-files
```

### Notebooks

**Location:** `notebooks/` (renamed from root in v0.2)
- `01_data_processing.ipynb`: Document processing pipeline
- `02_vector_bank.ipynb`: Vector store creation
- `03_rag_study.ipynb`: Analysis and experimentation

**Setup Jupyter kernel:**
```bash
python -m ipykernel install --user --name=amldo --display-name "AMLDO Kernel"
```

## Important Notes

### What Changed in v0.2+

**v0.2.0:**
- **Structure:** Moved from flat structure to `src/amldo/` package
- **Config:** Centralized in `src/amldo/core/config.py`
- **Embeddings:** LicitAI pipeline now uses REAL embeddings (not dummy)
- **Tests:** Added comprehensive test suite
- **CI/CD:** GitHub Actions for tests and linting
- **Interfaces:** Added Streamlit web interface
- **Scripts:** Added CLI scripts for common tasks
- **Agents:** Integrated CrewAI multi-agent system
- **Documentation:** Added MIGRATION.md guide

**v0.3.0 (current):**
- **RAG v3:** Added similarity search variant
- **FastAPI:** Complete REST API with 8+ endpoints
- **Metrics:** SQLite-based metrics system
- **Templates:** Web UI with Bootstrap 5
- **Config:** Added API settings (`api_host`, `api_port`, etc.)
- **Docs:** Complete API documentation (docs/10-api-fastapi.md)

### Breaking Changes from v0.1

- Import paths changed: `from rag_v1.tools import` → `from amldo.rag.v1.tools import`
- Config now loaded from `settings` singleton instead of env vars directly
- Notebooks moved to `notebooks/` directory
- Requirements split into `requirements/` subdirectories

### Security Notes

- FAISS deserialization uses `allow_dangerous_deserialization=True` (necessary for pickle-based indices)
- Only use with trusted data sources
- API keys managed via `.env` (never commit `.env`!)
- `settings.model_dump_safe()` redacts secrets in logs

### CrewAI Agents

**Location:** `src/amldo/agents/`

**Status:** Integrated but not fully connected to pipeline yet

**Available agents:**
- IngestionAgent
- StructuringAgent
- IndexingAgent
- ComplianceAgent
- ValidationAgent
- CompanyDocsAgent

**Usage:**
```python
from amldo.agents.orchestrator import build_all_agents

agents = build_all_agents()
# agents["compliance"], agents["validation"], etc.
```

### Migration Guide

See `MIGRATION.md` for detailed migration guide from v0.1 to v0.2.

## Troubleshooting

### ModuleNotFoundError: No module named 'amldo'

**Solution:** Install package in editable mode
```bash
pip install -e .
```

### FAISS deserialization error

**Solution:** Ensure `allow_dangerous_deserialization=True` is set (already configured in code)

### Google API Key not found

**Solution:** Create `.env` file from `.env.example` and add your key
```bash
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```

### Tests fail with import errors

**Solution:** Install dev dependencies
```bash
pip install -e ".[dev]"
```

### adk web doesn't find agents

**Solution:** Agents are now in `src/amldo/rag/`, but ADK should discover them automatically. If not, check that package is installed in editable mode.

## Quick Reference

**Common Commands:**
```bash
# Run interfaces (RECOMMENDED: use Python script)
python scripts/run.py            # Interactive menu ⭐
python scripts/run.py --all      # All apps at once
python scripts/run.py --api      # FastAPI (port 8000)
python scripts/run.py --streamlit  # Streamlit (port 8501)
python scripts/run.py --adk      # Google ADK (port 8080)

# Or direct commands
adk web                          # Google ADK
streamlit run src/amldo/interfaces/streamlit/app.py  # Streamlit
amldo-api                        # FastAPI

# Process documents
amldo-process --input file.pdf --output data/processed/
amldo-build-index --source artigos.jsonl --output vector_store/

# Run tests
pytest                           # All tests
pytest tests/unit/test_rag_v3.py  # Specific test
pytest --cov=src/amldo           # With coverage

# Code quality
black src/ && ruff check src/ && mypy src/
```

**Key Files:**
- `src/amldo/core/config.py` - All configuration
- `src/amldo/rag/v2/tools.py` - RAG v2 implementation
- `src/amldo/pipeline/embeddings.py` - Embedding management
- `pyproject.toml` - Project configuration
- `.env` - Environment variables (not in git)
- `MIGRATION.md` - Migration guide

**Documentation:**
- **Shell scripts:** `scripts/README.md` ⭐ NEW
- **Instructions:** `.instructions/README.md` ⭐ NEW
- Full technical docs in `docs/` directory
- API usage in `docs/04-guia-desenvolvedor.md`
- Migration guide in `MIGRATION.md`
- This file (CLAUDE.md) for quick reference
