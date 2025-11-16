# Inventário de Mudanças - AMLDO v0.2.0 → v0.3.0

**Data:** 2025-11-15
**Versão Origem:** AMLDO v0.2.0 + AMLDO_W
**Versão Destino:** AMLDO v0.3.0 (Integrada)

---

## 📋 Sumário

Este documento lista **TODAS** as mudanças planejadas e executadas na migração e integração do AMLDO_W para a estrutura v0.2.0.

---

## 🆕 Novos Arquivos e Diretórios

### Estrutura RAG v3

| Caminho | Tipo | Origem | Descrição |
|---------|------|--------|-----------|
| `src/amldo/rag/v3/` | Diretório | NOVO | RAG v3 com similarity search |
| `src/amldo/rag/v3/__init__.py` | Arquivo | NOVO | Exports do módulo RAG v3 |
| `src/amldo/rag/v3/agent.py` | Arquivo | Migrado de `AMLDO_W/rag_v3_sim/agent.py` | Google ADK agent para RAG v3 |
| `src/amldo/rag/v3/tools.py` | Arquivo | Migrado de `AMLDO_W/rag_v3_sim/tools.py` | Funções RAG v3 (similarity search) |

**Mudanças no código:**
- ✅ Substituir hardcoded `SEARCH_TYPE = "similarity"` por `settings.rag_v3_search_type`
- ✅ Substituir `K = 12` por `settings.rag_v3_k`
- ✅ Adicionar exception handling usando `amldo.core.exceptions`
- ✅ Adaptar imports para estrutura `src/amldo/`

### Estrutura API FastAPI

| Caminho | Tipo | Origem | Descrição |
|---------|------|--------|-----------|
| `src/amldo/interfaces/api/` | Diretório | NOVO | API REST FastAPI |
| `src/amldo/interfaces/api/__init__.py` | Arquivo | NOVO | Exports do módulo API |
| `src/amldo/interfaces/api/main.py` | Arquivo | Adaptado de `AMLDO_W/webapp/main.py` | App FastAPI principal |
| `src/amldo/interfaces/api/dependencies.py` | Arquivo | NOVO | Dependências compartilhadas (DB, settings, etc) |
| `src/amldo/interfaces/api/run.py` | Arquivo | NOVO | Script para executar API |

#### Routers

| Caminho | Tipo | Função Original (AMLDO_W) | Descrição |
|---------|------|---------------------------|-----------|
| `src/amldo/interfaces/api/routers/` | Diretório | NOVO | Routers modulares |
| `src/amldo/interfaces/api/routers/__init__.py` | Arquivo | NOVO | Exports de routers |
| `src/amldo/interfaces/api/routers/query.py` | Arquivo | `@app.post("/api/ask")` | Endpoint de consultas RAG |
| `src/amldo/interfaces/api/routers/upload.py` | Arquivo | `@app.post("/api/upload")` + `@app.post("/api/process")` | Upload e processamento PDFs |
| `src/amldo/interfaces/api/routers/metrics.py` | Arquivo | `@app.get("/api/metrics/embedding_history")` | Endpoints de métricas |

#### Models Pydantic

| Caminho | Tipo | Descrição |
|---------|------|-----------|
| `src/amldo/interfaces/api/models/` | Diretório | NOVO (modelos Pydantic) |
| `src/amldo/interfaces/api/models/__init__.py` | Arquivo | Exports |
| `src/amldo/interfaces/api/models/request.py` | Arquivo | `QueryRequest`, `UploadRequest` |
| `src/amldo/interfaces/api/models/response.py` | Arquivo | `QueryResponse`, `UploadResponse`, `ProcessResponse`, `MetricsResponse` |

#### Templates e Estáticos

| Caminho | Tipo | Origem | Descrição |
|---------|------|--------|-----------|
| `src/amldo/interfaces/api/templates/` | Diretório | Migrado de `AMLDO_W/webapp/templates/` | Templates Jinja2 |
| `src/amldo/interfaces/api/templates/index.html` | Arquivo | Migrado | Página inicial |
| `src/amldo/interfaces/api/templates/chat.html` | Arquivo | Migrado | Interface de chat |
| `src/amldo/interfaces/api/templates/process.html` | Arquivo | Migrado | Interface de processamento |
| `src/amldo/interfaces/api/static/` | Diretório | Migrado de `AMLDO_W/webapp/static/` | Arquivos estáticos |
| `src/amldo/interfaces/api/static/css/` | Diretório | Migrado | Estilos CSS |
| `src/amldo/interfaces/api/static/js/` | Diretório | Migrado | Scripts JavaScript |
| `src/amldo/interfaces/api/static/img/` | Diretório | NOVO | Imagens |

