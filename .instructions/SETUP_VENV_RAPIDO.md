# ⚡ Setup Rápido - Virtual Environment AMLDO

> **Comandos prontos** para copiar e colar no terminal Bash

---

## 🚨 PROBLEMA ATUAL

Você tem um **venv corrompido** que precisa ser recriado.

**Sintoma**: O diretório `venv/` existe mas `venv/bin/activate` não existe.

---

## ✅ SOLUÇÃO (Copie e Cole)

### Passo 1: Instalar python3-venv

```bash
sudo apt update
sudo apt install python3.12-venv
```

**Aguarde**: Você precisará digitar sua senha.

---

### Passo 2: Remover venv corrompido e recriar

```bash
cd /mnt/d/PYTHON/AMLDO
rm -rf venv
python3 -m venv venv
```

**Aguarde**: ~30-60 segundos

---

### Passo 3: Ativar venv

```bash
source venv/bin/activate
```

**✅ Sucesso**: Você verá `(venv)` no prompt:
```
(venv) petto@DESKTOP:/mnt/d/PYTHON/AMLDO$
```

---

### Passo 4: Verificar se funcionou

```bash
which python
```

**Deve mostrar**: `/mnt/d/PYTHON/AMLDO/venv/bin/python`

---

### Passo 5: Instalar dependências AMLDO

```bash
pip install --upgrade pip
pip install -e ".[api,adk,streamlit]"
```

**Aguarde**: ~3-5 minutos (muitas dependências)

---

## 🎯 Comandos Resumidos (tudo de uma vez)

Se preferir, copie e cole TUDO de uma vez:

```bash
# 1. Instalar python3-venv (precisa de senha)
sudo apt update && sudo apt install -y python3.12-venv

# 2. Ir para diretório
cd /mnt/d/PYTHON/AMLDO

# 3. Remover venv corrompido
rm -rf venv

# 4. Criar novo venv
python3 -m venv venv

# 5. Ativar venv
source venv/bin/activate

# 6. Verificar
which python

# 7. Instalar dependências
pip install --upgrade pip
pip install -e ".[api,adk,streamlit]"
```

---

## 🔍 Como saber se deu certo?

### 1. Venv está ativo?
```bash
echo $VIRTUAL_ENV
```
**Deve mostrar**: `/mnt/d/PYTHON/AMLDO/venv`

### 2. Python correto?
```bash
which python
```
**Deve mostrar**: `/mnt/d/PYTHON/AMLDO/venv/bin/python`

### 3. AMLDO instalado?
```bash
pip show amldo
```
**Deve mostrar**: `Name: amldo`, `Version: 0.3.0`

### 4. Comando amldo-api existe?
```bash
which amldo-api
```
**Deve mostrar**: `/mnt/d/PYTHON/AMLDO/venv/bin/amldo-api`

---

## 📝 Próximos Passos

Com o venv ativado, você pode:

### Executar a API nova (v0.3.0)
```bash
amldo-api
```
Acesse: http://localhost:8000

### Executar a webapp antiga
```bash
./scripts/run_webapp_old.sh
```
Acesse: http://localhost:8001

### Executar ambas simultaneamente
```bash
./scripts/run_both_webapps.sh
```

### Executar testes
```bash
pytest tests/
```

---

## 🆘 Ainda com problemas?

### Erro: "sudo: a password is required"

**Solução**: Digite sua senha do Ubuntu/WSL quando solicitado.

---

### Erro: "python3: command not found"

**Solução**: Instalar Python 3:
```bash
sudo apt update
sudo apt install python3
```

---

### Erro: Permission denied ao executar scripts

**Solução**: Dar permissão de execução:
```bash
chmod +x scripts/*.sh
chmod +x activate_venv.sh
```

---

### Venv não ativa (sem erro)

**Causa**: Você executou `./venv/bin/activate` ao invés de `source`

**Solução**: SEMPRE use `source`:
```bash
source venv/bin/activate
```

---

## 📚 Documentação Completa

Para mais detalhes, consulte:
- **VENV_GUIDE.md** - Guia completo de venv
- **QUICK_START_SCRIPTS.md** - Scripts de execução
- **WEBAPPS_GUIDE.md** - Comparação webapps

---

**Criado para**: AMLDO v0.3.0
**Sistema**: Ubuntu/WSL Bash
**Última atualização**: 2025-11-16

⚡ **Comando único para setup completo** (após instalar python3-venv):
```bash
cd /mnt/d/PYTHON/AMLDO && rm -rf venv && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -e ".[api,adk,streamlit]"
```
