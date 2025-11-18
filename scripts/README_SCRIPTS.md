# Scripts de Execução - AMLDO

> **3 scripts** para facilitar a execução de projetos Python

---

## 📜 Scripts Disponíveis

### 1. `run_amldo.sh` - Executar AMLDO (Projeto 1)

**Descrição**: Inicia o projeto AMLDO com a interface escolhida.

**Uso**:
```bash
# API FastAPI (padrão)
./scripts/run_amldo.sh api

# Streamlit
./scripts/run_amldo.sh streamlit

# Google ADK
./scripts/run_amldo.sh adk

# Todos via Docker Compose
./scripts/run_amldo.sh all
```

**Features**:
- ✅ Verifica configuração (`.env`, `GOOGLE_API_KEY`)
- ✅ Ativa virtual environment automaticamente
- ✅ Suporta 4 interfaces diferentes
- ✅ Docker Compose integrado
- ✅ Mensagens coloridas e informativas

**URLs**:
- API: http://localhost:8000
- Streamlit: http://localhost:8501
- ADK: http://localhost:8080

---

### 2. `run_projeto2.sh` - Executar Projeto 2

**Descrição**: Script **TEMPLATE** para executar outro projeto Python.

**⚠️ REQUER CONFIGURAÇÃO INICIAL**

**Como configurar**:

1. Abra o script:
   ```bash
   nano scripts/run_projeto2.sh
   ```

2. Edite a seção de configuração:
   ```bash
   # Exemplo para projeto MatchIt
   PROJECT_DIR="/mnt/d/PYTHON/MatchIt"
   PROJECT_NAME="MatchIt"
   RUN_COMMAND="streamlit run app.py"
   PORT="8501"
   NEEDS_ENV=true
   HAS_VENV=true
   ```

3. Salve e execute:
   ```bash
   ./scripts/run_projeto2.sh
   ```

**Exemplos de configuração**:

#### Exemplo 1: Streamlit App
```bash
PROJECT_DIR="/mnt/d/PYTHON/MatchIt"
PROJECT_NAME="MatchIt"
RUN_COMMAND="streamlit run app.py"
PORT="8501"
```

#### Exemplo 2: FastAPI
```bash
PROJECT_DIR="/mnt/d/PYTHON/MeuProjeto"
PROJECT_NAME="API do Projeto X"
RUN_COMMAND="uvicorn main:app --reload --port 5000"
PORT="5000"
```

#### Exemplo 3: Flask
```bash
PROJECT_DIR="/mnt/d/PYTHON/FlaskApp"
PROJECT_NAME="Flask App"
RUN_COMMAND="flask run --port 3000"
PORT="3000"
```

#### Exemplo 4: Docker Compose
```bash
PROJECT_DIR="/mnt/d/PYTHON/MeuProjeto"
PROJECT_NAME="Projeto Dockerizado"
RUN_COMMAND="docker-compose up -d"
PORT="8080"
```

---

### 3. `run_both.sh` - Executar Ambos Projetos Simultaneamente

**Descrição**: Inicia AMLDO E Projeto 2 **ao mesmo tempo** em processos separados.

**⚠️ REQUER CONFIGURAÇÃO DO PROJETO 2**

**Como configurar**:

1. **Primeiro**, configure o `run_projeto2.sh` (passo anterior)

2. **Depois**, edite `run_both.sh`:
   ```bash
   nano scripts/run_both.sh
   ```

3. Ajuste a configuração do Projeto 2:
   ```bash
   # Linha ~77
   PROJECT2_DIR="/mnt/d/PYTHON/MatchIt"  # Seu projeto
   PROJECT2_NAME="MatchIt"               # Nome
   PROJECT2_PORT="8501"                  # Porta
   PROJECT2_COMMAND="streamlit run app.py"  # Comando
   ```

4. Salve e execute:
   ```bash
   ./scripts/run_both.sh
   ```

**Uso**:
```bash
# Iniciar ambos
./scripts/run_both.sh

# Parar ambos
./scripts/run_both.sh stop
```

**Features**:
- ✅ Executa projetos em **paralelo** (background)
- ✅ Gerencia PIDs automaticamente
- ✅ Logs separados para cada projeto
- ✅ Comando único para parar tudo
- ✅ Suporta Docker Compose no AMLDO
- ✅ Configurável para qualquer projeto Python

**Logs**:
```bash
# Ver logs do AMLDO
tail -f /tmp/amldo_api.log

# Ver logs do Projeto 2
tail -f /tmp/projeto2.log
```

---

## 🚀 Quick Start

### Cenário 1: Apenas AMLDO

```bash
# API FastAPI
./scripts/run_amldo.sh api

# Ou Streamlit
./scripts/run_amldo.sh streamlit

# Ou tudo via Docker
./scripts/run_amldo.sh all
```

### Cenário 2: AMLDO + Outro Projeto

**1. Configure o Projeto 2**:
```bash
nano scripts/run_projeto2.sh
# Edite PROJECT_DIR, PROJECT_NAME, RUN_COMMAND, PORT
```

