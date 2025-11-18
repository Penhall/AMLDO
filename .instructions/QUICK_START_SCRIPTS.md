# Quick Start - Scripts de Execução

> Scripts prontos para subir rapidamente as duas webapps do AMLDO (nova e antiga).

---

## Uso Rápido

### 1) Executar WebApp ANTIGA (porta 8001)

**Linux / WSL (bash)**

```bash
cd /mnt/d/PYTHON/AMLDO
./scripts/run_webapp_old.sh
```

**Windows (PowerShell)**

```powershell
cd D:\PYTHON\AMLDO
.\scripts\run_webapp_old.ps1
```

Acesse: http://localhost:8001

---

### 2) Executar WebApp NOVA v0.3.0 (porta 8000)

**Linux / WSL (bash)**

```bash
cd /mnt/d/PYTHON/AMLDO
./scripts/run_webapp_new.sh
```

**Windows (PowerShell)**

```powershell
cd D:\PYTHON\AMLDO
.\scripts\run_webapp_new.ps1
```

Acesse:
- API:  http://localhost:8000
- Docs: http://localhost:8000/docs
- Chat: http://localhost:8000/consulta

---

### 3) Executar AMBAS WebApps ao mesmo tempo

**Linux / WSL (bash)**

```bash
cd /mnt/d/PYTHON/AMLDO

# Iniciar ambas
./scripts/run_both_webapps.sh

# Parar ambas
./scripts/run_both_webapps.sh stop
```

**Windows (PowerShell)**

```powershell
cd D:\PYTHON\AMLDO

# Iniciar ambas em janelas separadas do PowerShell
.\scripts\run_both_webapps.ps1

# Parar ambas usando os PIDs salvos
.\scripts\run_both_webapps.ps1 stop
```

URLs:
- WebApp Antiga: http://localhost:8001
- WebApp Nova:   http://localhost:8000

---

## Duas WebApps Diferentes

O projeto AMLDO possui **duas** webapps:

| WebApp   | Localização                    | Porta | Descrição                |
|----------|--------------------------------|-------|--------------------------|
| Antiga   | `AMLDO_W/AMLDO/webapp/`        | 8001  | Versão original (POC)    |
| Nova     | `src/amldo/interfaces/api/`    | 8000  | v0.3.0 (produção)        |

Resumo:
- WebApp Antiga: FastAPI simples, upload de PDFs, RAG básico.
- WebApp Nova: FastAPI completa, RAG v1/v2/v3, métricas, UI Bootstrap 5, docs Swagger.

Para detalhes, veja `WEBAPPS_GUIDE.md`.

---

## Scripts Disponíveis

### Scripts das WebApps

| Script                        | Plataforma        | Descrição                        | Porta        |
|-------------------------------|-------------------|----------------------------------|-------------|
| `run_webapp_old.sh`           | Linux / WSL       | WebApp antiga (original)         | 8001        |
| `run_webapp_new.sh`           | Linux / WSL       | WebApp nova (v0.3.0)             | 8000        |
| `run_both_webapps.sh`         | Linux / WSL       | Ambas webapps simultaneamente    | 8000 + 8001 |
| `run_webapp_old.ps1`          | Windows PowerShell| WebApp antiga (original)         | 8001        |
| `run_webapp_new.ps1`          | Windows PowerShell| WebApp nova (v0.3.0)             | 8000        |
| `run_both_webapps.ps1`        | Windows PowerShell| Ambas webapps simultaneamente    | 8000 + 8001 |

### Outros scripts

| Script            | Descrição                                         |
|-------------------|---------------------------------------------------|
| `run_amldo.sh`    | Executa AMLDO v0.3.0 (api/streamlit/adk/all)      |
| `run_tests.sh`    | Executa testes                                    |
| `deploy.sh`       | Deploy em ambientes                               |

Todos ficam em `scripts/`.

---

## Cenários Comuns

### Cenário 1: Testar WebApp Nova (recomendado)

**Linux / WSL**

```bash
./scripts/run_webapp_new.sh
```

**Windows**

```powershell
.\scripts\run_webapp_new.ps1
```

---

### Cenário 2: Comparar as duas versões lado a lado

**Linux / WSL**

```bash
./scripts/run_both_webapps.sh
```

**Windows**

```powershell
.\scripts\run_both_webapps.ps1
```

Depois compare:
- Antiga: http://localhost:8001
- Nova:   http://localhost:8000

Para parar:

**Linux / WSL**

```bash
./scripts/run_both_webapps.sh stop
```

**Windows**

```powershell
.\scripts\run_both_webapps.ps1 stop
```

---

### Cenário 3: Só WebApp Antiga para teste rápido

**Linux / WSL**

```bash
./scripts/run_webapp_old.sh
```

**Windows**

```powershell
.\scripts\run_webapp_old.ps1
```

Acesse: http://localhost:8001

---

## Configuração Inicial

### WebApp Antiga

1. Verificar `.env` em `AMLDO_W/AMLDO/`:

```bash
ls AMLDO_W/AMLDO/.env
```

2. Se não existir, criar:

```bash
cd AMLDO_W/AMLDO
nano .env   # ou notepad .env no Windows
```

Preencha com as variáveis necessárias da webapp antiga.

---

### WebApp Nova

1. Verificar `.env` na raiz:

```bash
cat .env | grep GOOGLE_API_KEY
```

2. Se não existir:

```bash
cp .env.example .env
nano .env   # ou notepad .env no Windows
```

3. Configure:

```text
GOOGLE_API_KEY= SUA_CHAVE_AQUI
```

4. Instalar dependências (venv ativo):

```bash
pip install -e ".[api]"
```

---

## Troubleshooting Rápido

### "Permission denied" ao executar `.sh` (Linux/WSL)

```bash
chmod +x scripts/*.sh
```

### WebApp Antiga não inicia

```bash
ls AMLDO_W/AMLDO/.env
cd AMLDO_W/AMLDO
pip install -r requirements.txt
```

### WebApp Nova não inicia

```bash
cat .env | grep GOOGLE_API_KEY
pip install -e ".[api]"
```

### Porta 8000 ou 8001 em uso

Linux/WSL:

```bash
lsof -i :8000
lsof -i :8001
kill -9 PID
```

Windows (PowerShell):

```powershell
netstat -ano | Select-String ":8000"
netstat -ano | Select-String ":8001"
Stop-Process -Id <PID> -Force
```

---

## Checklist

- [ ] Scripts `.sh` com permissão de execução (Linux/WSL)
- [ ] `.env` configurado na raiz (WebApp Nova)
- [ ] `.env` configurado em `AMLDO_W/AMLDO/` (WebApp Antiga)
- [ ] `GOOGLE_API_KEY` configurada (WebApp Nova)
- [ ] Virtual environment criado e ativado

---

Criado para: AMLDO v0.3.0  
Última atualização: 2025-11-16

