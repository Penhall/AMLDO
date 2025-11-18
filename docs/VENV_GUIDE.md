# 🐍 Guia Virtual Environment - AMLDO

> **Passo-a-passo** para criar e ativar ambiente virtual no Bash

---

## ⚡ Método Rápido (RECOMENDADO)

### Opção 1: Usar script automatizado

```bash
# Ir para o diretório do projeto
cd /mnt/d/PYTHON/AMLDO

# Ativar venv (usando source)
source activate_venv.sh
```

✅ **Pronto!** O ambiente virtual está ativado.

**Indicador**: Você verá `(venv)` antes do prompt:
```
(venv) petto@DESKTOP:/mnt/d/PYTHON/AMLDO$
```

---

## 📝 Método Manual (Passo-a-Passo)

### 1️⃣ Verificar se Python está instalado

```bash
python3 --version
```

**Saída esperada**: `Python 3.11.x` ou `Python 3.12.x`

### ⚠️ IMPORTANTE: Instalar python3-venv

**Se você receber erro "ensurepip is not available"**, precisa instalar o módulo venv:

```bash
# Ubuntu/Debian/WSL
sudo apt update
sudo apt install python3.12-venv

# Ou para Python 3.11
sudo apt install python3.11-venv

# Ou usar o Python disponível
python3 --version  # Verificar versão
```

**Este passo é OBRIGATÓRIO** antes de criar o venv!

---

### 2️⃣ Ir para o diretório do projeto

```bash
cd /mnt/d/PYTHON/AMLDO
```

**Verificar**:
```bash
pwd
# Deve mostrar: /mnt/d/PYTHON/AMLDO
```

---

### 3️⃣ Remover venv corrompido (se existir)

**IMPORTANTE**: Se você já tem um venv que não funciona, remova-o primeiro:

```bash
# Verificar se existe venv corrompido
ls venv/bin/activate

# Se o comando acima der erro "No such file", o venv está corrompido
# Remover venv antigo
rm -rf venv
```

---

### 4️⃣ Criar Virtual Environment

**Agora sim, criar o venv novo e funcional**:

```bash
python3 -m venv venv
```

**Aguardar**: Leva ~30-60 segundos (depende do sistema)

**Verificar criação com sucesso**:
```bash
ls venv/bin/activate
# Deve mostrar: venv/bin/activate

ls -la venv/
# Deve mostrar: bin/, lib/, include/, pyvenv.cfg
```

**✅ Sucesso**: Se `venv/bin/activate` existe, o venv foi criado corretamente!

---

### 5️⃣ Ativar Virtual Environment

**IMPORTANTE**: Use `source` (não só executar o script)

```bash
source venv/bin/activate
```

**OU** (alternativa):
```bash
. venv/bin/activate
```

**✅ Sucesso**: Você verá `(venv)` no prompt:
```
(venv) petto@DESKTOP:/mnt/d/PYTHON/AMLDO$
```

**Verificar**:
```bash
which python
# Deve mostrar: /mnt/d/PYTHON/AMLDO/venv/bin/python

python --version
# Deve mostrar a versão do Python
```

---

### 6️⃣ Instalar Dependências (primeira vez)

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar projeto em modo editável
pip install -e ".[api,adk,streamlit]"

# OU instalar apenas API
pip install -e ".[api]"
```

**Aguardar**: Pode demorar 2-5 minutos

**Verificar instalação**:
```bash
pip list | grep amldo
# Deve mostrar: amldo 0.3.0

which amldo-api
# Deve mostrar: /mnt/d/PYTHON/AMLDO/venv/bin/amldo-api
```

---

### 7️⃣ Desativar Virtual Environment

Quando terminar de trabalhar:

```bash
deactivate
```

**Resultado**: O `(venv)` desaparece do prompt

---

## 🔧 Troubleshooting

### Problema 1: "ensurepip is not available" ⚠️ COMUM!

**Erro completo**:
```
The virtual environment was not created successfully because ensurepip is not
available. On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.12-venv
```

**Causa**: O módulo `python3-venv` não está instalado no sistema

**Solução**: Instalar python3-venv
```bash
# Para Python 3.12 (verifique sua versão com python3 --version)
sudo apt update
sudo apt install python3.12-venv

# Para Python 3.11
sudo apt install python3.11-venv

# Depois de instalar, remover venv corrompido e recriar
cd /mnt/d/PYTHON/AMLDO
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

**Verificar sucesso**:
```bash
ls venv/bin/activate
# Se existir → sucesso!
```

---

### Problema 2: "source: command not found"

**Causa**: Você está usando `sh` ao invés de `bash`

**Solução**:
```bash
# Mudar para bash
bash

# Depois ativar
source venv/bin/activate
```

---

### Problema 3: "venv/bin/activate: No such file or directory"

**Causa**: Virtual environment não existe ou está corrompido

