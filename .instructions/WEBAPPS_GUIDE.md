# 🌐 Guia das WebApps - AMLDO

> **Duas versões diferentes** do projeto AMLDO web

---

## 📋 Resumo

O projeto AMLDO possui **DUAS webapps FastAPI diferentes**:

| WebApp | Localização | Porta | Versão | Status |
|--------|-------------|-------|--------|--------|
| **Antiga (Original)** | `AMLDO_W/AMLDO/webapp/` | 8001 | POC | 🟡 Legado |
| **Nova (v0.3.0)** | `src/amldo/interfaces/api/` | 8000 | Produção | ✅ Atual |

---

## 🔍 Diferenças

### WebApp ANTIGA (Original)

**Localização**: `AMLDO_W/AMLDO/webapp/main.py`

**Características**:
- ✅ FastAPI simples e direto
- ✅ Interface HTML básica
- ✅ Upload de PDFs
- ✅ Query RAG simples
- ⚪ Sem sistema de métricas
- ⚪ Sem múltiplas versões de RAG
- ⚪ Sem documentação Swagger extensa

**Tecnologias**:
- FastAPI
- Jinja2 templates
- HuggingFace Embeddings
- FAISS

**Estrutura**:
```
AMLDO_W/AMLDO/
├── webapp/
│   ├── main.py          # Aplicação FastAPI
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS
├── rag_v1/             # RAG versão 1
├── rag_v2/             # RAG versão 2
└── data/               # Dados compartilhados
```

**Porta**: 8001

---

### WebApp NOVA (v0.3.0)

**Localização**: `src/amldo/interfaces/api/`

**Características**:
- ✅ FastAPI completo e moderno
- ✅ Interface web com Bootstrap 5
- ✅ 8+ endpoints REST
- ✅ 3 versões de RAG (v1, v2, v3)
- ✅ Sistema de métricas (SQLite)
- ✅ Documentação Swagger automática
- ✅ Modelos Pydantic
- ✅ Health checks
- ✅ CORS configurável
- ✅ Testes automatizados

**Tecnologias**:
- FastAPI
- Pydantic (validação)
- Jinja2 templates
- Bootstrap 5
- SQLite (métricas)
- Sentence Transformers
- FAISS
- LangChain

**Estrutura**:
```
src/amldo/
├── interfaces/
│   └── api/
│       ├── main.py         # App FastAPI
│       ├── run.py          # Script execução
│       ├── routers/        # Endpoints organizados
│       │   ├── queries.py
│       │   ├── pipeline.py
│       │   └── metrics.py
│       ├── models/         # Pydantic schemas
│       ├── templates/      # HTML Jinja2
│       └── static/         # CSS, assets
├── rag/
│   ├── v1/                # RAG básico
│   ├── v2/                # RAG MMR
│   └── v3/                # RAG Similarity
└── utils/
    └── metrics.py         # Sistema métricas
```

**Porta**: 8000

---

## 🚀 Como Executar

### 1️⃣ Executar WebApp ANTIGA (Porta 8001)

```bash
cd /mnt/d/PYTHON/AMLDO

# Executar webapp antiga
./scripts/run_webapp_old.sh
```

**Acesse**: http://localhost:8001

**Requirements**:
- `.env` em `AMLDO_W/AMLDO/`
- Dependências básicas

---

### 2️⃣ Executar WebApp NOVA (Porta 8000)

```bash
cd /mnt/d/PYTHON/AMLDO

# Executar webapp nova
./scripts/run_webapp_new.sh
```

**Acesse**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Chat: http://localhost:8000/consulta
- Processamento: http://localhost:8000/processamento
- Métricas: http://localhost:8000/metricas

**Requirements**:
- `.env` na raiz com `GOOGLE_API_KEY`
- Virtual environment instalado
- `pip install -e ".[api]"`

---

### 3️⃣ Executar AMBAS Simultaneamente

```bash
cd /mnt/d/PYTHON/AMLDO

# Executar ambas webapps
./scripts/run_both_webapps.sh

# Parar ambas
./scripts/run_both_webapps.sh stop
```

**URLs**:
- WebApp Antiga: http://localhost:8001
- WebApp Nova: http://localhost:8000

**Logs**:
```bash
# Ver logs webapp antiga
tail -f /tmp/webapp_old.log

# Ver logs webapp nova
tail -f /tmp/webapp_new.log
```

---

## 📊 Comparação de Features