### Sistema de Métricas

| Caminho | Tipo | Origem | Descrição |
|---------|------|--------|-----------|
| `src/amldo/utils/metrics.py` | Arquivo | Adaptado de lógica em `AMLDO_W/webapp/main.py` | Sistema de métricas com SQLite |
| `data/metrics/` | Diretório | NOVO | Armazenamento de métricas |
| `data/metrics/metrics.db` | Arquivo | NOVO (criado em runtime) | Banco SQLite de métricas |

**Mudanças:**
- ❌ **Removido:** JSON `data/metrics/embedding_history.json` (AMLDO_W)
- ✅ **Adicionado:** SQLite `data/metrics/metrics.db`
- ✅ Tabelas: `processing_history`, `query_history`

### Testes

| Caminho | Tipo | Descrição |
|---------|------|-----------|
| `tests/unit/test_rag_v3.py` | Arquivo | NOVO - Testes unitários RAG v3 |
| `tests/unit/test_api_endpoints.py` | Arquivo | NOVO - Testes endpoints API |
| `tests/unit/test_metrics.py` | Arquivo | NOVO - Testes sistema métricas |
| `tests/integration/test_api_integration.py` | Arquivo | NOVO - Testes integração API |
| `tests/fixtures/test_document.pdf` | Arquivo | NOVO - PDF de teste |

### Documentação

| Caminho | Tipo | Descrição |
|---------|------|-----------|
| `docs/09-comparacao-versoes.md` | Arquivo | ✅ CRIADO - Comparação v0.2 vs AMLDO_W |
| `docs/10-api-fastapi.md` | Arquivo | NOVO - Documentação API REST |
| `docs/PLANO-MIGRACAO.md` | Arquivo | ✅ CRIADO - Este plano |
| `docs/INVENTARIO-MUDANCAS.md` | Arquivo | ✅ CRIADO - Este inventário |

---

## 📝 Arquivos Modificados

### Configuração

| Arquivo | Mudanças | Linhas Adicionadas | Linhas Removidas |
|---------|----------|-------------------|------------------|
| `src/amldo/core/config.py` | Adicionar settings RAG v3 e API | ~30 | 0 |
| `pyproject.toml` | Adicionar dependências FastAPI, script `amldo-api` | ~15 | 0 |
| `requirements/base.txt` | - | 0 | 0 |
| `requirements/api.txt` | **NOVO:** FastAPI, uvicorn, jinja2, python-multipart | ~10 | 0 |
| `.env.example` | Adicionar variáveis API (API_HOST, API_PORT) | ~5 | 0 |

**Detalhes de `src/amldo/core/config.py`:**

```python
# Adicionado:
class Settings(BaseSettings):
    # ... existentes

    # RAG v3 Settings
    rag_v3_enabled: bool = Field(True, description="Habilitar RAG v3")
    rag_v3_search_type: str = Field("similarity", regex="^(similarity|mmr)$")
    rag_v3_k: int = Field(12, ge=1, le=50)

    # API Settings
    api_host: str = Field("0.0.0.0", description="Host da API FastAPI")
    api_port: int = Field(8000, ge=1000, le=65535)
    api_debug: bool = Field(False, description="Debug mode para API")

    # Default RAG version for API
    default_rag_version: str = Field("v2", regex="^(v1|v2|v3)$")
```

### README

| Arquivo | Seção Modificada | Mudanças |
|---------|------------------|----------|
| `README.md` | Seção "Uso" | Adicionar seção "Interface FastAPI" |
| `README.md` | Seção "Estrutura do Projeto" | Atualizar árvore de diretórios |
| `README.md` | Seção "Novidades v0.3.0" | **NOVA SEÇÃO** |
| `README.md` | Badge de versão | `0.2.0` → `0.3.0` |
| `README.md` | Última atualização | `2025-11-15` → data de release |

### CLAUDE.md

