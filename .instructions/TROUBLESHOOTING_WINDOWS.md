# 🔧 Troubleshooting - AMLDO no Windows

> **Soluções para problemas comuns** ao executar AMLDO no Windows

---

## 🚨 Erro: `ModuleNotFoundError: No module named 'langchain_huggingface'`

### Sintoma

Ao executar `amldo-api`, você recebe:

```
Traceback (most recent call last):
  File "D:\PYTHON\AMLDO\venv\Scripts\amldo-api.exe\__main__.py", line 2, in <module>
    from amldo.interfaces.api.run import main
  File "D:\PYTHON\AMLDO\src\amldo\interfaces\api\main.py", line 17, in <module>
    from amldo.interfaces.api.routers import query, upload, metrics
  File "D:\PYTHON\AMLDO\src\amldo\interfaces\api\routers\query.py", line 18, in <module>
    from amldo.rag.v1.tools import consultar_base_rag as rag_v1
  File "D:\PYTHON\AMLDO\src\amldo\rag\v1\tools.py", line 10, in <module>
    from langchain_huggingface import HuggingFaceEmbeddings
ModuleNotFoundError: No module named 'langchain_huggingface'
```

### Causa

A dependência `langchain-huggingface` estava faltando no `pyproject.toml`. Isso já foi corrigido!

### Solução

**PowerShell** (com venv ativado):

```powershell
# Reinstalar o projeto em modo editável
pip install -e ".[api,adk,streamlit]" --force-reinstall --no-cache-dir
```

**OU** instalar apenas a dependência faltante:

```powershell
# Instalar apenas langchain-huggingface
pip install langchain-huggingface

# Depois reinstalar AMLDO
pip install -e ".[api]"
```

### Verificar se resolveu

```powershell
# Listar pacotes instalados
pip list | Select-String langchain

# Deve mostrar:
# langchain                  x.x.x
# langchain-community        x.x.x
# langchain-google-genai     x.x.x
# langchain-huggingface      x.x.x   ← Deve aparecer!
```

```powershell
# Testar import
python -c "from langchain_huggingface import HuggingFaceEmbeddings; print('OK')"

# Deve mostrar: OK
```

```powershell
# Executar API
amldo-api
```

---

## 🚨 Erro: `error: Microsoft Visual C++ 14.0 or greater is required`

### Sintoma

Ao instalar dependências com `pip install`, você recebe:

```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
```

### Causa

Algumas bibliotecas Python (como `faiss-cpu`, `numpy`) precisam compilar código C/C++, mas o compilador não está instalado no Windows.

### Solução 1: Instalar Build Tools (Recomendado)

1. **Baixar Visual Studio Build Tools**:
   - https://visualstudio.microsoft.com/downloads/
   - Procure por "Build Tools for Visual Studio 2022"

2. **Instalar com "Desktop development with C++"**:
   - Execute o instalador
   - Marque "Desktop development with C++"
   - Clique em "Install"
   - **Aguarde**: ~2-5 GB de download

3. **Reiniciar PowerShell** e tentar novamente:
   ```powershell
   pip install -e ".[api]"
   ```

### Solução 2: Usar Python 3.11 ou 3.12

Python 3.13 é muito recente. Versões anteriores têm melhor suporte de wheels pré-compilados.

1. **Desinstalar Python 3.13**:
   - Painel de Controle → Programas → Desinstalar Python 3.13

2. **Baixar Python 3.12**:
   - https://www.python.org/downloads/release/python-3120/
   - Escolha "Windows installer (64-bit)"
   - **Marque**: "Add Python to PATH"

3. **Instalar**

4. **Recriar venv**:
   ```powershell
   cd D:\PYTHON\AMLDO
   Remove-Item -Recurse -Force venv
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -e ".[api]"
   ```

---

## 🚨 Erro: `Activate.ps1 cannot be loaded`

### Sintoma

Ao tentar ativar venv no PowerShell:

```
.\venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

### Causa

Política de execução de scripts do PowerShell está bloqueando.

### Solução

**PowerShell** (como Administrador ou usuário normal):

```powershell
# Ver política atual
Get-ExecutionPolicy

# Permitir scripts locais (recomendado)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Responder: S (Sim) ou Y (Yes)

