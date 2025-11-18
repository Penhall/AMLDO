# ⚡ Fix Rápido - Erro langchain_huggingface

> **Solução imediata** para `ModuleNotFoundError: No module named 'langchain_huggingface'`

---

## 🎯 O Problema

Você executou `amldo-api` e recebeu:

```
ModuleNotFoundError: No module named 'langchain_huggingface'
```

## ✅ A Solução (1 minuto)

### PowerShell (com venv ativado)

Copie e cole no PowerShell:

```powershell
# Reinstalar projeto (isso vai pegar a dependência faltante)
pip install -e ".[api,adk,streamlit]" --force-reinstall --no-cache-dir
```

**Aguarde**: ~2-3 minutos (vai baixar e instalar pacotes)

---

## 🔍 Verificar se Resolveu

```powershell
# 1. Verificar se langchain-huggingface está instalado
pip show langchain-huggingface

# Deve mostrar:
# Name: langchain-huggingface
# Version: 0.x.x
```

```powershell
# 2. Testar import
python -c "from langchain_huggingface import HuggingFaceEmbeddings; print('✅ OK!')"

# Deve mostrar: ✅ OK!
```

```powershell
# 3. Executar API
amldo-api

# Deve mostrar:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🚀 Próximos Passos

Se funcionou:

1. **Acessar a API**: http://localhost:8000
2. **Ver documentação**: http://localhost:8000/docs
3. **Usar interface de chat**: http://localhost:8000/consulta

---

## 🔧 Se Ainda Não Funcionar

### Opção 1: Instalar apenas a dependência faltante

```powershell
# Instalar langchain-huggingface diretamente
pip install langchain-huggingface

# Verificar
pip show langchain-huggingface

# Tentar executar novamente
amldo-api
```

### Opção 2: Reinstalação completa

```powershell
# Desativar venv
deactivate

# Remover venv
Remove-Item -Recurse -Force venv

# Criar novo venv
python -m venv venv

# Ativar
.\venv\Scripts\Activate.ps1

# Instalar tudo de novo
python -m pip install --upgrade pip
pip install -e ".[api,adk,streamlit]"

# Executar
amldo-api
```

---

## 📋 O Que Foi Corrigido?

O arquivo `pyproject.toml` foi atualizado para incluir `langchain-huggingface` nas dependências.

**Antes**:
```toml
dependencies = [
    "langchain>=0.1.0",
    "langchain-community>=0.0.20",
    "langchain-google-genai>=0.0.6",
    # langchain-huggingface estava FALTANDO!
    "sentence-transformers>=2.2.0",
    ...
]
```

**Depois**:
```toml
dependencies = [
    "langchain>=0.1.0",
    "langchain-community>=0.0.20",
    "langchain-google-genai>=0.0.6",
    "langchain-huggingface>=0.0.1",  # ← ADICIONADO!
    "sentence-transformers>=2.2.0",
    ...
]
```

---

## ⚠️ Por Que Aconteceu?

O código em `src/amldo/rag/v1/tools.py` (e v2, v3) usa:

```python
from langchain_huggingface import HuggingFaceEmbeddings
```

Mas essa dependência não estava listada no `pyproject.toml`, então não foi instalada automaticamente.

Agora está corrigido! ✅

---

**Criado para**: AMLDO v0.3.0
**Sistema**: Windows
**Tempo de fix**: ~2-3 minutos
**Última atualização**: 2025-11-16