| Seção | Mudanças |
|-------|----------|
| "Running the Application" | Adicionar Option 4: FastAPI |
| "Architecture" | Adicionar `interfaces/api/` |
| "RAG Pipeline" | Adicionar descrição RAG v3 |
| "Important Notes" | Adicionar notas sobre API e métricas |

### Interfaces ADK

| Arquivo | Mudanças |
|---------|----------|
| `src/amldo/interfaces/adk/agent_loader.py` | Registrar `rag_v3` como agente disponível |

**Código a adicionar:**
```python
# src/amldo/interfaces/adk/agent_loader.py
from amldo.rag.v3.agent import root_agent as rag_v3_agent

AVAILABLE_AGENTS = {
    "rag_v1": rag_v1_agent,
    "rag_v2": rag_v2_agent,
    "rag_v3": rag_v3_agent,  # NOVO
}
```

---

## 🗑️ Arquivos e Diretórios Removidos/Deprecados

### Duplicações na Raiz (a remover)

| Caminho | Ação | Motivo | Substituído por |
|---------|------|--------|-----------------|
| `rag_v1/` | ❌ REMOVER | Duplicado | `src/amldo/rag/v1/` |
| `rag_v2/` | ❌ REMOVER | Duplicado | `src/amldo/rag/v2/` |
| `LicitAI/backend/agents/` | ❌ REMOVER | Duplicado | `src/amldo/agents/` |

**Ação:**
```bash
# Mover para backup
mkdir -p backup/deprecated_2025-11-15
mv rag_v1 backup/deprecated_2025-11-15/
mv rag_v2 backup/deprecated_2025-11-15/
mv LicitAI/backend backup/deprecated_2025-11-15/
```

### AMLDO_W (a deprecar)

| Caminho | Ação | Motivo | Migrado para |
|---------|------|--------|--------------|
| `AMLDO_W/AMLDO/` | ⚠️ DEPRECAR | Migrado completamente | `src/amldo/` |
| `AMLDO_W/AMLDO/rag_v3_sim/` | ✅ Migrado | - | `src/amldo/rag/v3/` |
| `AMLDO_W/AMLDO/webapp/` | ✅ Migrado | - | `src/amldo/interfaces/api/` |
| `AMLDO_W/AMLDO/rag_v1/` | ❌ Não migrar | Duplicado de v0.2.0 | `src/amldo/rag/v1/` |
| `AMLDO_W/AMLDO/rag_v2/` | ❌ Não migrar | Duplicado de v0.2.0 | `src/amldo/rag/v2/` |
| `AMLDO_W/AMLDO/*.ipynb` | ⚠️ Manter como referência | Notebooks experimentais | - |

**Ação Recomendada:**
```bash
# Opção 1: Renomear para indicar deprecated
mv AMLDO_W AMLDO_W_DEPRECATED_2025-11-15

# Criar README de aviso
cat > AMLDO_W_DEPRECATED_2025-11-15/README.md << 'EOF'
# ⚠️ DEPRECATED

Esta pasta foi **deprecada** em 2025-11-15.

## Migração Realizada

- `rag_v3_sim/` → `src/amldo/rag/v3/`
- `webapp/` → `src/amldo/interfaces/api/`

## Notebooks

Os notebooks `.ipynb` foram mantidos como referência em `notebooks/experimentos/`.

## Status

**NÃO USAR** este código. Use `src/amldo/` ao invés.

Para referência histórica apenas.
EOF

# Opção 2: Mover para backup (após 2 meses)
# mv AMLDO_W backup/AMLDO_W_original_2025-11-15
```

### Notebooks do AMLDO_W

| Arquivo | Ação | Destino |
|---------|------|---------|
| `AMLDO_W/AMLDO/get_v1_data.ipynb` | ⚠️ Copiar para referência | `notebooks/experimentos/amldo_w_get_v1_data.ipynb` |
| `AMLDO_W/AMLDO/get_vectorial_bank_v1.ipynb` | ⚠️ Copiar para referência | `notebooks/experimentos/amldo_w_vectorial_bank.ipynb` |
| `AMLDO_W/AMLDO/order_rag_study.ipynb` | ⚠️ Copiar para referência | `notebooks/experimentos/amldo_w_rag_study.ipynb` |

---

## 🔄 Mudanças de Comportamento

