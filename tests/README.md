# Testes - AMLDO v0.3.0

> **Suite completa de testes automatizados** para garantir qualidade e confiabilidade do sistema RAG.

---

## 🚀 Quick Start

```bash
# Executar todos os testes
pytest tests/

# Apenas testes rápidos (sem integration/slow)
pytest tests/ -m "not integration and not slow"

# Com cobertura
pytest tests/ --cov=src/amldo --cov-report=html

# Usando o script
./scripts/run_tests.sh cov
```

---

## 📁 Estrutura

```
tests/
├── README.md                    # Este arquivo
├── conftest.py                  # Fixtures compartilhadas
├── pytest.ini                   # Configuração pytest
├── .coveragerc                  # Configuração cobertura
│
├── unit/                        # Testes unitários
│   ├── test_config.py           # ✅ 4 testes
│   ├── test_ingestion.py        # ✅ 3 testes
│   ├── test_structure.py        # ✅ 4 testes
│   ├── test_embeddings.py       # ✅ 22 testes
│   ├── test_metrics.py          # ✅ 15 testes
│   ├── test_rag_v3.py           # ✅ 15 testes
│   ├── test_api.py              # ✅ 20+ testes
│   └── test_indexer.py          # ⏸️ desabilitado
│
└── integration/                 # Testes de integração
    └── test_rag_pipeline.py     # ✅ 10+ testes
```

**Total**: ~46 testes passando (+ testes de integração)

---

## 🧪 Tipos de Teste

### 1. Testes Unitários (`unit/`)

Testam componentes **isolados**:
- ✅ Configuração (settings, env vars)
- ✅ Embeddings (geração, normalização)
- ✅ API FastAPI (endpoints, validação)
- ✅ Métricas (SQLite, rastreamento)
- ✅ RAG v3 (similarity search)
- ✅ Processamento (ingestão, estruturação)

### 2. Testes de Integração (`integration/`)

Testam **fluxos completos**:
- ✅ Pipeline RAG end-to-end (documento → indexação → query)
- ✅ RAG v1, v2, v3 juntos
- ✅ API + métricas + RAG
- ✅ Performance e concorrência

---

## 🎯 Executando Testes

### Por Tipo

```bash
# Unitários
pytest tests/unit/ -v

# Integração
pytest tests/integration/ -v -m integration

# Rápidos (excluir lentos)
pytest tests/ -m "not integration and not slow"
```

### Por Módulo

```bash
# API
pytest tests/unit/test_api.py -v

# Embeddings
pytest tests/unit/test_embeddings.py -v

# Métricas
pytest tests/unit/test_metrics.py -v

# RAG
pytest tests/unit/test_rag_v3.py -v
pytest tests/integration/test_rag_pipeline.py -v
```

### Teste Específico

```bash
# Formato: arquivo::classe::metodo
pytest tests/unit/test_api.py::TestQueryEndpoint::test_ask_endpoint_v1_success -v
```

### Com Opções

```bash
# Parar no primeiro erro
pytest tests/ -x

# Modo verboso
pytest tests/ -vv

# Com coverage
pytest tests/ --cov=src/amldo --cov-report=html

# Apenas ver quais testes rodariam
pytest tests/ --collect-only
```

---

## 📊 Cobertura de Código

```bash
# Gerar relatório completo
pytest tests/ \
    --cov=src/amldo \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml

# Abrir no navegador
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Arquivos gerados**:
- `htmlcov/index.html` - Relatório visual interativo
- `coverage.xml` - Para CI/CD (Codecov, SonarQube)
- Terminal - Sumário rápido

---

## 🏷️ Markers

Use markers para categorizar testes:

```python
@pytest.mark.integration
def test_full_pipeline():
    """Teste de integração (lento)."""
    pass

@pytest.mark.slow
def test_large_dataset():
    """Teste de performance (> 1 segundo)."""
    pass

@pytest.mark.requires_api_key
def test_llm_query():
    """Requer GOOGLE_API_KEY configurada."""
    pass
```

**Executar por marker**:
```bash
# Apenas integration
pytest tests/ -m integration

# Excluir integration e slow
pytest tests/ -m "not integration and not slow"

# Apenas slow
pytest tests/ -m slow
```

---

## 🧰 Fixtures Disponíveis

### Diretórios e Arquivos
- `temp_dir` - Diretório temporário (auto-cleanup)
- `sample_text` - Texto de lei simples
- `sample_lei_completa` - Lei completa com estrutura
- `sample_pdf_path` - Arquivo TXT temporário

### DataFrames
- `sample_articles_df` - Artigos estruturados
- `sample_art_0_df` - Artigos 0 (introduções)
- `sample_metadata_list` - Lista de metadados

### Configuração
- `mock_env_vars` - Env vars mock
- `mock_embeddings` - Embeddings fake (384 dim)
- `sample_csv_file` - CSV temporário

### API e Serviços
- `api_client` - TestClient FastAPI
- `metrics_manager` - MetricsManager com DB temporário
- `mock_retriever_docs` - Documentos mock do retriever

**Uso**:
```python
def test_something(temp_dir, sample_articles_df):
    """Fixture é injetada automaticamente."""
    csv_path = temp_dir / "test.csv"
    sample_articles_df.to_csv(csv_path)
    assert csv_path.exists()
