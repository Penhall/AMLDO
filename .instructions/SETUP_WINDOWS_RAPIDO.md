# ⚡ Setup Rápido - AMLDO no Windows

> **Solução específica** para o seu problema no Windows

---

## 🚨 SUA SITUAÇÃO ATUAL

- **Sistema**: Windows (não WSL!)
- **Python**: 3.13.1 (muito recente - pode dar problemas)
- **Terminal atual**: Git Bash (MINGW64) - **NÃO FUNCIONA BEM** para Python
- **Problema**: `sed: command not found`, `python: command not found`

---

## ✅ SOLUÇÃO: Use PowerShell!

O Git Bash tem limitações no Windows. **Use PowerShell** para trabalhar com Python.

---

## 🎯 Passos Rápidos (PowerShell)

### 1. Abrir PowerShell

- Pressione `Win + X`
- Clique em **"Windows PowerShell"** ou **"Terminal"**

---

### 2. Ir para o diretório do projeto

```powershell
cd D:\PYTHON\AMLDO
```

---

### 3. Verificar Python

```powershell
python --version
```

**Deve mostrar**: `Python 3.13.1`

⚠️ **AVISO**: Python 3.13 é muito novo (Outubro 2024). Se tiver problemas, baixe Python 3.12: https://www.python.org/downloads/release/python-3120/

---

### 4. Criar Virtual Environment

```powershell
python -m venv venv
```

**Aguarde**: ~30-60 segundos

---

### 5. Permitir execução de scripts (primeira vez)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Digite **"S"** (Sim) ou **"Y"** (Yes) quando solicitado.

---

### 6. Ativar venv

```powershell
.\venv\Scripts\Activate.ps1
```

**✅ Sucesso**: Você verá `(venv)` no prompt:
```
(venv) PS D:\PYTHON\AMLDO>
```

---

### 7. Verificar ativação

```powershell
where python
```

**Deve mostrar**: `D:\PYTHON\AMLDO\venv\Scripts\python.exe`

---

### 8. Instalar dependências

```powershell
python -m pip install --upgrade pip
pip install -e ".[api,adk,streamlit]"
```

**Aguarde**: ~3-7 minutos

⚠️ **Se tiver erros de compilação**: Python 3.13 pode ter problemas com algumas bibliotecas. Considere usar Python 3.12.

---

### 9. Verificar instalação

```powershell
pip show amldo
```

**Deve mostrar**:
```
Name: amldo
Version: 0.3.0
```

---

## 🚀 Executar AMLDO

Com o venv ativado:

### API Nova (v0.3.0) - Recomendado

```powershell
amldo-api
```

Acesse: http://localhost:8000

---

### Streamlit

```powershell
streamlit run src\amldo\interfaces\streamlit\app.py
```

Acesse: http://localhost:8501

---

### ADK

```powershell
adk web
```

Acesse: http://localhost:8080

---

## 📝 Workflow Diário

### Ao começar a trabalhar:

```powershell
cd D:\PYTHON\AMLDO
.\venv\Scripts\Activate.ps1
```

### Ao terminar:

```powershell
deactivate
```

---

## 🔧 Troubleshooting

### Erro: "Activate.ps1 cannot be loaded"

**Solução**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

### Erro: Problemas ao instalar pacotes (Python 3.13)

**Sintomas**:
- `error: Microsoft Visual C++ 14.0 or greater is required`
- Falhas ao compilar bibliotecas

**Solução 1**: Instalar Visual C++ Build Tools
- Download: https://visualstudio.microsoft.com/downloads/
- Instalar "Desktop development with C++"

**Solução 2 (RECOMENDADA)**: Usar Python 3.12

1. Baixar Python 3.12: https://www.python.org/downloads/release/python-3120/
2. Instalar (marque "Add to PATH")
3. Recriar venv:
```powershell
cd D:\PYTHON\AMLDO
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e ".[api]"
```

---

### Git Bash não funciona