# Agora ativar venv
.\venv\Scripts\Activate.ps1
```

**Explicação**:
- `RemoteSigned`: Permite scripts locais, mas exige assinatura para scripts baixados
- `Scope CurrentUser`: Aplica apenas ao seu usuário (não precisa de admin)

---

## 🚨 Erro: `python: command not found` (Git Bash)

### Sintoma

No Git Bash:

```bash
$ python --version
bash: python: command not found
```

### Causa

Git Bash não encontra Python do Windows por padrão.

### Solução 1: **Usar PowerShell** (RECOMENDADO)

Git Bash tem limitações no Windows. Use PowerShell:

```powershell
# PowerShell
python --version
```

### Solução 2: Adicionar Python ao PATH do Git Bash

Editar `~/.bashrc`:

```bash
# Abrir .bashrc
nano ~/.bashrc

# Adicionar no final (ajuste o caminho):
export PATH="/c/Users/SEU_USUARIO/AppData/Local/Programs/Python/Python313:$PATH"
export PATH="/c/Users/SEU_USUARIO/AppData/Local/Programs/Python/Python313/Scripts:$PATH"

# Salvar (Ctrl+O, Enter, Ctrl+X)

# Recarregar
source ~/.bashrc

# Testar
python --version
```

**Alternativa**: Criar alias

```bash
# Adicionar ao ~/.bashrc
alias python='/c/Users/SEU_USUARIO/AppData/Local/Programs/Python/Python313/python.exe'
alias pip='/c/Users/SEU_USUARIO/AppData/Local/Programs/Python/Python313/Scripts/pip.exe'
```

---

## 🚨 Erro: `No module named 'amldo'`

### Sintoma

```python
ModuleNotFoundError: No module named 'amldo'
```

### Causa

O pacote não foi instalado em modo editável.

### Solução

```powershell
# Ir para o diretório raiz do projeto
cd D:\PYTHON\AMLDO

# Ativar venv
.\venv\Scripts\Activate.ps1

# Instalar em modo editável
pip install -e ".[api]"

# Verificar
pip show amldo
```

---

## 🚨 Erro: `GOOGLE_API_KEY not found`

### Sintoma

Ao executar `amldo-api`:

```
ValidationError: GOOGLE_API_KEY is required
```

### Causa

Arquivo `.env` não existe ou não tem a chave da API.

### Solução

```powershell
# 1. Criar .env a partir do exemplo
Copy-Item .env.example .env

# 2. Editar .env
notepad .env

# 3. Adicionar sua chave:
# GOOGLE_API_KEY=SUA_CHAVE_AQUI

# 4. Salvar e fechar

# 5. Verificar
Get-Content .env | Select-String GOOGLE_API_KEY
```

**Obter chave da API**:
- https://makersuite.google.com/app/apikey

---

## 🚨 Erro: `FileNotFoundError: data/vector_db/v1_faiss_vector_db`

### Sintoma

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/vector_db/v1_faiss_vector_db'
```

### Causa

O vector store (banco de vetores FAISS) não foi criado ou não está no local esperado.

### Solução 1: Verificar se existe

```powershell
# Verificar se diretório existe
Test-Path data\vector_db\v1_faiss_vector_db

# Se retornar False, o vector store não existe
```

### Solução 2: Clonar repositório completo

O vector store deve vir com o repositório. Se não veio:

```powershell
# Verificar tamanho dos arquivos
Get-ChildItem -Path data\vector_db -Recurse | Measure-Object -Property Length -Sum
```

**Se os arquivos estiverem vazios ou faltando**:

1. Re-clonar repositório
2. OU processar documentos novamente (ver seção abaixo)

### Solução 3: Reprocessar documentos

```powershell
# Ativar venv
.\venv\Scripts\Activate.ps1

# Processar documentos (se tiver PDFs em data/raw/)
python src\amldo\pipeline\main.py

# OU usar script (se existir)
amldo-process --input data\raw\ --output data\processed\

# Construir índice
amldo-build-index --source data\processed\ --output data\vector_db\
```

---

## 🚨 Erro: Port 8000 already in use

### Sintoma

```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): only one usage of each socket address
```

### Causa

Outro processo já está usando a porta 8000.

### Solução 1: Parar o processo

```powershell
# Ver o que está usando porta 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object -Property LocalAddress,LocalPort,OwningProcess

# Identificar o processo
Get-Process -Id PROCESS_ID

# Matar o processo (substitua PID)
Stop-Process -Id PID -Force
```

### Solução 2: Usar outra porta

```powershell
# Executar na porta 8001
$env:API_PORT=8001
amldo-api

# OU editar .env
# API_PORT=8001
```

---

## 🚨 Erro: NumPy 2.x incompatível

### Sintoma

