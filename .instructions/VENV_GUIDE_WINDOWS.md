# 🪟 Guia Virtual Environment - AMLDO (Windows)

> **Passo-a-passo** para criar e ativar ambiente virtual no **Windows**

---

## 🎯 Contexto

Você está em **Windows**, não em Linux/WSL. Os comandos são diferentes!

**Seu ambiente**:
- Sistema: Windows
- Python: 3.13.1
- Terminal: Git Bash (MINGW64) ou PowerShell ou CMD

---

## ⚡ Método Rápido (RECOMENDADO)

### PowerShell (Recomendado)

Abra **PowerShell** (não Git Bash!) e execute:

```powershell
# Ir para o diretório do projeto
cd D:\PYTHON\AMLDO

# Criar virtual environment
python -m venv venv

# Ativar venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Se der erro de execução, execute antes:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

✅ **Pronto!** O ambiente virtual está ativado.

**Indicador**: Você verá `(venv)` antes do prompt:
```
(venv) PS D:\PYTHON\AMLDO>
```

---

### CMD (Prompt de Comando)

Se preferir CMD:

```cmd
REM Ir para o diretório
cd D:\PYTHON\AMLDO

REM Criar venv
python -m venv venv

REM Ativar venv (CMD)
venv\Scripts\activate.bat
```

**Indicador**: Você verá `(venv)` no prompt:
```
(venv) D:\PYTHON\AMLDO>
```

---

## 📝 Método Manual (Passo-a-Passo)

### 1️⃣ Verificar se Python está instalado

**PowerShell ou CMD**:
```powershell
python --version
```

**Saída esperada**: `Python 3.13.1`

⚠️ **IMPORTANTE**: Python 3.13 é muito recente. Se tiver problemas com dependências, considere instalar Python 3.11 ou 3.12.

**Baixar Python**:
- Python 3.12: https://www.python.org/downloads/release/python-3120/
- Python 3.11: https://www.python.org/downloads/release/python-3110/

---

### 2️⃣ Ir para o diretório do projeto

**PowerShell**:
```powershell
cd D:\PYTHON\AMLDO
```

**CMD**:
```cmd
cd D:\PYTHON\AMLDO
```

**Git Bash** (NÃO RECOMENDADO para venv):
```bash
cd /d/PYTHON/AMLDO
```

**Verificar**:
```powershell
pwd  # PowerShell
cd   # CMD/Git Bash
```

---

### 3️⃣ Remover venv antigo (se existir e estiver corrompido)

**PowerShell**:
```powershell
# Verificar se existe
Test-Path venv\Scripts\activate

# Se retornar False, o venv está corrompido
# Remover
Remove-Item -Recurse -Force venv
```

**CMD**:
```cmd
REM Remover venv antigo
rmdir /s /q venv
```

---

### 4️⃣ Criar Virtual Environment

**PowerShell ou CMD**:
```powershell
python -m venv venv
```

**Aguardar**: Leva ~30-60 segundos

**Verificar criação**:
```powershell
# PowerShell
Test-Path venv\Scripts\activate.ps1
Test-Path venv\Scripts\activate.bat

# CMD
dir venv\Scripts\activate*
```

**✅ Sucesso**: Se os arquivos de ativação existirem, o venv foi criado corretamente!

---

### 5️⃣ Ativar Virtual Environment

#### PowerShell (Recomendado)

```powershell
.\venv\Scripts\Activate.ps1
```

**Se der erro "não pode ser carregado porque a execução de scripts foi desabilitada"**:

```powershell
# Permitir execução de scripts (UMA VEZ)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Agora ativar
.\venv\Scripts\Activate.ps1
```

#### CMD

```cmd
venv\Scripts\activate.bat
```

#### Git Bash (Limitado - NÃO RECOMENDADO)

```bash
source venv/Scripts/activate
```

⚠️ **Git Bash tem limitações**: Muitos comandos não funcionam. Use PowerShell ou CMD.

---

**✅ Sucesso**: Você verá `(venv)` no prompt:

**PowerShell**:
```
(venv) PS D:\PYTHON\AMLDO>
```

**CMD**:
```
(venv) D:\PYTHON\AMLDO>
```

**Git Bash**:
```
(venv) penhall@Paladino MINGW64 /d/PYTHON/AMLDO
```

---

**Verificar**:
```powershell
# PowerShell/CMD
where python
# Deve mostrar: D:\PYTHON\AMLDO\venv\Scripts\python.exe

python --version
# Deve mostrar: Python 3.13.1
```

---

### 6️⃣ Instalar Dependências (primeira vez)

**IMPORTANTE**: Python 3.13 é muito novo. Algumas bibliotecas podem não ter wheels compilados ainda.

```powershell
# Atualizar pip
python -m pip install --upgrade pip

# Instalar projeto em modo editável
pip install -e ".[api,adk,streamlit]"