**2. Configure o script de ambos**:
```bash
nano scripts/run_both.sh
# Edite PROJECT2_* na seção de configuração
```

**3. Execute**:
```bash
./scripts/run_both.sh
```

**4. Parar**:
```bash
./scripts/run_both.sh stop
```

---

## 🎯 Casos de Uso

### Caso 1: AMLDO API + MatchIt Streamlit

**Projeto 2** (`run_projeto2.sh`):
```bash
PROJECT_DIR="/mnt/d/PYTHON/MatchIt"
PROJECT_NAME="MatchIt"
RUN_COMMAND="streamlit run app.py"
PORT="8501"
```

**Ambos** (`run_both.sh`):
```bash
PROJECT1_INTERFACE="api"  # AMLDO na porta 8000
PROJECT2_DIR="/mnt/d/PYTHON/MatchIt"
PROJECT2_COMMAND="streamlit run app.py"
PROJECT2_PORT="8501"
```

**Executar**:
```bash
./scripts/run_both.sh
```

**Resultado**:
- AMLDO API: http://localhost:8000
- MatchIt: http://localhost:8501

---

### Caso 2: Dois projetos FastAPI (portas diferentes)

**Projeto 2**:
```bash
PROJECT_DIR="/mnt/d/PYTHON/MeuAPI"
RUN_COMMAND="uvicorn main:app --reload --port 5000"
PORT="5000"
```

**Ambos**:
```bash
PROJECT1_INTERFACE="api"  # AMLDO porta 8000
PROJECT2_COMMAND="uvicorn main:app --reload --port 5000"
PROJECT2_PORT="5000"
```

**Resultado**:
- AMLDO: http://localhost:8000
- MeuAPI: http://localhost:5000

---

## 🔧 Customização Avançada

### Adicionar verificações pré-execução

Edite qualquer script e adicione antes de `eval "$RUN_COMMAND"`:

```bash
# Verificar se porta está livre
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}❌ Porta $PORT já está em uso${NC}"
    exit 1
fi

# Verificar dependências
if ! command -v streamlit &> /dev/null; then
    echo -e "${RED}❌ Streamlit não instalado${NC}"
    exit 1
fi

# Instalar requirements automaticamente
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
fi
```

### Mudar interface do AMLDO no `run_both.sh`

Linha ~64:
```bash
# Opções: api, streamlit, adk, all
PROJECT1_INTERFACE="streamlit"  # Mudar para Streamlit
```

### Adicionar mais projetos

Para executar 3+ projetos, edite `run_both.sh`:

```bash
# Após Projeto 2, adicione:

echo -e "${GREEN}🚀 Iniciando Projeto 3...${NC}"
cd "/mnt/d/PYTHON/Projeto3"
nohup python app3.py > /tmp/projeto3.log 2>&1 &
echo $! >> "$PID_FILE"
```

---

## 🐛 Troubleshooting

### Problema: "Permission denied"

**Solução**:
```bash
chmod +x scripts/run_amldo.sh
chmod +x scripts/run_projeto2.sh
chmod +x scripts/run_both.sh
```

### Problema: "Porta já em uso"

**Solução**:
```bash
# Ver o que está usando a porta
lsof -i :8000

# Matar processo
kill -9 PID

# Ou mudar porta no script
```

### Problema: "GOOGLE_API_KEY não configurada"

**Solução**:
```bash
cd /mnt/d/PYTHON/AMLDO
cp .env.example .env
nano .env  # Adicionar chave
```

### Problema: Scripts não param com `run_both.sh stop`

**Solução**:
```bash
# Matar manualmente
ps aux | grep python
kill -9 PID

# Limpar arquivo PID
rm -f /tmp/amldo_both_projects.pid

# Docker Compose
cd /mnt/d/PYTHON/AMLDO
docker-compose down
```

---

## 📝 Exemplos Práticos

### Exemplo 1: Desenvolvimento Full-Stack

```bash
# AMLDO (Backend API) + MatchIt (Frontend)
./scripts/run_both.sh

# Resultado:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:8501
```

### Exemplo 2: Testes Paralelos

```bash
# AMLDO produção (Docker) + AMLDO dev (Python)
# run_both.sh:
PROJECT1_INTERFACE="all"  # Docker na porta 8000
PROJECT2_DIR="/mnt/d/PYTHON/AMLDO"
PROJECT2_COMMAND="streamlit run src/amldo/interfaces/streamlit/app.py --server.port 8502"
PROJECT2_PORT="8502"
```

---

## ✨ Dicas

1. **Use Docker quando possível** para isolamento
2. **Separe logs** por projeto (`/tmp/projeto_X.log`)
3. **Configure portas diferentes** para cada serviço
4. **Teste individualmente** antes de rodar ambos
5. **Use `tmux` ou `screen`** para sessões persistentes

---

## 📚 Referências

- [AMLDO Documentation](../docs/)
- [Docker Compose](../docker-compose.yml)
- [Deploy Guide](../docs/12-ci-cd-deployment.md)

---

**Scripts criados para**: AMLDO v0.3.0
**Última atualização**: 2025-11-16