### RAG v2 (sem mudanças de código, mas importante documentar)

| Aspecto | v0.2.0 | v0.3.0 |
|---------|--------|--------|
| Search Type | `settings.search_type` (MMR por padrão) | ✅ Mantém mesmo comportamento |
| Filtragem | Filtra `artigo_0.txt` | ✅ Mantém |
| Pós-processamento | Hierárquico (XML) | ✅ Mantém |

**Sem breaking changes!**

### RAG v3 (novo)

| Aspecto | Valor Padrão | Configurável via |
|---------|--------------|------------------|
| Search Type | `similarity` | `settings.rag_v3_search_type` |
| K (documentos) | `12` | `settings.rag_v3_k` |
| Filtragem | Filtra `artigo_0.txt` | Código |
| Pós-processamento | Hierárquico (XML) | Código |

**Diferença chave vs v2:** Usa `similarity` ao invés de `mmr` por padrão.

### API Endpoints (novo)

#### POST /api/ask

**Request:**
```json
{
  "question": "string (obrigatório)",
  "rag_version": "v1 | v2 | v3 (opcional, default: v2)"
}
```

**Response:**
```json
{
  "answer": "string",
  "rag_version": "string",
  "question": "string"
}
```

**Status Codes:**
- `200`: Sucesso
- `400`: Pergunta vazia ou versão RAG inválida
- `500`: Erro interno (LLM, FAISS, etc)

#### POST /api/upload

**Request:** `multipart/form-data` com campo `files` (lista de PDFs)

**Response:**
```json
{
  "saved": ["arquivo1.pdf", "arquivo2.pdf"],
  "failed": [{"file": "arquivo3.pdf", "error": "Tipo inválido"}]
}
```

#### POST /api/process

**Request:** (vazio)

**Response:**
```json
{
  "processed": 3,
  "total_chunks": 450,
  "files": [
    {"file": "lei.pdf", "chunks": 150},
    {"file": "decreto.pdf", "chunks": 200},
    {"file": "portaria.pdf", "chunks": 100}
  ]
}
```

**Status Codes:**
- `200`: Sucesso
- `404`: Nenhum PDF encontrado
- `500`: Erro ao processar

#### GET /api/metrics/stats

**Response:**
```json
{
  "rag_stats": [
    {"version": "v1", "queries": 50, "avg_response_time_ms": 1200},
    {"version": "v2", "queries": 150, "avg_response_time_ms": 1500},
    {"version": "v3", "queries": 25, "avg_response_time_ms": 1100}
  ],
  "total_files_processed": 12,
  "total_chunks_indexed": 5430
}
```

#### GET /api/metrics/processing-history

**Query Params:** `limit` (int, default: 100)

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "timestamp": "2025-11-15T10:30:00",
      "files_processed": 3,
      "total_chunks": 450,
      "duration_seconds": 45.5
    },
    ...
  ]
}
```

### Métricas

#### Sistema Antigo (AMLDO_W)

- ✅ Formato: JSON (`data/metrics/embedding_history.json`)
- ⚠️ Limitações:
  - Sem queries de busca eficientes
  - Crescimento ilimitado de arquivo
  - Sem índices
  - Sem agregações

#### Sistema Novo (v0.3.0)

- ✅ Formato: SQLite (`data/metrics/metrics.db`)
- ✅ Vantagens:
  - Queries SQL rápidas
  - Índices automáticos
  - Agregações (COUNT, AVG, SUM)
  - Limitação de tamanho (VACUUM)
  - Backup fácil

**Migration Path:**
```python
# Script de migração (se necessário)
import json
import sqlite3
from pathlib import Path

def migrate_json_to_sqlite():
    old_json = Path("data/metrics/embedding_history.json")
    if not old_json.exists():
        return

    with open(old_json) as f:
        data = json.load(f)

    conn = sqlite3.connect("data/metrics/metrics.db")
    cursor = conn.cursor()

    for entry in data:
        cursor.execute(
            "INSERT INTO processing_history (timestamp, files_processed, total_chunks) VALUES (?, ?, ?)",
            (entry["ts"], 0, entry["chunks"])  # Assumindo estrutura
        )

    conn.commit()
    conn.close()

    # Backup do JSON original
    old_json.rename("data/metrics/embedding_history.json.bak")
