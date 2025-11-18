# Scripts de Execução AMLDO

Scripts para executar as diferentes interfaces do sistema AMLDO.

## 🚀 Scripts Disponíveis

### 1. `run_api.sh` - FastAPI REST API
Execute a API REST completa com documentação Swagger.

```bash
./scripts/run_api.sh
```

**Porta:** 8000
**Acessos:**
- Interface Web: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health

**Endpoints principais:**
- `POST /api/ask` - Consultas RAG (v1, v2, v3)
- `POST /api/upload` - Upload de PDFs
- `POST /api/process` - Processar documentos
- `GET /api/metrics/stats` - Estatísticas do sistema

---

### 2. `run_streamlit.sh` - Streamlit Web App
Execute a interface web interativa com Streamlit.

```bash
./scripts/run_streamlit.sh
```

**Porta:** 8501
**Acesso:** http://localhost:8501

**Páginas:**
- **Home** - Visão geral do sistema
- **Pipeline** - Processamento de documentos (upload → estrutura → índice)
- **RAG Query** - Consultas à base de conhecimento

---

### 3. `run_adk.sh` - Google ADK Interface
Execute a interface conversacional com agentes RAG.

```bash
./scripts/run_adk.sh
```

**Porta:** 8080
**Acesso:** http://localhost:8080

**Agentes disponíveis:**
- `rag_v1` - RAG básico (MMR search)
- `rag_v2` - RAG avançado (contexto hierárquico + MMR) ⭐ Recomendado
- `rag_v3` - RAG experimental (similarity search)

---

### 4. `run_all.sh` - Todas as Aplicações
Execute todas as aplicações simultaneamente.

```bash
./scripts/run_all.sh
```

**Portas:**
- FastAPI: 8000
- Streamlit: 8501
- Google ADK: 8080

**Logs:** Os logs são salvos em `logs/`:
- `logs/api.log` - FastAPI
- `logs/streamlit.log` - Streamlit
- `logs/adk.log` - Google ADK

**Para parar:** Pressione `Ctrl+C` (encerra todas as aplicações)

---

## 📋 Pré-requisitos

Antes de executar qualquer script, certifique-se de que:

1. **Virtual environment está criado e ativado:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Dependências estão instaladas:**
   ```bash
   # Todas as dependências (recomendado)
   pip install -e ".[adk,streamlit,dev]"

   # Ou específicas
   pip install -e .              # Base
   pip install -e ".[adk]"       # + Google ADK
   pip install -e ".[streamlit]" # + Streamlit
   ```

3. **Arquivo `.env` está configurado:**
   ```bash
   cp .env.example .env
   # Edite .env e adicione GOOGLE_API_KEY
   ```

4. **Vector store existe:**
   ```bash
   # Verificar se existe
   ls data/vector_db/v1_faiss_vector_db/

   # Se não existir, processar documentos primeiro
   # (use Streamlit Pipeline ou notebooks)
   ```

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Você pode configurar portas e hosts via variáveis de ambiente:

```bash
# FastAPI
export API_HOST=0.0.0.0
export API_PORT=8080
./scripts/run_api.sh

# Streamlit
export STREAMLIT_PORT=8502
./scripts/run_streamlit.sh
```

### Permissões (Linux/Mac)

Os scripts já foram tornados executáveis. Se necessário:

```bash
chmod +x scripts/*.sh
```

### Windows (WSL)

Os scripts funcionam no WSL (Windows Subsystem for Linux). Para executar no Windows nativo, use:

```bash
bash scripts/run_api.sh
```

Ou crie arquivos `.bat` equivalentes.

---

## 📚 Documentação Adicional

- **Setup Rápido:** `.instructions/SETUP_VENV_RAPIDO.md`
- **Setup Windows:** `.instructions/SETUP_WINDOWS_RAPIDO.md`
- **Troubleshooting:** `.instructions/TROUBLESHOOTING_WINDOWS.md`
- **Guia de WebApps:** `.instructions/WEBAPPS_GUIDE.md`
- **Quick Start:** `.instructions/QUICK_START_SCRIPTS.md`
- **Documentação Técnica:** `docs/`
- **Guia de Desenvolvimento:** `CLAUDE.md`

---

## 🐛 Problemas Comuns

### Erro: "Virtual environment não encontrado"
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -e ".[adk,streamlit,dev]"
```

### Erro: "Pacote 'amldo' não instalado"
```bash
source venv/bin/activate
pip install -e .
```

### Erro: "GOOGLE_API_KEY não configurado"
```bash
cp .env.example .env
# Edite .env e adicione sua chave do Google
```

### Erro: "FAISS deserialization error"
Certifique-se de que o vector store foi criado corretamente. Se necessário, reprocesse os documentos usando o Streamlit Pipeline ou os notebooks.

### Porta já em uso
```bash
# Verificar processos usando a porta
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Matar processo
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

---

## 📞 Suporte

Para mais informações:
- Documentação: `docs/`
- Issues: GitHub Issues
- Guia do Desenvolvedor: `CLAUDE.md`
