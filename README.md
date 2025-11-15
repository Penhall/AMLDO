# AMLDO — Sistema RAG para Legislação de Licitações

> **Sistema de Retrieval-Augmented Generation (RAG)** especializado em legislação brasileira de licitações, compliance e governança.

[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0-green.svg)](https://langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

##  📋 Visão Geral

O **AMLDO** permite consultas em linguagem natural sobre legislação de licitações, retornando respostas precisas e fundamentadas exclusivamente nos documentos legais indexados.

### Principais Características

- ✅ **Busca Semântica Avançada** - Embeddings multilíngues + FAISS
- ✅ **Respostas Fundamentadas** - Cita artigos e leis (sem alucinações)
- ✅ **Múltiplas Interfaces** - Google ADK (CLI) + Streamlit (Web)
- ✅ **2 Versões do RAG** - Básico (v1) e Aprimorado com contexto hierárquico (v2)
- ✅ **Pipeline Completo** - Ingestão → Estruturação → Indexação → Consulta
- ✅ **4 Documentos Indexados** - Lei 14.133, LGPD, LCP 123, Decreto 10.024

### Tecnologias

- **Python 3.11+** | **LangChain** | **FAISS** | **Sentence Transformers** | **Gemini 2.5 Flash** | **Google ADK** | **Streamlit**

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
pip install -e ".[adk,streamlit]"

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY

# 5. Rodar sistema
adk web  # Interface Google ADK
# ou
streamlit run src/amldo/interfaces/streamlit/app.py  # Interface Streamlit
```

**Google ADK:** http://localhost:8080 (selecione agente `rag_v2`)
**Streamlit:** http://localhost:8501

**Teste uma pergunta:**
```
Qual é o limite de valor para dispensa de licitação em obras?
```

---

## 📁 Estrutura do Projeto (v0.2.0)

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
│       │   └── v2/                 # RAG avançado (contexto hierárquico)
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
│       │   ├── adk/                # Interface Google ADK
│       │   └── streamlit/          # Interface Streamlit
│       │       ├── app.py
│       │       └── pages/
│       │           ├── 01_Pipeline.py     # Processamento de docs
│       │           └── 02_RAG_Query.py    # Consultas RAG
│       │
│       └── utils/                  # Utilidades compartilhadas
│
├── tests/                          # Testes
│   ├── unit/                       # Testes unitários
│   ├── integration/                # Testes de integração
│   └── conftest.py                 # Fixtures pytest
│
├── notebooks/                      # Análise e experimentação
│   ├── 01_data_processing.ipynb
│   ├── 02_vector_bank.ipynb
│   └── 03_rag_study.ipynb
│
├── data/                           # Dados do projeto
│   ├── raw/                        # PDFs originais (4 leis)
│   ├── split_docs/                 # Documentos hierarquicamente divididos
│   ├── processed/                  # CSVs processados
│   └── vector_db/                  # Índice FAISS
│
├── docs/                           # Documentação completa
│   ├── 00-visao-geral.md
│   ├── 01-arquitetura-tecnica.md
│   └── ...
│
├── requirements/                   # Requirements organizados
│   ├── base.txt                    # Core dependencies
│   ├── adk.txt                     # Google ADK
│   ├── streamlit.txt               # Streamlit interface
│   ├── agents.txt                  # CrewAI agents
│   ├── dev.txt                     # Development tools
│   └── notebooks.txt               # Jupyter notebooks
│
├── pyproject.toml                  # Configuração moderna Python
├── setup.py                        # Setup para instalação
├── .env.example                    # Template de variáveis de ambiente
├── .pre-commit-config.yaml         # Pre-commit hooks
├── MIGRATION.md                    # Guia de migração v0.1 → v0.2
└── README.md                       # Este arquivo
```

---

## 🎯 Uso

### Interface Google ADK (Recomendado para consultas)

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar interface ADK
adk web

# Acesse http://localhost:8080
# Selecione agente: rag_v2 (recomendado) ou rag_v1
```

**Diferenças entre v1 e v2:**
- **v1**: Contexto direto, mais rápido
- **v2**: Contexto hierárquico estruturado (Lei → Título → Capítulo → Artigo)

### Interface Streamlit (Web completa)

```bash
# Executar app Streamlit
streamlit run src/amldo/interfaces/streamlit/app.py
# ou
python -m streamlit run src/amldo/interfaces/streamlit/app.py

# Acesse http://localhost:8501
```

**Páginas disponíveis:**
- **Home**: Visão geral do sistema
- **Pipeline**: Upload e processamento de novos documentos
- **RAG Query**: Consultas à base de conhecimento

### Scripts CLI

```bash
# Processar novo documento
amldo-process --input data/raw/nova_lei.pdf --output data/processed/

# Criar índice FAISS
amldo-build-index --source data/processed/artigos.jsonl --output data/vector_db/
```

---

## 📖 Documentação Completa

📚 **[Acesse a documentação completa em `/docs`](docs/README.md)**

### Guias Principais

| Documento | Descrição | Para Quem |
|-----------|-----------|-----------|
| **[Visão Geral](docs/00-visao-geral.md)** | Introdução, objetivos e contexto | Todos |
| **[Arquitetura Técnica](docs/01-arquitetura-tecnica.md)** | Componentes, camadas e decisões | Desenvolvedores |
| **[Pipeline RAG](docs/02-pipeline-rag.md)** | Como funciona o RAG internamente | Data Scientists |
| **[Estrutura de Dados](docs/03-estrutura-dados.md)** | Organização de dados e metadados | Data Engineers |
| **[Guia do Desenvolvedor](docs/04-guia-desenvolvedor.md)** | Setup, desenvolvimento e debugging | Desenvolvedores |
| **[Comandos e Fluxos](docs/05-comandos-fluxos.md)** | Comandos úteis e workflows | Todos |
| **[Estado Atual](docs/06-estado-atual.md)** | Funcionalidades e limitações | Gestores |
| **[Casos de Uso](docs/07-casos-de-uso.md)** | Exemplos práticos | Usuários finais |
| **[Melhorias e Roadmap](docs/08-melhorias-roadmap.md)** | Próximos passos | Stakeholders |
| **[Guia de Migração](MIGRATION.md)** | v0.1 → v0.2 | Desenvolvedores |

---

## 🧪 Desenvolvimento

### Setup para Desenvolvimento

```bash
# Instalar com dependências de desenvolvimento
pip install -e ".[dev,adk,streamlit,agents,notebooks]"

# Instalar pre-commit hooks
pre-commit install

# Rodar testes
pytest

# Com coverage
pytest --cov=src/amldo --cov-report=html

# Formatar código
black src/

# Lint
ruff check src/

# Type checking
mypy src/
```

### Estrutura de Testes

```
tests/
├── unit/                   # Testes unitários
│   ├── test_config.py
│   ├── test_ingestion.py
│   ├── test_structure.py
│   └── test_indexer.py
├── integration/            # Testes de integração
└── conftest.py             # Fixtures compartilhadas
```

### Pre-commit Hooks

Configurados automaticamente para:
- ✅ Formatação com Black
- ✅ Linting com Ruff
- ✅ Type checking com mypy
- ✅ Validações gerais (trailing whitespace, YAML, etc)

---

## 🔧 Configuração

Todas as configurações são centralizadas em `src/amldo/core/config.py` e podem ser sobrescritas via `.env`:

```bash
# API Keys (OBRIGATÓRIO)
GOOGLE_API_KEY=sua_chave_aqui

# Modelos
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LLM_MODEL=gemini-2.5-flash

# RAG
SEARCH_K=12
SEARCH_TYPE=mmr

# Paths
VECTOR_DB_PATH=data/vector_db/v1_faiss_vector_db

# Ambiente
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=false
```

Ver `.env.example` para lista completa de variáveis.

---

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit suas mudanças: `git commit -m 'feat: adiciona nova feature'`
4. Push para a branch: `git push origin feature/minha-feature`
5. Abra um Pull Request

**Padrões de commit:** Usamos [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## 📞 Contato

**Equipe AMLDO**
GitHub: [@Penhall/AMLDO](https://github.com/Penhall/AMLDO)

---

## 🎯 Roadmap

Ver [docs/08-melhorias-roadmap.md](docs/08-melhorias-roadmap.md) para detalhes completos.

**Próximas features:**
- [ ] Integração completa de agentes CrewAI
- [ ] Análise de editais vs documentos empresariais
- [ ] Cache de embeddings
- [ ] Suporte a mais fontes de dados
- [ ] API REST
- [ ] Deploy em produção

---

## 🙏 Agradecimentos

- Google ADK pela excelente framework de agentes
- LangChain pela infraestrutura RAG
- Comunidade open-source de NLP em português

---

**Versão:** 0.2.0
**Última atualização:** 2025-11-14