```

---

## 📊 Estatísticas de Mudanças

### Linhas de Código

| Módulo | Linhas Adicionadas | Linhas Removidas | Linhas Modificadas | Total |
|--------|-------------------|------------------|-------------------|-------|
| `src/amldo/rag/v3/` | ~200 | 0 | 0 | +200 |
| `src/amldo/interfaces/api/` | ~800 | 0 | 0 | +800 |
| `src/amldo/utils/metrics.py` | ~150 | 0 | 0 | +150 |
| `src/amldo/core/config.py` | ~30 | 0 | ~5 | +35 |
| `tests/` | ~400 | 0 | 0 | +400 |
| `docs/` | ~2500 | 0 | ~100 | +2600 |
| **TOTAL** | **~4080** | **0** | **~105** | **+4185** |

### Arquivos

| Tipo | Novos | Modificados | Removidos | Total Mudanças |
|------|-------|-------------|-----------|----------------|
| Python (`.py`) | 15 | 5 | 0 | 20 |
| Markdown (`.md`) | 4 | 2 | 0 | 6 |
| HTML | 3 | 0 | 0 | 3 |
| TOML | 0 | 1 | 0 | 1 |
| TXT (requirements) | 1 | 0 | 0 | 1 |
| **TOTAL** | **23** | **8** | **0** | **31** |

### Diretórios

| Tipo | Novos | Removidos | Deprecados |
|------|-------|-----------|------------|
| Código-fonte | 6 | 3 | 1 (AMLDO_W) |
| Testes | 0 | 0 | 0 |
| Docs | 0 | 0 | 0 |
| Data | 1 (metrics) | 0 | 0 |
| **TOTAL** | **7** | **3** | **1** |

---

## 🔗 Dependências

### Novas Dependências (requirements/api.txt)

| Biblioteca | Versão | Propósito |
|-----------|--------|-----------|
| `fastapi` | `>=0.110.0` | Framework web API REST |
| `uvicorn[standard]` | `>=0.27.0` | ASGI server para FastAPI |
| `python-multipart` | `>=0.0.9` | Upload de arquivos multipart/form-data |
| `jinja2` | `>=3.1.0` | Templates HTML |

### Dependências Existentes (sem mudanças)

Todas as dependências de `requirements/base.txt` mantidas sem alterações:
- `langchain==1.0.2`
- `sentence-transformers==5.1.2`
- `faiss-cpu==1.12.0`
- `pandas==2.3.2`
- etc.

### Dependências de Desenvolvimento (sem mudanças)

`requirements/dev.txt` mantido sem alterações.

---

## 🧪 Testes

### Cobertura de Testes (meta)

| Módulo | Cobertura Antes | Cobertura Meta | Status |
|--------|-----------------|----------------|--------|
| `src/amldo/rag/v1/` | 85% | 85% | ✅ Manter |
| `src/amldo/rag/v2/` | 80% | 80% | ✅ Manter |
| `src/amldo/rag/v3/` | 0% (novo) | >80% | 🔄 A implementar |
| `src/amldo/interfaces/api/` | 0% (novo) | >85% | 🔄 A implementar |
| `src/amldo/utils/metrics.py` | 0% (novo) | >90% | 🔄 A implementar |
| **Projeto Geral** | **75%** | **>80%** | 🎯 Meta |

### Novos Testes

| Arquivo de Teste | Testes (#) | Linhas (~) |
|------------------|------------|-----------|
| `test_rag_v3.py` | 8 | 120 |
| `test_api_endpoints.py` | 12 | 180 |
| `test_metrics.py` | 6 | 80 |
| `test_api_integration.py` | 4 | 100 |
| **TOTAL** | **30** | **480** |

---

## 📅 Timeline de Implementação

### Semana 1 (2025-11-16 a 2025-11-22)

**Fase 2: RAG v3**
- [ ] Dia 1-2: Migrar código RAG v3
- [ ] Dia 3: Atualizar config e testes
- [ ] Dia 4: Integração ADK
- [ ] Dia 5: Validação e ajustes

### Semana 2 (2025-11-23 a 2025-11-29)

**Fase 3: FastAPI**
- [ ] Dia 1-2: Estrutura base API
- [ ] Dia 3: Routers e models
- [ ] Dia 4: Templates e estáticos
- [ ] Dia 5: Testes endpoints

### Semana 3 (2025-11-30 a 2025-12-06)

**Fases 4-7: Métricas, Testes, Docs, Limpeza**
- [ ] Dia 1: Sistema de métricas
- [ ] Dia 2-3: Testes completos
- [ ] Dia 4: Documentação
- [ ] Dia 5: Limpeza e revisão final

---

## ✅ Critérios de Aceitação

### Funcionalidade

- [ ] RAG v1 funciona sem regressões
- [ ] RAG v2 funciona sem regressões
- [ ] RAG v3 retorna respostas válidas
- [ ] API `/api/ask` funciona para v1, v2, v3
- [ ] Upload de PDFs via API funciona
- [ ] Processamento de PDFs via API funciona
- [ ] Métricas são registradas corretamente
- [ ] ADK reconhece `rag_v3`
- [ ] Streamlit continua funcionando
- [ ] Templates HTML renderizam corretamente

### Performance

- [ ] RAG v3 responde em <3s (95th percentile)
- [ ] API responde em <2s para consultas RAG
- [ ] Upload não trava para arquivos <10MB
- [ ] Processamento de 1 PDF (<100 páginas) em <1min

### Testes

- [ ] Cobertura >80% para novos módulos
- [ ] Todos testes passando
- [ ] Testes de integração passando
- [ ] Nenhum teste flaky

### Documentação

- [ ] README atualizado
- [ ] CLAUDE.md atualizado
- [ ] API documentada (OpenAPI/Swagger)
- [ ] Guia de migração completo
- [ ] Inventário de mudanças completo

### Qualidade de Código

- [ ] Black formatação OK
- [ ] Ruff linting OK
- [ ] Mypy type checking OK
- [ ] Pre-commit hooks passando
- [ ] Sem duplicações de código
- [ ] Sem code smells críticos

---

## 🔍 Validação de Migração

### Checklist de Validação

#### RAG v3
```bash
# 1. Importação
python -c "from amldo.rag.v3.tools import consultar_base_rag; print('✅ Import OK')"

