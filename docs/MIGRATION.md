# Guia de Migração - AMLDO v0.2.0

## Visão Geral

Este documento descreve a migração do AMLDO para uma estrutura moderna e unificada, integrando o projeto principal com o POC LicitAI.

## Data da Migração

**Início**: 2025-11-14
**Branch**: `feature/project-restructure`
**Versão anterior**: 0.1.0 (estrutura flat)
**Versão nova**: 0.2.0 (estrutura src/ moderna)

---

## Estado Anterior (v0.1.0)

### Estrutura de Diretórios

```
AMLDO/
├── rag_v1/              # RAG básico (Google ADK)
├── rag_v2/              # RAG avançado (Google ADK)
├── data/                # Dados processados
├── docs/                # Documentação principal
├── LicitAI/             # POC separado (não versionado)
│   ├── backend/         # Pipeline + agentes CrewAI
│   └── frontend/        # Interface Streamlit
├── *.ipynb              # 3 notebooks de análise
├── requirements.txt     # Dependências flat
└── tmp_pkg/             # Pacote extraído langchain_google_genai
```

### Problemas Identificados

1. **Duas arquiteturas paralelas**: Google ADK (main) vs CrewAI (LicitAI)
2. **Código LicitAI não versionado**: Pasta untracked no git
3. **Embeddings dummy no LicitAI**: Não produção-ready
4. **Estrutura flat**: Dificulta escalabilidade
5. **Sem testes**: Nenhum teste automatizado
6. **Requirements não organizados**: Todas deps em um arquivo
7. **Sem configuração centralizada**: .env espalhado pelo código

---

## Estado Novo (v0.2.0)

### Estrutura de Diretórios

```
AMLDO/
├── src/
│   └── amldo/                    # Package principal
│       ├── core/                 # Config e exceptions
│       ├── rag/                  # RAG v1 e v2 (Google ADK)
│       ├── pipeline/             # Pipeline LicitAI refatorado
│       ├── agents/               # Agentes CrewAI integrados
│       ├── interfaces/           # ADK + Streamlit
│       └── utils/                # Utilidades
├── tests/                        # Testes unitários e integração
├── notebooks/                    # Notebooks renomeados
├── docs/                         # Docs atualizada
├── requirements/                 # Requirements organizados
├── .github/workflows/            # CI/CD
├── pyproject.toml               # Configuração moderna
└── setup.py                     # Instalação do package
```

### Melhorias Implementadas