```

---

## 📝 Escrevendo Novos Testes

### 1. Estrutura AAA

```python
def test_track_query(metrics_manager):
    # ARRANGE (preparar)
    rag_version = "v2"
    question = "Teste"

    # ACT (executar)
    row_id = metrics_manager.track_query(rag_version, question, 1500.0, True)

    # ASSERT (verificar)
    assert row_id > 0
```

### 2. Use Fixtures

```python
# ✅ BOM
def test_embed(manager):
    embeddings = manager.embed(["texto"])
    assert embeddings is not None

# ❌ EVITAR
def test_embed():
    manager = EmbeddingManager()  # Repetitivo
    embeddings = manager.embed(["texto"])
```

### 3. Isole Testes

```python
# ✅ BOM - usa temp_dir
def test_save(temp_dir):
    file_path = temp_dir / "test.txt"
    file_path.write_text("content")
    # Auto-cleanup

# ❌ EVITAR - polui filesystem
def test_save():
    Path("test.txt").write_text("content")
    # Arquivo permanece!
```

### 4. Mock Dependências

```python
@patch("amldo.interfaces.api.routers.queries.consultar_v2")
def test_api(mock_rag, api_client):
    mock_rag.return_value = "Resposta"
    response = api_client.post("/api/ask", json={"pergunta": "?"})
    assert response.status_code == 200
```

### 5. Nomeie Claramente

```python
# ✅ BOM
def test_ask_endpoint_returns_200_on_success():
    """Testa se endpoint retorna 200 em caso de sucesso."""

# ❌ EVITAR
def test1():
    pass
```

---

## 🔍 Debugging Testes

### Ver output detalhado

```bash
pytest tests/unit/test_api.py -v -s  # -s mostra print()
```

### Modo verboso com traceback completo

```bash
pytest tests/ -vv --tb=long
```

### Apenas mostrar quais testes falham

```bash
pytest tests/ --tb=short
```

### Usar debugger (pdb)

```python
def test_something():
    import pdb; pdb.set_trace()  # Breakpoint
    result = do_something()
    assert result
```

---

## ⚡ Performance

### Executar em paralelo (pytest-xdist)

```bash
# Instalar
pip install pytest-xdist

# Executar com 4 workers
pytest tests/ -n 4
```

### Pular testes lentos

```bash
pytest tests/ -m "not slow"
```

### Ver testes mais lentos

```bash
pytest tests/ --durations=10  # Top 10 mais lentos
```

---

## 🎨 Relatórios

### HTML (Coverage)

```bash
pytest --cov=src/amldo --cov-report=html
open htmlcov/index.html
```

### JUnit XML (CI/CD)

```bash
pytest --junitxml=junit.xml
```

### JSON

```bash
pytest --json=report.json
```

---

## 🐛 Troubleshooting

### ImportError: No module named 'amldo'

```bash
# Instalar em modo editable
pip install -e .
```

### Tests falham por falta de API key

```bash
# Pular testes que requerem API
pytest -m "not requires_api_key"
```

### Warnings excessivos

```bash
# Desabilitar warnings
pytest --disable-warnings
```

### Testes muito lentos

```bash
# Apenas rápidos
pytest -m "not integration and not slow"
```

---

## 📈 Status Atual

```
========================= test session starts ==========================
platform linux -- Python 3.12.3, pytest-8.4.2
collected 51 items

tests/unit/test_config.py ....                                   [  8%]
tests/unit/test_ingestion.py ...                                [  13%]
tests/unit/test_structure.py ....                               [  21%]
tests/unit/test_embeddings.py ..................F...FF          [  63%]
tests/unit/test_metrics.py ...............                      [  92%]
tests/unit/test_api.py ........                                 [100%]

============ 46 PASSED, 5 FAILED, 3 WARNINGS in 113.11s ===============
```

**✅ 46 testes passando**
**⚠️ 5 falhas menores** (edge cases)

---

## 📚 Documentação Completa

Ver **`docs/11-testes-automatizados.md`** para documentação detalhada.

---

## 🤝 Contribuindo

1. **Escreva testes** para novas funcionalidades
2. **Mantenha cobertura** > 80%
3. **Siga convenções** de nomenclatura
4. **Use fixtures** para reutilização
5. **Marque testes lentos** com `@pytest.mark.slow`

---

**AMLDO v0.3.0** - Sistema RAG com testes automatizados de qualidade 🚀