# OU instalar apenas API
pip install -e ".[api]"
```

**Aguardar**: Pode demorar 3-7 minutos

⚠️ **Se tiver erros de compilação**: Algumas bibliotecas podem precisar de compiladores C++ (não disponíveis por padrão no Windows).

**Solução**:
1. Instalar Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
2. OU usar Python 3.11/3.12 (têm melhor suporte de bibliotecas)

**Verificar instalação**:
```powershell
pip show amldo
# Deve mostrar: amldo 0.3.0

where amldo-api
# Deve mostrar: D:\PYTHON\AMLDO\venv\Scripts\amldo-api.exe
```

---

### 7️⃣ Desativar Virtual Environment

Quando terminar de trabalhar:

```powershell
deactivate
```

**Resultado**: O `(venv)` desaparece do prompt

---

## 🔧 Troubleshooting (Windows)

### Problema 1: "python: command not found" (Git Bash)

**Causa**: Git Bash não encontra Python do Windows

**Solução 1**: Usar PowerShell ou CMD
```powershell
# Abrir PowerShell e usar lá
```

**Solução 2**: Adicionar Python ao PATH do Git Bash
```bash
# Adicionar ao ~/.bashrc
export PATH="/c/Users/SEU_USUARIO/AppData/Local/Programs/Python/Python313:$PATH"
export PATH="/c/Users/SEU_USUARIO/AppData/Local/Programs/Python/Python313/Scripts:$PATH"
```

---

### Problema 2: "sed: command not found" (Git Bash)

**Causa**: Git Bash tem conjunto limitado de comandos Unix

**Solução**: **NÃO use Git Bash** para desenvolvimento Python. Use:
- **PowerShell** (recomendado)
- **CMD**
- **Windows Terminal** (PowerShell moderno)

---

### Problema 3: "Activate.ps1 cannot be loaded" (PowerShell)

**Erro completo**:
```
Activate.ps1 cannot be loaded because running scripts is disabled on this system
```

**Causa**: Política de execução do PowerShell

**Solução**:
```powershell
# Ver política atual
Get-ExecutionPolicy

# Permitir scripts locais (recomendado)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ativar novamente
.\venv\Scripts\Activate.ps1
```

---

### Problema 4: venv não ativa (sem erro)

**Causa**: Você executou `venv\Scripts\activate.ps1` sem `.\` no PowerShell

**Solução**:
```powershell
# ✅ CORRETO (PowerShell)
.\venv\Scripts\Activate.ps1

# ❌ ERRADO
venv\Scripts\Activate.ps1

# ✅ CORRETO (CMD)
venv\Scripts\activate.bat
```

---

### Problema 5: Erros de compilação ao instalar pacotes

**Erro**: `error: Microsoft Visual C++ 14.0 or greater is required`

**Causa**: Algumas bibliotecas precisam compilar código C/C++

**Solução 1**: Instalar Visual C++ Build Tools
- Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Instalar "Desktop development with C++"

**Solução 2**: Usar Python 3.11 ou 3.12
- Têm melhor suporte de wheels pré-compilados
- Download: https://www.python.org/downloads/

---

### Problema 6: Python 3.13 incompatível com bibliotecas

**Sintomas**: Erros ao importar módulos, crashes, warnings

**Causa**: Python 3.13 é muito recente (Outubro 2024)

**Solução**: Usar Python 3.11 ou 3.12
```powershell
# Desinstalar Python 3.13 (Painel de Controle > Programas)
# Baixar e instalar Python 3.12
# https://www.python.org/downloads/release/python-3120/

# Recriar venv com Python 3.12
cd D:\PYTHON\AMLDO
rmdir /s /q venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e ".[api]"
```

---

## 📋 Comandos Úteis (Windows)

### Verificar se venv está ativo

**PowerShell**:
```powershell
# Método 1: Ver prompt
# Se tiver (venv) → está ativo

# Método 2: Verificar caminho do Python
where python
# Ativo: D:\PYTHON\AMLDO\venv\Scripts\python.exe
# Inativo: C:\Users\...\AppData\Local\Programs\Python\...

# Método 3: Verificar variável de ambiente
$env:VIRTUAL_ENV
# Ativo: D:\PYTHON\AMLDO\venv
# Inativo: (vazio)
```

**CMD**:
```cmd
where python
echo %VIRTUAL_ENV%
```

---

### Listar pacotes instalados

```powershell
pip list
```

---

### Verificar se AMLDO está instalado

```powershell
pip show amldo
```

---

### Reinstalar AMLDO

```powershell
pip install -e ".[api]" --force-reinstall
```

---

## 🎯 Workflow Diário (Windows)

### Ao começar a trabalhar:

**PowerShell**:
```powershell
cd D:\PYTHON\AMLDO
.\venv\Scripts\Activate.ps1
```

**CMD**:
```cmd
cd D:\PYTHON\AMLDO
venv\Scripts\activate.bat
```

---

### Trabalhar normalmente:

```powershell
# Executar API
amldo-api