| Feature | WebApp Antiga | WebApp Nova v0.3.0 |
|---------|--------------|-------------------|
| **FastAPI** | ✅ Básico | ✅ Completo |
| **Endpoints REST** | ~3 | 8+ |
| **Interface Web** | ✅ HTML simples | ✅ Bootstrap 5 |
| **Upload PDFs** | ✅ | ✅ |
| **Query RAG** | ✅ v1 apenas | ✅ v1, v2, v3 |
| **Sistema Métricas** | ❌ | ✅ SQLite |
| **Documentação Swagger** | ⚪ Básica | ✅ Completa |
| **Pydantic Models** | ❌ | ✅ |
| **Health Checks** | ❌ | ✅ |
| **Testes Automatizados** | ❌ | ✅ 86 testes |
| **CORS** | ⚪ Básico | ✅ Configurável |
| **Docker** | ❌ | ✅ |
| **CI/CD** | ❌ | ✅ GitHub Actions |
| **Métricas de Queries** | ❌ | ✅ |
| **Histórico Processamento** | ❌ | ✅ |

---

## 🎯 Quando Usar Cada Uma?

### Use a WebApp ANTIGA quando:

- 🔸 Precisa de algo **simples e rápido**
- 🔸 Quer apenas **testar RAG básico**
- 🔸 Não precisa de **métricas ou tracking**
- 🔸 Está fazendo **prototipagem rápida**

### Use a WebApp NOVA quando:

- 🔹 Quer a **versão mais atualizada**
- 🔹 Precisa de **múltiplas versões de RAG**
- 🔹 Quer **métricas e estatísticas**
- 🔹 Precisa de **API REST completa**
- 🔹 Está em **produção**
- 🔹 Quer **testes e qualidade**

---

## 🔄 Migração

Se você está usando a **WebApp Antiga** e quer **migrar para a Nova**:

### Passo 1: Dados

Os dados (vector store, CSVs) são **compartilhados**:
```
data/
├── vector_db/              # Usado por ambas
├── processed/              # Usado por ambas
└── raw/                    # Usado por ambas
```

✅ **Não precisa reprocessar documentos!**

### Passo 2: Configuração

A WebApp Nova requer:
```bash
# Copiar .env
cp .env.example .env

# Adicionar GOOGLE_API_KEY
nano .env
```

### Passo 3: Instalação

```bash
# Instalar dependências da nova versão
pip install -e ".[api]"
```

### Passo 4: Executar

```bash
./scripts/run_webapp_new.sh
```

---

## 🐛 Troubleshooting

### WebApp Antiga não inicia

**Problema**: Erro ao executar `run_webapp_old.sh`

**Soluções**:
```bash
# 1. Verificar .env
ls -la AMLDO_W/AMLDO/.env

# 2. Verificar dependências
cd AMLDO_W/AMLDO
pip install -r requirements.txt

# 3. Verificar porta
lsof -i :8001
```

### WebApp Nova não inicia

**Problema**: Erro ao executar `run_webapp_new.sh`

**Soluções**:
```bash
# 1. Verificar .env na raiz
cat .env | grep GOOGLE_API_KEY

# 2. Reinstalar
pip install -e ".[api]"

# 3. Verificar porta
lsof -i :8000
```

### Conflito de portas

**Problema**: As duas webapps usam a mesma porta

**Solução**: As webapps usam portas **diferentes**:
- Antiga: 8001
- Nova: 8000

Se ainda houver conflito:
```bash
# Mudar porta da webapp antiga
# Edite scripts/run_webapp_old.sh, linha com uvicorn:
uvicorn main:app --reload --port 8002  # ← mudar aqui
```

---

## 📚 Arquivos de Script

| Script | Função |
|--------|--------|
| `run_webapp_old.sh` | Executa webapp antiga (8001) |
| `run_webapp_new.sh` | Executa webapp nova (8000) |
| `run_both_webapps.sh` | Executa ambas simultaneamente |

Todos em: `scripts/`

---

## 💡 Recomendação

**Para novos projetos e produção**: Use a **WebApp Nova (v0.3.0)** 🚀

**Para estudos e testes rápidos**: A **WebApp Antiga** ainda funciona ✅

**Para comparação**: Execute **ambas** com `run_both_webapps.sh` 🔄

---

## 📖 Documentação Adicional

- [API FastAPI Completa](docs/10-api-fastapi.md)
- [CI/CD e Deployment](docs/12-ci-cd-deployment.md)
- [Testes Automatizados](docs/11-testes-automatizados.md)
- [README Principal](README.md)

---

**Última atualização**: 2025-11-16
**Versão atual**: v0.3.0
