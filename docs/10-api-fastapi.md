# API REST FastAPI - AMLDO v0.3.0

**Versão:** 0.3.0
**Data:** 2025-11-16
**Status:** ✅ Implementado

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Instalação e Configuração](#instalação-e-configuração)
- [Executando a API](#executando-a-api)
- [Endpoints](#endpoints)
- [Modelos de Dados](#modelos-de-dados)
- [Sistema de Métricas](#sistema-de-métricas)
- [Exemplos de Uso](#exemplos-de-uso)
- [Deployment](#deployment)

---

## 🎯 Visão Geral

A API REST do AMLDO fornece acesso programático a todas as funcionalidades do sistema via HTTP. Construída com FastAPI, oferece:

- **Interface REST completa** para consultas RAG e processamento de documentos
- **Documentação automática** OpenAPI/Swagger em `/docs`
- **3 versões de RAG** selecionáveis (v1, v2, v3)
- **Sistema de métricas** com SQLite
- **Interface web** para usuários finais
- **Performance** com async/await

### Arquitetura

```
src/amldo/interfaces/api/
├── main.py              # App FastAPI principal
├── run.py               # Script de execução
├── dependencies.py      # Injeção de dependências
├── routers/             # Endpoints modulares
│   ├── query.py         # /api/ask, /api/health
│   ├── upload.py        # /api/upload, /api/process
│   └── metrics.py       # /api/metrics/*
├── models/              # Schemas Pydantic
│   ├── request.py       # QueryRequest, UploadRequest
│   └── response.py      # Respostas tipadas
├── templates/           # HTML (Jinja2)
│   ├── index.html
│   ├── chat.html
│   └── process.html
└── static/              # CSS, JS, imagens
    └── css/style.css
```

---

## 🔧 Instalação e Configuração

### 1. Instalar Dependências

```bash
# Opção 1: Via pyproject.toml (recomendado)
pip install -e ".[api]"

# Opção 2: Via requirements
pip install -r requirements/api.txt
```

**Dependências instaladas:**
- `fastapi>=0.110.0` - Framework web
- `uvicorn[standard]>=0.27.0` - Servidor ASGI
- `python-multipart>=0.0.9` - Upload de arquivos
- `jinja2>=3.1.0` - Templates HTML
- `PyMuPDF>=1.23.0` - Processamento de PDFs

### 2. Configurar Variáveis de Ambiente

Edite `.env`:

```bash
# Google API Key (obrigatória)
GOOGLE_API_KEY=sua_chave_aqui

# API Settings (opcionais)
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False
DEFAULT_RAG_VERSION=v2

# Outros settings...
LOG_LEVEL=INFO
```

### 3. Verificar Estrutura de Dados

A API precisa dos seguintes diretórios:

```bash
data/
├── raw/                  # PDFs para processamento
├── vector_db/            # Índice FAISS
│   └── v1_faiss_vector_db/
├── processed/            # CSVs de artigos
│   ├── v1_artigos_0.csv
│   └── v1_processed_articles.csv
└── metrics/              # Banco SQLite (criado automaticamente)
    └── metrics.db
```

---

## 🚀 Executando a API

### Método 1: Via script instalado (recomendado)

```bash
amldo-api
```

### Método 2: Via uvicorn diretamente

```bash
uvicorn amldo.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Método 3: Via Python

```python
from amldo.interfaces.api.run import main
main()
```

### Acessar a Aplicação

Após iniciar, acesse:

- **Página inicial**: http://localhost:8000/
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc
- **Chat RAG**: http://localhost:8000/consulta
- **Processamento**: http://localhost:8000/processamento

---

## 📡 Endpoints

### Consultas RAG

#### `POST /api/ask`

Faz uma consulta ao sistema RAG.

**Request:**
```json
{
  "question": "Qual é o limite para dispensa de licitação?",
  "rag_version": "v2"
}
```

**Parâmetros:**
- `question` (string, obrigatório): Pergunta do usuário
- `rag_version` (string, opcional): Versão do RAG (`v1`, `v2`, `v3`). Default: `v2`

**Response (200):**
```json
{
  "answer": "De acordo com a Lei 14.133/2021...",
  "rag_version": "v2",
  "question": "Qual é o limite para dispensa de licitação?",
  "response_time_ms": 1523.4
}
```

**Erros:**
- `400`: Pergunta vazia ou versão RAG inválida
- `500`: Erro no retrieval, LLM ou interno

**Exemplo curl:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Limite de dispensa?", "rag_version": "v2"}'
```

---

### Upload e Processamento

#### `POST /api/upload`

Faz upload de múltiplos arquivos PDF.

**Request:** `multipart/form-data` com campo `files`

**Response (200):**
```json
{
  "saved": ["lei_14133.pdf", "decreto_10024.pdf"],
  "failed": [
    {"file": "documento.txt", "error": "Tipo inválido - apenas PDF aceito"}
  ]
}
```

**Comportamento:**
- Apenas arquivos `.pdf` são aceitos
- Arquivos duplicados ganham sufixo numérico (`_1`, `_2`, etc.)
- Salvos em `data/raw/`

**Exemplo curl:**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "files=@lei_14133.pdf" \
  -F "files=@decreto_10024.pdf"
```

---

#### `POST /api/process`

Processa todos os PDFs em `data/raw/` e atualiza o índice FAISS.

**Request:** Nenhum parâmetro necessário

**Response (200):**
```json
{
  "processed": 3,
  "total_chunks": 450,
  "files": [
    {"file": "lei.pdf", "chunks": 150},
    {"file": "decreto.pdf", "chunks": 200},
    {"file": "portaria.pdf", "chunks": 100}
  ],
  "duration_seconds": 45.5
}
```

**Workflow:**
1. Lê todos os `.pdf` em `data/raw/`
2. Extrai texto com PyMuPDF
3. Divide em chunks (RecursiveCharacterTextSplitter)
4. Cria embeddings (sentence-transformers)
5. Atualiza índice FAISS incrementalmente
6. Registra métricas no SQLite

**Erros:**
- `404`: Nenhum PDF encontrado
- `500`: Erro ao processar

**Exemplo curl:**
```bash
curl -X POST "http://localhost:8000/api/process"
```

**⚠️ Nota:** Este endpoint pode demorar vários minutos para PDFs grandes.

---

### Métricas

#### `GET /api/metrics/stats`

Retorna estatísticas gerais do sistema.

**Response (200):**
```json
{
  "rag_stats": [
    {
      "version": "v1",
      "queries": 50,
      "avg_response_time_ms": 1200.5,
      "min_response_time_ms": 800.2,
      "max_response_time_ms": 2500.0,
      "successful": 48,
      "failed": 2
    },
    {
      "version": "v2",
      "queries": 150,
      "avg_response_time_ms": 1500.3,
      "min_response_time_ms": 900.0,
      "max_response_time_ms": 3000.0,
      "successful": 148,
      "failed": 2
    }
  ],
  "total_files_processed": 12,
  "total_chunks_indexed": 5430
}
```

**Dados incluem:**
- Estatísticas por versão RAG (v1, v2, v3)
- Contagem de queries
- Tempos de resposta (médio, mínimo, máximo)
- Taxa de sucesso/falha
- Total de arquivos e chunks processados

---

#### `GET /api/metrics/processing-history`

Retorna histórico de processamentos.

**Parâmetros:**
- `limit` (int, opcional): Máximo de registros (default: 100, max: 1000)

**Response (200):**
```json
{
  "history": [
    {
      "id": 5,
      "timestamp": "2025-11-16T14:30:00",
      "files_processed": 3,
      "total_chunks": 450,
      "duration_seconds": 45.5,
      "details": "[{\"file\":\"lei.pdf\",\"chunks\":150}]"
    }
  ]
}
```

**Exemplo:**
```bash
curl "http://localhost:8000/api/metrics/processing-history?limit=50"
```

---

#### `GET /api/metrics/query-history`

Retorna histórico de consultas RAG.

**Parâmetros:**
- `limit` (int, opcional): Máximo de registros (default: 100, max: 1000)
- `rag_version` (string, opcional): Filtrar por versão (`v1`, `v2`, `v3`)

**Response (200):**
```json
{
  "history": [
    {
      "id": 10,
      "timestamp": "2025-11-16T14:25:00",
      "rag_version": "v2",
      "question": "Limite de dispensa?",
      "response_time_ms": 1523.4,
      "success": 1,
      "error_message": null
    }
  ]
}
```

**Exemplo:**
```bash
# Todas as queries
curl "http://localhost:8000/api/metrics/query-history?limit=100"

# Apenas v2
curl "http://localhost:8000/api/metrics/query-history?rag_version=v2&limit=50"
```

---

#### `GET /api/metrics/health`

Health check do sistema de métricas.

**Response (200):**
```json
{
  "status": "ok",
  "metrics_enabled": true,
  "db_path": "/path/to/data/metrics/metrics.db",
  "db_exists": true
}
```

---

### Health Checks

#### `GET /health`

Health check geral da API.

**Response (200):**
```json
{
  "status": "ok",
  "version": "0.3.0",
  "service": "AMLDO API",
  "rag_versions": ["v1", "v2", "v3"],
  "default_rag_version": "v2"
}
```

---

## 📦 Modelos de Dados

### QueryRequest

```python
class QueryRequest(BaseModel):
    question: str          # Pergunta (min: 1, max: 1000 chars)
    rag_version: Optional[Literal["v1", "v2", "v3"]] = "v2"
```

### QueryResponse

```python
class QueryResponse(BaseModel):
    answer: str            # Resposta do LLM
    rag_version: str       # Versão usada
    question: str          # Pergunta original
    response_time_ms: Optional[float]  # Tempo de resposta
```

### UploadResponse

```python
class UploadResponse(BaseModel):
    saved: List[str]       # Arquivos salvos
    failed: List[Dict[str, str]]  # Falhas com motivo
```

### ProcessResponse

```python
class ProcessResponse(BaseModel):
    processed: int         # Arquivos processados
    total_chunks: int      # Total de chunks criados
    files: List[Dict[str, Any]]  # Detalhes por arquivo
    duration_seconds: Optional[float]  # Tempo de processamento
```

### MetricsResponse

```python
class MetricsResponse(BaseModel):
    rag_stats: List[Dict[str, Any]]  # Stats por versão
    total_files_processed: int
    total_chunks_indexed: int
```

---

## 💾 Sistema de Métricas

### Banco de Dados SQLite

**Localização:** `data/metrics/metrics.db`

**Tabelas:**

#### `processing_history`
```sql
CREATE TABLE processing_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    files_processed INTEGER NOT NULL,
    total_chunks INTEGER NOT NULL,
    duration_seconds REAL,
    details TEXT
);
```

#### `query_history`
```sql
CREATE TABLE query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    rag_version TEXT NOT NULL,
    question TEXT NOT NULL,
    response_time_ms REAL,
    success BOOLEAN DEFAULT 1,
    error_message TEXT
);
```

### Vantagens vs JSON (AMLDO_W)

| Recurso | JSON | SQLite |
|---------|------|--------|
| Queries complexas | ❌ Lento | ✅ Rápido (SQL) |
| Agregações | ❌ Manual | ✅ Nativo (AVG, COUNT) |
| Índices | ❌ Não | ✅ Sim |
| Escalabilidade | ❌ Limitada | ✅ Milhares de registros |
| Transações | ❌ Não | ✅ ACID |
| Recuperação de espaço | ❌ Não | ✅ VACUUM |

---

## 🔍 Exemplos de Uso

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Fazer uma consulta RAG
response = requests.post(
    f"{BASE_URL}/api/ask",
    json={"question": "Qual o limite de dispensa?", "rag_version": "v2"}
)
result = response.json()
print(result["answer"])

# Upload de PDF
with open("lei.pdf", "rb") as f:
    files = {"files": ("lei.pdf", f, "application/pdf")}
    response = requests.post(f"{BASE_URL}/api/upload", files=files)
print(response.json()["saved"])

# Processar PDFs
response = requests.post(f"{BASE_URL}/api/process")
print(f"Processados: {response.json()['processed']}")

# Obter estatísticas
response = requests.get(f"{BASE_URL}/api/metrics/stats")
stats = response.json()
for rag in stats["rag_stats"]:
    print(f"{rag['version']}: {rag['queries']} queries, avg {rag['avg_response_time_ms']}ms")
```

### JavaScript (fetch)

```javascript
// Consulta RAG
const response = await fetch('http://localhost:8000/api/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    question: 'Limite de dispensa?',
    rag_version: 'v2'
  })
});
const data = await response.json();
console.log(data.answer);

// Upload de arquivo
const formData = new FormData();
formData.append('files', fileInput.files[0]);

const uploadResponse = await fetch('http://localhost:8000/api/upload', {
  method: 'POST',
  body: formData
});
console.log(await uploadResponse.json());
```

### cURL

```bash
# Consulta simples
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Teste"}'

# Upload de PDF
curl -X POST "http://localhost:8000/api/upload" \
  -F "files=@documento.pdf"

# Processar documentos
curl -X POST "http://localhost:8000/api/process"

# Estatísticas
curl "http://localhost:8000/api/metrics/stats" | jq

# Histórico filtrado
curl "http://localhost:8000/api/metrics/query-history?rag_version=v2&limit=10" | jq
```

---

## 🚀 Deployment

### Desenvolvimento

```bash
# Com auto-reload
API_DEBUG=True amldo-api

# Ou
uvicorn amldo.interfaces.api.main:app --reload --port 8000
```

### Produção

```bash
# Via uvicorn (single worker)
uvicorn amldo.interfaces.api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4

# Via gunicorn (múltiplos workers)
gunicorn amldo.interfaces.api.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements/api.txt requirements/base.txt ./
RUN pip install --no-cache-dir -r api.txt -r base.txt

COPY src/ ./src/
COPY data/ ./data/
COPY pyproject.toml .

RUN pip install -e .

EXPOSE 8000

CMD ["amldo-api"]
```

**Build e Run:**
```bash
docker build -t amldo-api .
docker run -p 8000:8000 -v $(pwd)/data:/app/data amldo-api
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name amldo.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /app/src/amldo/interfaces/api/static;
    }
}
```

---

## 🔐 Segurança

### Recomendações para Produção

1. **CORS:** Configurar domínios permitidos em `main.py`
   ```python
   allow_origins=["https://example.com"]
   ```

2. **Rate Limiting:** Usar middleware ou nginx
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

3. **HTTPS:** Sempre usar TLS em produção

4. **API Keys:** Adicionar autenticação
   ```python
   from fastapi.security import APIKeyHeader
   ```

5. **Validação:** Pydantic já valida inputs

6. **Logs:** Configurar logging adequado
   ```bash
   LOG_LEVEL=WARNING
   ```

---

## 📚 Recursos Adicionais

- **Documentação FastAPI:** https://fastapi.tiangolo.com/
- **OpenAPI Spec:** http://localhost:8000/openapi.json
- **Código fonte:** `src/amldo/interfaces/api/`
- **Testes:** `tests/unit/test_api_endpoints.py`

---

**Última atualização:** 2025-11-16
**Versão da API:** 0.3.0