# 2. Configuração
python -c "from amldo.core.config import settings; print(f'✅ RAG v3 enabled: {settings.rag_v3_enabled}')"

# 3. Consulta teste
python -c "from amldo.rag.v3.tools import consultar_base_rag; r = consultar_base_rag('Teste'); print(f'✅ Consulta OK: {len(r)} chars')"

# 4. ADK
adk web
# Verificar se 'rag_v3' aparece na lista de agentes
```

#### API FastAPI
```bash
# 1. Iniciar servidor
amldo-api &
API_PID=$!

# 2. Testar root
curl -s http://localhost:8000/ | grep -q "<title>" && echo "✅ Root OK"

# 3. Testar /api/ask
curl -s -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Teste","rag_version":"v2"}' \
  | jq -e '.answer' > /dev/null && echo "✅ /api/ask OK"

# 4. Testar métricas
curl -s http://localhost:8000/api/metrics/stats \
  | jq -e '.total_chunks_indexed' > /dev/null && echo "✅ Métricas OK"

# 5. Parar servidor
kill $API_PID
```

#### Métricas
```bash
# 1. Verificar banco SQLite
python -c "
import sqlite3
conn = sqlite3.connect('data/metrics/metrics.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
tables = [r[0] for r in cursor.fetchall()]
assert 'processing_history' in tables
assert 'query_history' in tables
print('✅ SQLite OK')
"

# 2. Inserir métrica teste
python -c "
from amldo.utils.metrics import track_query_metrics
track_query_metrics('v2', 'Teste validação', 1500.0)
print('✅ Track OK')
"

# 3. Ler métricas
python -c "
from amldo.utils.metrics import get_metrics_manager
stats = get_metrics_manager().get_stats()
print(f'✅ Stats OK: {stats}')
"
```

---

## 📞 Contato e Suporte

**Equipe AMLDO**
- Repositório: https://github.com/Penhall/AMLDO
- Issues: https://github.com/Penhall/AMLDO/issues

**Revisões:**
- Semanal durante migração
- Final antes do release v0.3.0

---

**Status:** 🔄 Em Progresso
**Última Atualização:** 2025-11-15
**Próxima Revisão:** 2025-11-22