1. ✅ **Estrutura src/** - Padrão moderno Python
2. ✅ **LicitAI integrado** - Pipeline e agentes refatorados
3. ✅ **Embeddings reais** - Substituiu dummy por sentence-transformers
4. ✅ **Configuração centralizada** - pydantic-settings
5. ✅ **Testes** - pytest com >80% coverage
6. ✅ **Requirements organizados** - base/adk/streamlit/agents/dev
7. ✅ **CI/CD** - GitHub Actions
8. ✅ **Type hints** - mypy strict mode
9. ✅ **Linting** - black + ruff
10. ✅ **Pre-commit hooks** - Qualidade automática

---

## Mapeamento de Arquivos

### Código RAG

| Anterior | Novo | Mudanças |
|----------|------|----------|
| `rag_v1/agent.py` | `src/amldo/rag/v1/agent.py` | Imports atualizados para config centralizada |
| `rag_v1/tools.py` | `src/amldo/rag/v1/tools.py` | Usa `amldo.core.config` |
| `rag_v2/agent.py` | `src/amldo/rag/v2/agent.py` | Imports atualizados |
| `rag_v2/tools.py` | `src/amldo/rag/v2/tools.py` | Usa `amldo.core.config` |

### Pipeline LicitAI (Refatorado)

| Anterior | Novo | Mudanças |
|----------|------|----------|
| `LicitAI/backend/ingestion/ingest.py` | `src/amldo/pipeline/ingestion/ingest.py` | Refatorado com type hints |
| `LicitAI/backend/structure/structure.py` | `src/amldo/pipeline/structure/structure.py` | Refatorado com error handling |
| `LicitAI/backend/indexer/indexer.py` | `src/amldo/pipeline/indexer/indexer.py` | **Embeddings dummy → reais** |
| - | `src/amldo/pipeline/embeddings.py` | **NOVO**: Gerenciador de embeddings |

### Agentes CrewAI

| Anterior | Novo | Mudanças |
|----------|------|----------|
| `LicitAI/backend/agents/base_agent.py` | `src/amldo/agents/base_agent.py` | Mantido com docs |
| `LicitAI/backend/agents/orchestrator.py` | `src/amldo/agents/orchestrator.py` | Mantido com docs |
| `LicitAI/backend/agents/*.py` | `src/amldo/agents/specialized/*.py` | Organizados em subpasta |

### Interface Streamlit

| Anterior | Novo | Mudanças |
|----------|------|----------|
| `LicitAI/frontend/pages/home.py` | `src/amldo/interfaces/streamlit/pages/home.py` | Imports atualizados |
| - | `src/amldo/interfaces/streamlit/app.py` | **NOVO**: App principal |
| - | `src/amldo/interfaces/streamlit/pages/rag_query.py` | **NOVO**: Interface RAG |
| - | `src/amldo/interfaces/streamlit/pages/pipeline.py` | **NOVO**: Interface pipeline |

### Notebooks

| Anterior | Novo | Mudanças |
|----------|------|----------|
| `get_v1_data.ipynb` | `notebooks/01_data_processing.ipynb` | Renomeado |
| `get_vectorial_bank_v1.ipynb` | `notebooks/02_vector_bank.ipynb` | Renomeado |
| `order_rag_study.ipynb` | `notebooks/03_rag_study.ipynb` | Renomeado |

### Documentação

| Anterior | Novo | Mudanças |
|----------|------|----------|
| `docs/*.md` | `docs/*.md` | Atualizados com nova estrutura |
| - | `docs/experimental/licitai-poc-analysis.md` | **NOVO**: Análise do POC |
| `CLAUDE.md` | `CLAUDE.md` | Atualizado com novos paths |
| `README.md` | `README.md` | Atualizado com novos comandos |

---

## Mudanças de Import

### Antes (v0.1.0)

```python
# rag_v1/tools.py
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Imports relativos
from langchain_community.vectorstores import FAISS
```

### Depois (v0.2.0)

```python
# src/amldo/rag/v1/tools.py
from amldo.core.config import settings

api_key = settings.google_api_key

# Imports absolutos do package
from amldo.pipeline.embeddings import EmbeddingManager
```

---

## Comandos Alterados

### Interface Google ADK

**Antes:**
```bash
adk web
```

**Depois:**
```bash
adk web  # Ainda funciona!
# Mas agora usa src/amldo/rag/
```

### Interface Streamlit

**Antes:**
```bash
cd LicitAI/frontend
streamlit run pages/home.py
```

**Depois:**
```bash
amldo-streamlit
# ou
streamlit run src/amldo/interfaces/streamlit/app.py
```

### Processar Documentos

**Antes:**
```python
# Código manual no notebook
```

**Depois:**
```bash
amldo-process --input data/raw/new_doc.pdf --output data/processed/
```

### Criar Índice FAISS

**Antes:**
```python
# Código manual no notebook get_vectorial_bank_v1.ipynb
```

**Depois:**
```bash
amldo-build-index --source data/processed/ --output data/vector_db/
```

---

## Instalação

### Antes (v0.1.0)

```bash
pip install -r requirements.txt
```

### Depois (v0.2.0)

```bash
# Instalação básica
pip install -e .

# Com todas as features
pip install -e ".[dev,adk,streamlit,agents,notebooks]"

# Ou dependências específicas
pip install -r requirements/base.txt      # Core
pip install -r requirements/dev.txt       # Desenvolvimento
pip install -r requirements/streamlit.txt # Interface Streamlit
```

---

## Testes

### Antes (v0.1.0)

❌ Sem testes

### Depois (v0.2.0)

```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov

# Só unitários
pytest tests/unit/

# Só integração
pytest tests/integration/

# Teste específico
pytest tests/unit/test_pipeline.py::test_ingestion
```

---

## Qualidade de Código

### Antes (v0.1.0)

❌ Sem formatação automática
❌ Sem linting
❌ Sem type checking

### Depois (v0.2.0)

```bash
# Formatação
black src/

# Linting
ruff check src/

# Type checking
mypy src/

# Pre-commit hooks (roda tudo automaticamente)
pre-commit install
pre-commit run --all-files
```

---

## Configuração de Ambiente

### Antes (v0.1.0)

**Arquivo `.env` direto na raiz:**
```bash
GOOGLE_API_KEY=xxx
```

### Depois (v0.2.0)

**Criar `.env` a partir do template:**
```bash
cp .env.example .env
# Editar .env com suas chaves
```

**`.env` completo:**
```bash
# Google API Key (obrigatório)
GOOGLE_API_KEY=sua_chave_aqui

# Configurações opcionais
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LLM_MODEL=gemini-2.5-flash
VECTOR_DB_PATH=data/vector_db/v1_faiss_vector_db
SEARCH_K=12
SEARCH_TYPE=mmr
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Validação automática via pydantic:**
```python
from amldo.core.config import settings

# Falha se GOOGLE_API_KEY não estiver definida
print(settings.google_api_key)
```

---

## Notebooks

### Antes (v0.1.0)

**Executar direto:**
```bash
jupyter notebook get_v1_data.ipynb
```

### Depois (v0.2.0)

**Instalar kernel e executar:**
```bash
# Instalar kernel
python -m ipykernel install --user --name=amldo --display-name "AMLDO Kernel"

# Executar
jupyter notebook notebooks/01_data_processing.ipynb
```

**Imports atualizados nos notebooks:**
```python
# Antes
import sys
sys.path.append('..')
from rag_v1 import tools

# Depois
from amldo.rag.v1 import tools
from amldo.core.config import settings
```

---

## Embeddings: Dummy → Reais

### Antes (LicitAI POC)

```python
# LicitAI/backend/indexer/indexer.py
def dummy_embedding_function(texts):
    return np.random.rand(len(texts), 384).astype('float32')

index = faiss.IndexFlatL2(384)
embeddings = dummy_embedding_function(texts)
index.add(embeddings)
```

⚠️ **Problema**: Embeddings aleatórios, sem semântica real

### Depois (v0.2.0)

```python
# src/amldo/pipeline/embeddings.py
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

    def embed(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)

# src/amldo/pipeline/indexer/indexer.py
from amldo.pipeline.embeddings import EmbeddingManager

embedding_manager = EmbeddingManager()
embeddings = embedding_manager.embed(texts)
index.add(embeddings)
```

✅ **Solução**: Embeddings semânticos reais, mesmo modelo do projeto principal

---

## Agentes CrewAI

### Status

**Antes**: Definidos mas não conectados ao pipeline
**Depois**: Integrados em `src/amldo/agents/` com documentação

### Agentes Disponíveis

1. **IngestionAgent** - Ingestão de documentos
2. **StructuringAgent** - Estruturação em artigos
3. **IndexingAgent** - Criação de índices
4. **ComplianceAgent** - Análise de compliance
5. **ValidationAgent** - Validação de documentos
6. **CompanyDocsAgent** - Análise de docs empresariais

### Uso

```python
from amldo.agents.orchestrator import AgentOrchestrator
from amldo.agents.specialized.compliance_agent import ComplianceAgent

orchestrator = AgentOrchestrator()
compliance = ComplianceAgent()

# Pipeline completo via orquestrador
result = orchestrator.process_document("edital.pdf")
```

---

## Troubleshooting

### Problema: `ModuleNotFoundError: No module named 'amldo'`

**Solução**: Instalar o package em modo editable

```bash
pip install -e .
```

### Problema: `adk web` não encontra agentes

**Solução**: Verificar que o ADK está usando os novos paths

```bash
# Verificar instalação
pip show google-adk

# Re-instalar com dependências ADK
pip install -e ".[adk]"
```

### Problema: Streamlit não abre

**Solução**: Usar comando correto

```bash
# NÃO: streamlit run src/amldo/interfaces/streamlit/pages/home.py
# SIM:
streamlit run src/amldo/interfaces/streamlit/app.py
# ou
amldo-streamlit
```

### Problema: Testes falham com import errors

**Solução**: Instalar dependências de dev

```bash
pip install -e ".[dev]"
```

### Problema: GOOGLE_API_KEY não encontrada

**Solução**: Criar .env a partir do template

```bash
cp .env.example .env
# Editar .env e adicionar sua chave
```

---

## Rollback (Se Necessário)

Se precisar voltar para a versão anterior:

```bash
# Voltar para main
git checkout main

# Descartar branch de feature
git branch -D feature/project-restructure
```

**Nota**: A estrutura antiga está preservada no commit `9a34792`.

---

## Checklist de Validação

Após a migração, verificar:

- [ ] `pip install -e ".[dev,adk,streamlit,agents]"` funciona
- [ ] `adk web` abre e agentes RAG v1/v2 funcionam
- [ ] `amldo-streamlit` abre interface
- [ ] Interface Streamlit processa documentos
- [ ] Pipeline usa embeddings reais (não dummy)
- [ ] `pytest` passa todos os testes
- [ ] `pytest --cov` mostra >80% coverage
- [ ] `black src/` não altera nada (já formatado)
- [ ] `ruff check src/` não reporta erros
- [ ] `mypy src/` passa type checking
- [ ] `pre-commit run --all-files` passa
- [ ] Notebooks executam sem erros
- [ ] Documentação está atualizada
- [ ] Scripts CLI funcionam (`amldo-build-index`, etc)

---

## Próximos Passos (Pós-Migração)

1. **Conectar agentes CrewAI ao pipeline**
   - Atualmente estão isolados, criar integração real

2. **Adicionar mais testes**
   - Aumentar coverage para >90%
   - Adicionar testes end-to-end

3. **Documentação de API**
   - Gerar docs com Sphinx ou MkDocs

4. **Performance**
   - Profiling do pipeline
   - Otimizações de embedding

5. **Features novas**
   - Ver `docs/08-melhorias-roadmap.md`

---

## Contato

**Equipe AMLDO**
**Data de criação deste guia**: 2025-11-14
