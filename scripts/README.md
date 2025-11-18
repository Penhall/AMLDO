# Scripts de Execução AMLDO

Script multiplataforma em Python para executar as aplicações do AMLDO com menu interativo.

## 🚀 Uso Rápido

### Menu Interativo (Recomendado)

```bash
python scripts/run.py
```

Você verá um menu com as opções:
```
1 - FastAPI REST API (porta 8000)
2 - Streamlit Web App (porta 8501)
3 - Google ADK Interface (porta 8080)
4 - Todas as aplicações (8000, 8501, 8080)
0 - Sair
```

### Execução Direta (sem menu)

```bash
# FastAPI REST API
python scripts/run.py --api

# Streamlit Web App
python scripts/run.py --streamlit

# Google ADK Interface
python scripts/run.py --adk

# Todas as aplicações
python scripts/run.py --all
```

### Aliases curtos

```bash
python scripts/run.py -a   # FastAPI
python scripts/run.py -s   # Streamlit
python scripts/run.py -k   # Google ADK
python scripts/run.py -A   # Todas
```

---

## 📋 Aplicações Disponíveis

### 1. FastAPI REST API (porta 8000)

API REST completa com documentação Swagger.

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

### 2. Streamlit Web App (porta 8501)

Interface web interativa com Streamlit.

**Acesso:** http://localhost:8501

**Páginas:**
- **Home** - Visão geral do sistema
- **Pipeline** - Processamento de documentos (upload → estrutura → índice)
- **RAG Query** - Consultas à base de conhecimento

---

### 3. Google ADK Interface (porta 8080)

Interface conversacional com agentes RAG.

**Acesso:** http://localhost:8080

**Agentes disponíveis:**
- `rag_v1` - RAG básico (MMR search)
- `rag_v2` - RAG avançado (contexto hierárquico + MMR) ⭐ Recomendado
- `rag_v3` - RAG experimental (similarity search)

---

### 4. Todas as Aplicações

Execute todas simultaneamente em portas diferentes.

**Portas:**
- FastAPI: 8000
- Streamlit: 8501
- Google ADK: 8080

**Logs:** Salvos em `logs/`:
- `logs/api.log` - FastAPI
- `logs/streamlit.log` - Streamlit
- `logs/adk.log` - Google ADK

**Para parar:** Pressione `Ctrl+C`

---

## 🔧 Pré-requisitos

O script verifica automaticamente os seguintes pré-requisitos:

### 1. Python 3.11+

```bash
python --version
# Deve ser 3.11 ou superior
```

### 2. Pacote AMLDO Instalado

```bash
# Se ainda não instalou
pip install -e .

# Com extras (adk, streamlit)
pip install -e ".[adk,streamlit]"
```

### 3. Arquivo .env Configurado

```bash
# Criar .env
cp .env.example .env

# Editar e adicionar GOOGLE_API_KEY
# GOOGLE_API_KEY=sua_chave_aqui
```

---

## 💻 Compatibilidade

✅ **Windows** (PowerShell, CMD, Git Bash)
✅ **Linux** (Ubuntu, Debian, Fedora, etc.)
✅ **macOS**
✅ **WSL** (Windows Subsystem for Linux)

O script:
- Usa Python puro (sem dependências shell)
- Detecta automaticamente o sistema operacional
- Funciona em qualquer terminal que tenha Python

---

## 🎨 Recursos

### ✅ Verificação de Pré-requisitos

O script verifica automaticamente:
- Se está no diretório correto
- Se o pacote `amldo` está instalado
- Se o arquivo `.env` existe

### ✅ Cores e Formatação

- Output colorido (funciona em todos os sistemas)
- Banner visual
- Mensagens claras e informativas

### ✅ Gerenciamento de Processos

- Inicia aplicações em background (modo `--all`)
- Cleanup automático ao pressionar Ctrl+C
- Logs separados para cada aplicação
- Detecção de falhas em processos

### ✅ Multiplataforma

- Sem dependências de shell (bash, sh, etc.)
- Funciona igualmente em Windows, Linux e Mac
- Trata diferenças de sistema operacional automaticamente

---

## 🐛 Troubleshooting

### ❌ Erro: Keras 3 incompatível com Transformers

**Erro completo:**
```
ValueError: Your currently installed version of Keras is Keras 3, but this is not yet supported in Transformers.
Please install the backwards-compatible tf-keras package with `pip install tf-keras`.
```

**Solução (30 segundos):**
```bash
pip install tf-keras
```

**Verificar:**
```bash
python -c "import tf_keras; print('✅ OK!')"
python scripts/run.py --api
```

📖 **Mais detalhes:** [.instructions/FIX_LANGCHAIN_HUGGINGFACE.md](../.instructions/FIX_LANGCHAIN_HUGGINGFACE.md)

---

### Erro: "Execute este script do diretório raiz do projeto"

**Solução:**
```bash
cd /caminho/para/AMLDO
python scripts/run.py
```

### Erro: "Pacote 'amldo' não instalado"

**Solução:**
```bash
pip install -e .
# ou com extras
pip install -e ".[adk,streamlit]"
```

### Erro: "Comando 'adk' não encontrado"

**Solução:**
```bash
pip install -e ".[adk]"
```

### Aviso: "Arquivo .env não encontrado"

**Solução:**
```bash
cp .env.example .env
# Edite .env e adicione GOOGLE_API_KEY
```

### Porta já em uso

**Verificar processos:**
```bash
# Linux/Mac
lsof -i :8000
lsof -i :8501
lsof -i :8080

# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :8501
netstat -ano | findstr :8080
```

**Matar processo:**
```bash
# Linux/Mac
kill -9 <PID>

# Windows (PowerShell como Admin)
taskkill /PID <PID> /F
```

### Aplicação não inicia

**Ver logs:**
```bash
# Se usou --all
cat logs/api.log
cat logs/streamlit.log
cat logs/adk.log

# Windows
type logs\api.log
type logs\streamlit.log
type logs\adk.log
```

---

## 📚 Documentação Adicional

- **Setup Rápido:** `../.instructions/README.md`
- **Troubleshooting:** `../.instructions/TROUBLESHOOTING_WINDOWS.md`
- **Guia Técnico:** `../CLAUDE.md`
- **Documentação Completa:** `../docs/`

---

## 💡 Exemplos de Uso

### Desenvolvimento

```bash
# Testar FastAPI durante desenvolvimento
python scripts/run.py --api
```

### Demonstração

```bash
# Mostrar todas as interfaces
python scripts/run.py --all
```

### Produção (Docker recomendado)

Para produção, use Docker Compose:
```bash
docker-compose up -d
```

---

## 🔗 Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `run.py` | **Script principal** - Menu interativo para todas as aplicações |
| `run_tests.sh` | Executa suite de testes (pytest) |

---

## ✨ Vantagens do Script Python

1. **Multiplataforma** - Funciona em qualquer OS com Python
2. **Sem dependências** - Não precisa de bash/sh/PowerShell
3. **Menu interativo** - Fácil de usar
4. **Verificações automáticas** - Valida pré-requisitos
5. **Gerenciamento robusto** - Cleanup correto de processos
6. **Logs organizados** - Um arquivo por aplicação
7. **Cores em todos OS** - Output bonito em Windows, Linux e Mac

---

## 📞 Suporte

- **Documentação:** `../docs/`
- **Issues:** GitHub Issues
- **Guias:** `../.instructions/`