# Executar testes
pytest tests\

# Executar scripts (PowerShell)
.\scripts\run_webapp_new.ps1  # Se existir versão PowerShell
# OU
python src\amldo\interfaces\api\run.py
```

---

### Ao terminar:

```powershell
deactivate
```

---

## 🚀 Scripts para Windows

Os scripts em `scripts/` são **shell scripts (.sh)** para Linux/WSL/Git Bash.

Para Windows, você tem **3 opções**:

### Opção 1: Usar Python diretamente (RECOMENDADO)

**PowerShell ou CMD**:
```powershell
# API nova (v0.3.0)
python src\amldo\interfaces\api\run.py

# Streamlit
streamlit run src\amldo\interfaces\streamlit\app.py

# ADK
adk web
```

---

### Opção 2: Criar scripts PowerShell (.ps1)

Posso criar versões PowerShell dos scripts se você quiser:
- `run_webapp_new.ps1`
- `run_webapp_old.ps1`
- `run_both_webapps.ps1`

---

### Opção 3: Usar Git Bash (LIMITADO)

Git Bash pode executar os scripts `.sh`, mas com limitações:

```bash
# Ativar venv no Git Bash
source venv/Scripts/activate

# Executar scripts
bash scripts/run_webapp_new.sh  # Pode não funcionar totalmente
```

⚠️ **Não recomendado**: Git Bash não tem comandos como `sed`, `lsof`, `ps`, etc.

---

## 💡 Recomendações para Windows

### 1. Use PowerShell (não Git Bash)

PowerShell é o terminal nativo do Windows e tem melhor suporte a Python.

**Abrir PowerShell**:
- Pressione `Win + X` → "Windows PowerShell"
- OU `Win + R` → digite `powershell` → Enter

---

### 2. Use Python 3.11 ou 3.12 (não 3.13)

Python 3.13 é muito recente. AMLDO foi testado com 3.11/3.12.

**Verificar versão**:
```powershell
python --version
```

**Se tiver 3.13 e problemas**: Considere instalar 3.12 em paralelo.

---

### 3. Instale Windows Terminal (opcional)

Windows Terminal é moderno e suporta PowerShell, CMD, Git Bash em abas.

**Download**: Microsoft Store → "Windows Terminal"

---

## 📚 Comandos de Ativação - Resumo

| Terminal | Criar venv | Ativar venv | Desativar |
|----------|-----------|-------------|-----------|
| **PowerShell** | `python -m venv venv` | `.\venv\Scripts\Activate.ps1` | `deactivate` |
| **CMD** | `python -m venv venv` | `venv\Scripts\activate.bat` | `deactivate` |
| **Git Bash** | `python -m venv venv` | `source venv/Scripts/activate` | `deactivate` |

---

## ✅ Checklist (Windows)

Antes de executar qualquer comando do AMLDO:

- [ ] Estou usando **PowerShell** ou **CMD** (não Git Bash)
- [ ] Estou no diretório correto (`D:\PYTHON\AMLDO`)
- [ ] Venv está ativado (vejo `(venv)` no prompt)
- [ ] `where python` mostra `...\venv\Scripts\python.exe`
- [ ] `.env` está configurado com `GOOGLE_API_KEY`
- [ ] Dependências instaladas (`pip show amldo`)

---

## 🆘 Ajuda Rápida (Windows)

### Não consegue ativar venv?

**PowerShell**:
```powershell
# Copie e cole EXATAMENTE:
cd D:\PYTHON\AMLDO
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
where python
```

**CMD**:
```cmd
cd D:\PYTHON\AMLDO
venv\Scripts\activate.bat
where python
```

**Se mostrar** `...\venv\Scripts\python.exe` → ✅ Funcionou!

---

### Venv corrompido?

```powershell
# Recriar do zero (PowerShell):
cd D:\PYTHON\AMLDO
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[api]"
```

```cmd
REM Recriar do zero (CMD):
cd D:\PYTHON\AMLDO
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[api]"
```

**Aguarde** ~3-5 minutos para concluir.

---

## 📞 Ainda com problemas?

Se nada funcionar, me mande a saída destes comandos (PowerShell):

```powershell
cd D:\PYTHON\AMLDO
python --version
where python
Test-Path venv\Scripts\activate.ps1
$env:VIRTUAL_ENV
Get-Content venv\pyvenv.cfg
```

---

**Criado para**: AMLDO v0.3.0
**Sistema**: Windows 10/11
**Python**: 3.11+ (recomendado 3.11 ou 3.12, não 3.13)
**Última atualização**: 2025-11-16

🪟 **Comando único para setup completo (PowerShell)**:
```powershell
cd D:\PYTHON\AMLDO; Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue; python -m venv venv; .\venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -e ".[api,adk,streamlit]"
```
