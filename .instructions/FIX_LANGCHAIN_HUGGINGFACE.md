# ⚡ Fix Rápido - Erros de Dependências

> **Soluções imediatas** para erros comuns de dependências no AMLDO

---

## 🔴 Problema 1: Keras 3 Incompatível

### Erro

```
ValueError: Your currently installed version of Keras is Keras 3, but this is not yet supported in Transformers.
Please install the backwards-compatible tf-keras package with `pip install tf-keras`.
```

### ✅ Solução (30 segundos)

```bash
pip install tf-keras
```

**Pronto!** O transformers agora vai usar `tf-keras` que é compatível.

### Verificar

```bash
python -c "import tf_keras; print('✅ tf-keras instalado!')"
```

---

## 🟡 Problema 2: langchain_huggingface não encontrado

### Erro

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

## 🔵 Problema 3: AttributeError com MessageFactory

### Erro

```
AttributeError: 'MessageFactory' object has no attribute 'GetPrototype'
```

### ✅ Solução

Este erro geralmente está relacionado a incompatibilidades de versão do protobuf. Tente:

```bash
pip install --upgrade protobuf
```

Ou force uma versão específica compatível:

```bash
pip install "protobuf<4.0.0"
```

---

## 🟢 Problema 4: TensorFlow oneDNN

### Aviso

```
I tensorflow/core/util/port.cc:153] oneDNN custom operations are on.
```

Este é apenas um **aviso informativo**, não um erro. Para desabilitar se desejar:

```bash
# Windows (PowerShell)
$env:TF_ENABLE_ONEDNN_OPTS="0"

# Linux/Mac
export TF_ENABLE_ONEDNN_OPTS=0
```

Ou adicione ao `.env`:
```
TF_ENABLE_ONEDNN_OPTS=0
```

---

## 🛠️ Solução Completa (se nada funcionou)

Se você está tendo múltiplos erros, reinstale tudo com versões compatíveis:

```bash
# 1. Instalar tf-keras (Keras compatível)
pip install tf-keras

# 2. Instalar langchain-huggingface
pip install langchain-huggingface

# 3. Reinstalar projeto
pip install -e ".[api,adk,streamlit]" --force-reinstall

# 4. Verificar
python scripts/run.py --api
```

---

## 📋 Resumo de Comandos Rápidos

```bash
# Keras 3 incompatível
pip install tf-keras

# langchain_huggingface faltando
pip install langchain-huggingface

# protobuf incompatível
pip install --upgrade protobuf

# Reinstalar tudo
pip install -e ".[api,adk,streamlit]" --force-reinstall
```

---

**Criado para**: AMLDO v0.3.0
**Sistemas**: Windows, Linux, Mac
**Tempo de fix**: ~30 segundos a 3 minutos
**Última atualização**: 2025-11-17