**Solução**: Recriar venv
```bash
# Remover venv antigo
rm -rf venv

# Criar novo
python3 -m venv venv

# Ativar
source venv/bin/activate

# Reinstalar
pip install -e ".[api]"
```

---

### Problema 4: Virtual environment não ativa (sem erro)

**Causa**: Você executou `./venv/bin/activate` ao invés de `source`

**Solução**: Use `source` ou `.`
```bash
# ✅ CORRETO
source venv/bin/activate

# ✅ CORRETO (alternativa)
. venv/bin/activate

# ❌ ERRADO (não funciona)
./venv/bin/activate
```

---

### Problema 5: "python3: command not found"

**Causa**: Python não instalado

**Solução**:
```bash
# Verificar se python existe (sem o 3)
python --version

# Se sim, usar:
python -m venv venv

# Se não, instalar Python
sudo apt update
sudo apt install python3
```

---

### Problema 6: Permissão negada

**Causa**: WSL ou permissões do Windows

**Solução**:
```bash
# Dar permissões
chmod +x venv/bin/activate

# Tentar ativar novamente
source venv/bin/activate
```

---

## 📋 Comandos Úteis

### Verificar se venv está ativo

```bash
# Método 1: Ver prompt
# Se tiver (venv) → está ativo

# Método 2: Verificar caminho do Python
which python
# Ativo: /mnt/d/PYTHON/AMLDO/venv/bin/python
# Inativo: /usr/bin/python

# Método 3: Verificar variável de ambiente
echo $VIRTUAL_ENV
# Ativo: /mnt/d/PYTHON/AMLDO/venv
# Inativo: (vazio)
```

### Listar pacotes instalados

```bash
pip list
```

### Verificar se AMLDO está instalado

```bash
pip show amldo
```

### Reinstalar AMLDO

```bash
pip install -e ".[api]" --force-reinstall
```

---

## 🎯 Workflow Diário

### Ao começar a trabalhar:

```bash
cd /mnt/d/PYTHON/AMLDO
source venv/bin/activate
# Ou: source activate_venv.sh
```

### Trabalhar normalmente:

```bash
# Executar API
amldo-api

# Executar testes
pytest tests/

# Executar scripts
./scripts/run_webapp_new.sh
```

### Ao terminar:

```bash
deactivate
```

---

## 🚀 Scripts Prontos

Criamos scripts que **ativam automaticamente** o venv:

### Script 1: Ativar venv
```bash
source activate_venv.sh
```

### Script 2: Executar webapp (ativa automaticamente)
```bash
./scripts/run_webapp_new.sh  # Ativa venv automaticamente
```

### Script 3: Executar testes (ativa automaticamente)
```bash
./scripts/run_tests.sh unit  # Ativa venv automaticamente
```

---

## 💡 Dicas

### 1. Adicionar ao ~/.bashrc (opcional)

Para ativar automaticamente ao entrar no diretório:

```bash
# Editar ~/.bashrc
nano ~/.bashrc

# Adicionar no final:
amldo() {
    cd /mnt/d/PYTHON/AMLDO
    source venv/bin/activate
}

# Salvar e recarregar
source ~/.bashrc

# Agora você pode usar:
amldo  # Vai para AMLDO e ativa venv
```

### 2. Verificar sempre antes de executar

```bash
# Sempre verificar se venv está ativo
which python

# Se mostrar /usr/bin/python → NÃO está ativo
# Se mostrar .../venv/bin/python → ESTÁ ativo
```

### 3. Usar sempre `source`

```bash
# ✅ SEMPRE use source
source venv/bin/activate

# ❌ NUNCA use ./
./venv/bin/activate  # Não funciona!
```

---

## 🆘 Ajuda Rápida

### Não consegue ativar?

```bash
# Copie e cole EXATAMENTE estes comandos:
cd /mnt/d/PYTHON/AMLDO
bash
source venv/bin/activate
which python
```

**Se mostrar** `.../venv/bin/python` → ✅ Funcionou!

### Venv corrompido?

```bash
# Recriar do zero (copia e cola tudo):
cd /mnt/d/PYTHON/AMLDO
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e ".[api]"
```

**Aguarde** ~3-5 minutos para concluir.

---

## ✅ Checklist

Antes de executar qualquer comando do AMLDO:

- [ ] Estou no diretório correto (`/mnt/d/PYTHON/AMLDO`)
- [ ] Venv está ativado (vejo `(venv)` no prompt)
- [ ] `which python` mostra `.../venv/bin/python`
- [ ] `.env` está configurado
- [ ] Dependências instaladas (`pip list | grep amldo`)

---

## 📞 Ainda com problemas?

Se nada funcionar, me mande a saída destes comandos:

```bash
pwd
python3 --version
ls -la venv/ | head -5
which python
echo $VIRTUAL_ENV
cat venv/pyvenv.cfg
```

---

**Criado para**: AMLDO v0.3.0
**Sistema**: Ubuntu/WSL Bash
**Última atualização**: 2025-11-16

🐍 **Boa sorte!**