**Problema**: Git Bash tem comandos limitados (`sed`, `lsof`, `ps` não funcionam)

**Solução**: **NÃO use Git Bash** para desenvolvimento Python no Windows.

Use:
- ✅ **PowerShell** (recomendado)
- ✅ **CMD** (funciona)
- ✅ **Windows Terminal** (PowerShell moderno)
- ❌ Git Bash (limitado)

---

## 📊 Comparação de Terminais (Windows)

| Terminal | Criar venv | Ativar venv | Executar Python | Scripts .sh | Recomendado |
|----------|-----------|-------------|----------------|-------------|-------------|
| **PowerShell** | ✅ | ✅ `.\venv\Scripts\Activate.ps1` | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **CMD** | ✅ | ✅ `venv\Scripts\activate.bat` | ✅ | ❌ | ⭐⭐⭐ |
| **Git Bash** | ⚠️ | ⚠️ `source venv/Scripts/activate` | ❌ (sem PATH) | ⚠️ (limitado) | ⭐ |
| **WSL** | ✅ | ✅ `source venv/bin/activate` | ✅ | ✅ | ⭐⭐⭐⭐ |

---

## 🎯 Comando Único (PowerShell)

Se quiser fazer tudo de uma vez:

```powershell
cd D:\PYTHON\AMLDO; Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue; python -m venv venv; Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser; .\venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -e ".[api,adk,streamlit]"
```

**Tempo total**: ~5-10 minutos

---

## 📚 Próximos Passos

1. **Configurar .env**:
```powershell
# Copiar exemplo
Copy-Item .env.example .env

# Editar com Notepad
notepad .env
# Adicionar: GOOGLE_API_KEY=sua_chave_aqui
```

2. **Executar API**:
```powershell
amldo-api
```

3. **Acessar**:
- http://localhost:8000 - API
- http://localhost:8000/docs - Documentação
- http://localhost:8000/consulta - Chat

---

## ⚠️ Importante: Scripts .sh não funcionam nativamente no Windows

Os scripts em `scripts/` são para Linux/WSL:
- `run_webapp_new.sh`
- `run_webapp_old.sh`
- `run_both_webapps.sh`

**Para Windows**, use comandos Python diretamente:

```powershell
# Em vez de ./scripts/run_webapp_new.sh
amldo-api

# Em vez de ./scripts/run_webapp_old.sh
cd AMLDO_W\AMLDO\webapp
python -m uvicorn main:app --reload --port 8001
```

---

## 💡 Dicas

### 1. Adicione Python ao PATH

Se `python --version` não funcionar, Python não está no PATH:

1. Painel de Controle → Sistema → Configurações avançadas do sistema
2. Variáveis de Ambiente
3. PATH → Editar
4. Adicionar: `C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python313`
5. Adicionar: `C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python313\Scripts`

### 2. Use Windows Terminal

Windows Terminal é mais moderno que PowerShell padrão:
- Download: Microsoft Store → "Windows Terminal"
- Suporta múltiplas abas (PowerShell, CMD, Git Bash)

### 3. VSCode Terminal

Configure VSCode para usar PowerShell por padrão:
1. VSCode → Settings (Ctrl+,)
2. Buscar: "terminal default profile"
3. Selecionar: "PowerShell"

---

## ✅ Checklist Final

Após setup, verifique:

- [ ] `python --version` mostra Python 3.13.1 (ou 3.12/3.11)
- [ ] `where python` mostra `D:\PYTHON\AMLDO\venv\Scripts\python.exe`
- [ ] `pip show amldo` mostra `Version: 0.3.0`
- [ ] `where amldo-api` mostra `...\venv\Scripts\amldo-api.exe`
- [ ] Arquivo `.env` existe e tem `GOOGLE_API_KEY`

---

**Criado para**: Windows 10/11
**Python**: 3.13.1 (recomendado: 3.11 ou 3.12)
**Terminal**: PowerShell
**Última atualização**: 2025-11-16

🪟 **Tudo pronto para Windows!**