```
ValueError: numpy.dtype size changed, may indicate binary incompatibility
```

### Causa

NumPy 2.x tem breaking changes. AMLDO requer NumPy 1.x.

### Solução

```powershell
# Verificar versão do NumPy
pip show numpy

# Se for 2.x, fazer downgrade
pip install "numpy>=1.24.0,<2.0.0" --force-reinstall
```

---

## 🚨 Venv não ativa (sem erro)

### Sintoma

Você executa `.\venv\Scripts\Activate.ps1` mas não vê `(venv)` no prompt.

### Causa

Você executou sem `.\` ou está em outro terminal.

### Solução

```powershell
# ✅ CORRETO (PowerShell)
.\venv\Scripts\Activate.ps1

# ❌ ERRADO (falta .\)
venv\Scripts\Activate.ps1

# ✅ CORRETO (CMD)
venv\Scripts\activate.bat

# ✅ CORRETO (Git Bash - se configurado)
source venv/Scripts/activate
```

---

## 🚨 Scripts .sh não funcionam no Windows

### Sintoma

```powershell
.\scripts\run_webapp_new.sh
# Erro: cannot be loaded or is not recognized
```

### Causa

Scripts `.sh` são para Linux/WSL. Windows usa PowerShell (`.ps1`) ou Batch (`.bat`).

### Solução

**Usar comandos Python diretamente**:

```powershell
# Em vez de ./scripts/run_webapp_new.sh
amldo-api

# Em vez de ./scripts/run_tests.sh
pytest tests\

# Em vez de ./scripts/run_webapp_old.sh
cd AMLDO_W\AMLDO\webapp
python -m uvicorn main:app --reload --port 8001
```

**Alternativa**: Executar no WSL (se tiver instalado)

```bash
# Abrir WSL
wsl

# Navegar para projeto (Windows D:\ = WSL /mnt/d/)
cd /mnt/d/PYTHON/AMLDO

# Executar script
./scripts/run_webapp_new.sh
```

---

## 🛠️ Comandos Úteis de Diagnóstico

### Verificar instalação completa

```powershell
# 1. Python
python --version

# 2. Venv ativo?
$env:VIRTUAL_ENV  # Deve mostrar caminho do venv

# 3. Onde está o Python?
where python  # Deve mostrar venv\Scripts\python.exe

# 4. AMLDO instalado?
pip show amldo

# 5. Dependências críticas
pip list | Select-String langchain
pip list | Select-String faiss
pip list | Select-String fastapi

# 6. .env existe?
Test-Path .env

# 7. GOOGLE_API_KEY configurada?
Get-Content .env | Select-String GOOGLE_API_KEY

# 8. Vector DB existe?
Test-Path data\vector_db\v1_faiss_vector_db

# 9. Porta 8000 livre?
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

### Reinstalação completa (se tudo falhar)

```powershell
# 1. Ir para diretório
cd D:\PYTHON\AMLDO

# 2. Desativar venv (se ativo)
deactivate

# 3. Remover venv
Remove-Item -Recurse -Force venv

# 4. Criar novo venv
python -m venv venv

# 5. Ativar
.\venv\Scripts\Activate.ps1

# 6. Atualizar pip
python -m pip install --upgrade pip

# 7. Instalar AMLDO
pip install -e ".[api,adk,streamlit]" --no-cache-dir

# 8. Verificar
pip show amldo
pip list | Select-String langchain

# 9. Testar
amldo-api
```

---

## 📞 Ainda com problemas?

Se nenhuma solução funcionou, me envie a saída destes comandos:

```powershell
# Informações do sistema
python --version
where python
$PSVersionTable.PSVersion

# Informações do venv
$env:VIRTUAL_ENV
Test-Path venv\Scripts\activate.ps1

# Informações dos pacotes
pip list
pip show amldo

# Informações do projeto
Get-Content .env.example
Test-Path .env
Get-ChildItem data\vector_db

# Erro completo (ao executar)
amldo-api 2>&1 | Out-File -FilePath error_log.txt
Get-Content error_log.txt
```

---

**Criado para**: AMLDO v0.3.0
**Sistema**: Windows 10/11
**Terminal**: PowerShell
**Última atualização**: 2025-11-16

🔧 **Boas práticas**:
- Sempre use PowerShell (não Git Bash) para Python no Windows
- Use Python 3.11 ou 3.12 (evite 3.13 por enquanto)
- Mantenha venv ativado durante desenvolvimento
- Verifique `.env` antes de executar
