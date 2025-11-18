# CI/CD e Deployment - AMLDO v0.3.0

> **Guia completo** de integração contínua, deployment e infraestrutura do AMLDO.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [CI/CD com GitHub Actions](#cicd-com-github-actions)
3. [Docker e Containerização](#docker-e-containerização)
4. [Ambientes (Dev, Staging, Prod)](#ambientes)
5. [Deploy Manual](#deploy-manual)
6. [Deploy Automatizado](#deploy-automatizado)
7. [Monitoramento](#monitoramento)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O AMLDO v0.3.0 possui **infraestrutura completa de CI/CD**:

- ✅ **GitHub Actions** - CI/CD automatizado
- ✅ **Docker** - Containerização multi-stage
- ✅ **Docker Compose** - Orquestração de serviços
- ✅ **Ambientes** - Dev, Staging, Production
- ✅ **Scripts** - Automação de deploy
- ✅ **Health Checks** - Monitoramento de saúde

### Arquitetura de Deploy

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Repository                       │
│  (Push / PR)                                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI                         │
│  ├─ Linting (Black, Ruff, MyPy)                            │
│  ├─ Unit Tests (Python 3.11, 3.12)                         │
│  ├─ Integration Tests                                       │
│  ├─ Coverage Report (Codecov)                              │
│  ├─ Security Scan (Safety, Bandit)                         │
│  └─ Build Check                                             │
└────────────────┬────────────────────────────────────────────┘
                 │ ✅ All checks passed
                 v
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CD                         │
│  ├─ Build Docker Image (ghcr.io)                           │
│  ├─ Deploy to Staging (auto em main)                       │
│  ├─ Deploy to Production (manual em tags)                  │
│  └─ Publish to PyPI (opcional)                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 v
┌──────────────┬──────────────┬─────────────┐
│   Staging    │  Production  │    PyPI     │
│  (Test env)  │  (Live env)  │  (Package)  │
└──────────────┴──────────────┴─────────────┘
```

---

## 🔄 CI/CD com GitHub Actions

### Workflows Disponíveis

| Workflow | Trigger | Descrição |
|----------|---------|-----------|
| **`ci.yml`** | Push/PR | Testes, linting, cobertura |
| **`cd.yml`** | Tags/Manual | Build, deploy, publicação |

### Workflow CI (`ci.yml`)

**Localização**: `.github/workflows/ci.yml`

**Jobs**:

1. **Lint** - Black, Ruff, MyPy
2. **Test-Unit** - Testes unitários (Python 3.11 e 3.12)
3. **Test-Integration** - Testes de integração (apenas main)
4. **Coverage** - Relatório de cobertura (Codecov)
5. **Build** - Verificação de build
6. **Security** - Scan de segurança (Safety, Bandit)
7. **Notify** - Notificação de resultados

**Exemplo de execução**:
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

**Status Badges**:
```markdown
![CI](https://github.com/SEU_USER/AMLDO/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/SEU_USER/AMLDO/branch/main/graph/badge.svg)
```

### Workflow CD (`cd.yml`)

**Localização**: `.github/workflows/cd.yml`

**Jobs**:

1. **Build-Docker** - Build e push de imagem Docker
2. **Deploy-Staging** - Deploy automático para staging (main)
3. **Deploy-Production** - Deploy manual para produção (tags)
4. **Publish-PyPI** - Publicação no PyPI (opcional)
5. **Update-Docs** - Atualização de documentação

**Exemplo de tag para produção**:
```bash
git tag -a v0.3.1 -m "Release v0.3.1"
git push origin v0.3.1  # Trigger deploy automático
```

### Secrets Necessários

Configure em **Settings → Secrets and variables → Actions**:

| Secret | Descrição | Obrigatório |
|--------|-----------|-------------|
| `GOOGLE_API_KEY` | API key do Gemini | ✅ Sim |
| `CODECOV_TOKEN` | Token do Codecov | ⚪ Opcional |
| `PYPI_TOKEN` | Token para publicar no PyPI | ⚪ Opcional |
| `GITHUB_TOKEN` | Auto-gerado pelo GitHub | ✅ Auto |

---

## 🐳 Docker e Containerização

### Dockerfile Multi-Stage

**Localização**: `Dockerfile`

**Estrutura**:
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
# Instala dependências

# Stage 2: Runtime
FROM python:3.11-slim
# Copia apenas o necessário
# Cria usuário não-root
# Define health check
```

**Vantagens**:
- ✅ Imagem final pequena (~500MB vs ~1.5GB)
- ✅ Segurança (usuário não-root)
- ✅ Health checks nativos
- ✅ Multi-arch (amd64, arm64)

### Build Local

```bash
# Build simples
docker build -t amldo:latest .

# Build com tag de versão
docker build -t amldo:0.3.0 -t amldo:latest .

# Build sem cache (força rebuild)
docker build --no-cache -t amldo:latest .

# Build multi-arch
docker buildx build --platform linux/amd64,linux/arm64 -t amldo:latest .
```

### Run Local

```bash
# Executar API
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -v $(pwd)/data:/data \
  amldo:latest

# Executar Streamlit
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_key \
  -v $(pwd)/data:/data \
  amldo:latest \
  streamlit run src/amldo/interfaces/streamlit/app.py --server.port=8501 --server.address=0.0.0.0

# Shell interativo
docker run -it --rm \
  -v $(pwd)/data:/data \
  amldo:latest \
  bash
```

### Docker Compose

**Localização**: `docker-compose.yml`

**Serviços**:
- `api` - FastAPI (porta 8000)
- `streamlit` - Interface web (porta 8501)
- `adk` - Google ADK agent (porta 8080)
- `nginx` - Reverse proxy (opcional, porta 80/443)

**Comandos**:

```bash
# Iniciar todos os serviços
docker-compose up -d

# Apenas API e Streamlit
docker-compose up -d api streamlit

# Com rebuild
docker-compose up -d --build

# Ver logs
docker-compose logs -f api

# Parar tudo
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Status dos serviços
docker-compose ps

# Shell em container rodando
docker-compose exec api bash
```

---

## 🌍 Ambientes

### 1. Development (Local)

**Configuração**: `.env`

```bash
# Copiar exemplo
cp .env.example .env

# Editar
nano .env  # Configure GOOGLE_API_KEY

# Executar
docker-compose up api streamlit

# Ou sem Docker
amldo-api
```

**URLs**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Streamlit: http://localhost:8501

**Características**:
- ✅ Debug habilitado
- ✅ Hot reload
- ✅ Logs verbosos (DEBUG)
- ✅ CORS permissivo

### 2. Staging (Homologação)

**Configuração**: `.env.staging`

```bash
# Copiar exemplo
cp .env.staging.example .env.staging

# Editar
nano .env.staging

# Deploy
./scripts/deploy.sh staging --build
```

**URLs**:
- API: https://staging.amldo.example.com
- Streamlit: https://staging.amldo.example.com:8501

**Características**:
- ⚪ Debug desabilitado
- ⚪ Logs INFO
- ⚪ CORS restrito
- ✅ Métricas habilitadas
- ✅ Testes de integração

### 3. Production (Produção)

**Configuração**: `.env.production`

```bash
# Copiar exemplo
cp .env.production.example .env.production

# Editar (use valores REAIS de produção!)
nano .env.production

# Deploy (requer confirmação)
./scripts/deploy.sh production --build --backup
```

**URLs**:
- API: https://amldo.example.com
- Docs: https://amldo.example.com/docs
- Streamlit: https://amldo.example.com/app

**Características**:
- 🔴 Debug DESABILITADO
- 🔴 Logs WARNING/ERROR apenas
- 🔴 CORS muito restrito
- ✅ HTTPS obrigatório
- ✅ Rate limiting
- ✅ Backup automático
- ✅ Health checks
- ✅ Monitoramento completo

### Comparação de Ambientes

| Feature | Dev | Staging | Production |
|---------|-----|---------|------------|
| **Debug** | ✅ ON | ❌ OFF | ❌ OFF |
| **Log Level** | DEBUG | INFO | WARNING |
| **CORS** | `*` | Específico | Muito restrito |
| **HTTPS** | ⚪ Opcional | ✅ Sim | ✅ Obrigatório |
| **Métricas** | ⚪ Opcional | ✅ Sim | ✅ Sim |
| **Backup** | ❌ Não | ⚪ Manual | ✅ Auto |
| **Health Check** | ⚪ Opcional | ✅ Sim | ✅ Sim |

---

## 🚀 Deploy Manual

### Opção 1: Script de Deploy Automatizado

```bash
# Development
./scripts/deploy.sh dev

# Staging (com rebuild)
./scripts/deploy.sh staging --build

# Production (com backup)
./scripts/deploy.sh production --build --backup
```

**Flags disponíveis**:
- `--build` - Força rebuild de imagens
- `--migrate` - Executa migrações de dados
- `--backup` - Cria backup antes do deploy

### Opção 2: Docker Compose Manual

```bash
# 1. Parar serviços atuais
docker-compose down

# 2. Pull de imagens (se usando registry)
docker-compose pull

# 3. Rebuild (se necessário)
docker-compose build --no-cache

# 4. Iniciar serviços
docker-compose up -d

# 5. Verificar health
curl http://localhost:8000/health

# 6. Ver logs
docker-compose logs -f api
```

### Opção 3: Kubernetes (Avançado)

```bash
# Criar namespace
kubectl create namespace amldo

# Apply manifests
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
kubectl apply -f k8s/ingress.yml

# Verificar status
kubectl get pods -n amldo
kubectl logs -f deployment/amldo-api -n amldo
```

---

## 🤖 Deploy Automatizado

### Via GitHub Actions (Recomendado)

**Staging** - Automático em push para `main`:
```bash
git checkout main
git pull
git merge develop
git push origin main  # → Trigger deploy staging
```

**Production** - Via tag:
```bash
# 1. Criar tag
git tag -a v0.3.1 -m "Release v0.3.1: Melhorias na API"

# 2. Push tag
git push origin v0.3.1  # → Trigger deploy production

# 3. Acompanhar no GitHub
# Actions → CD - Deployment
```

### Workflow de Release

```
develop → PR → main → Staging Deploy → Tag → Production Deploy
   ↓         ↓       ↓         ↓          ↓          ↓
 Feature   Review  Merge   Auto test   Manual   Live deploy
```

---

## 📊 Monitoramento

### Health Checks

**API Health Endpoint**:
```bash
curl http://localhost:8000/health

# Resposta esperada:
{
  "status": "healthy",
  "version": "0.3.0",
  "timestamp": "2025-11-16T20:00:00Z"
}
```

**Docker Health Check**:
```bash
docker ps  # Ver status HEALTH

# (healthy)   - OK
# (unhealthy) - Problema
# (starting)  - Inicializando
```

### Logs

```bash
# Docker Compose
docker-compose logs -f api
docker-compose logs -f --tail=100 api

# Docker direto
docker logs -f amldo-api

# Logs em arquivo
tail -f logs/amldo.log
```

### Métricas

**Endpoint de métricas**:
```bash
curl http://localhost:8000/api/metrics/stats

# Resposta:
{
  "rag_stats": [...],
  "total_files_processed": 15,
  "total_chunks_indexed": 2500,
  "queries_last_24h": 150
}
```

**Banco de métricas SQLite**:
```bash
sqlite3 data/metrics/metrics.db

SELECT * FROM query_history ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM processing_history;
```

---

## 🛠️ Troubleshooting

### Problema: Container não inicia

**Sintomas**:
```
docker-compose up → ERROR
```

**Soluções**:
```bash
# 1. Verificar logs
docker-compose logs api

# 2. Verificar .env
cat .env | grep GOOGLE_API_KEY

# 3. Rebuild completo
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# 4. Verificar portas
netstat -tuln | grep 8000
```

### Problema: Health check falhando

**Sintomas**:
```
Container status: (unhealthy)
```

**Soluções**:
```bash
# 1. Testar manualmente
curl -v http://localhost:8000/health

# 2. Verificar se API iniciou
docker-compose exec api ps aux | grep python

# 3. Ver logs de erro
docker-compose logs api | grep -i error

# 4. Entrar no container
docker-compose exec api bash
curl localhost:8000/health
```

### Problema: Falta de memória/CPU

**Sintomas**:
```
Container lento ou crashando
```

**Soluções**:
```bash
# 1. Ver uso de recursos
docker stats

# 2. Limitar recursos no docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G

# 3. Cleanup
docker system prune -a
docker volume prune
```

### Problema: Build falha

**Sintomas**:
```
docker build → ERROR
```

**Soluções**:
```bash
# 1. Build com mais output
docker build --progress=plain -t amldo:latest .

# 2. Verificar .dockerignore
cat .dockerignore

# 3. Rebuild sem cache
docker build --no-cache -t amldo:latest .

# 4. Verificar disco
df -h
docker system df
```

---

## 📚 Recursos

### Documentação Relacionada

- [Testes Automatizados](./11-testes-automatizados.md)
- [API FastAPI](./10-api-fastapi.md)
- [Configuração](./04-guia-desenvolvedor.md)

### Links Externos

- [Docker Docs](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Kubernetes Docs](https://kubernetes.io/docs/)

---

## ✅ Checklist de Deploy

### Pre-Deploy

- [ ] Testes passando localmente (`pytest tests/`)
- [ ] Build Docker OK (`docker build -t amldo:latest .`)
- [ ] Arquivo `.env` configurado
- [ ] GOOGLE_API_KEY válida
- [ ] Backup de dados importante (se prod)
- [ ] Migrations executadas (se necessário)

### Deploy

- [ ] CI passou no GitHub Actions
- [ ] Build de imagem Docker OK
- [ ] Deploy executado (`./scripts/deploy.sh`)
- [ ] Serviços iniciados (`docker-compose ps`)
- [ ] Health check OK (`curl /health`)

### Post-Deploy

- [ ] Logs sem erros (`docker-compose logs`)
- [ ] Métricas funcionando (`/api/metrics/stats`)
- [ ] Smoke tests OK (testar endpoints principais)
- [ ] Documentação atualizada (se necessário)
- [ ] Tag criada (se produção)
- [ ] Changelog atualizado

---

**AMLDO v0.3.0** - Infraestrutura moderna de CI/CD 🚀
