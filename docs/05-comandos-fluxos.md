# Comandos e Fluxos do Sistema AMLDO

## 📋 Sumário

- [Comandos Principais](#comandos-principais)
- [Fluxos de Execução](#fluxos-de-execução)
- [Notebooks de Processamento](#notebooks-de-processamento)
- [Operações de Manutenção](#operações-de-manutenção)
- [Scripts Úteis](#scripts-úteis)

## Comandos Principais

### Ambiente Virtual

#### Ativar Ambiente

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Verificar ativação:**
```bash
which python  # Deve mostrar caminho do venv
python --version  # Deve ser 3.11.x
```

#### Desativar Ambiente

```bash
deactivate
```

### Instalação e Atualização

#### Instalar Dependências

```bash
pip install -r requirements.txt
```

#### Atualizar Dependências

```bash
# Atualizar todas
pip install --upgrade -r requirements.txt

# Atualizar apenas uma biblioteca
pip install --upgrade langchain

# Ver pacotes desatualizados
pip list --outdated
```

#### Adicionar Nova Dependência

```bash
# Instalar
pip install nome-do-pacote

# Salvar em requirements.txt
pip freeze > requirements.txt
```

⚠️ **Melhor prática:** Adicione apenas a dependência principal ao `requirements.txt`, não todas as sub-dependências

#### Gerar requirements.txt Limpo

```bash
# Usando pipreqs (instale primeiro: pip install pipreqs)
pipreqs . --force
```

### Interface Web

#### Iniciar Servidor ADK

```bash
adk web
```

**Saída esperada:**
```
Starting Google Agent Development Kit Web Interface...
Detecting agents...
  ✓ Found agent: rag_v1
  ✓ Found agent: rag_v2
Server running at http://localhost:8080
Press Ctrl+C to stop
```

**Opções:**
```bash
# Especificar porta
adk web --port 8000

# Especificar host
adk web --host 0.0.0.0  # Acessível de outras máquinas na rede
```

#### Parar Servidor

```bash
Ctrl + C
```

### Jupyter Notebooks

#### Iniciar Jupyter Lab

```bash
jupyter lab
```

Abre browser em `http://localhost:8888`

#### Iniciar Jupyter Notebook (Clássico)

```bash
jupyter notebook
```

#### Executar Notebook via Linha de Comando

```bash
# Executar notebook inteiro
jupyter nbconvert --execute --to notebook --inplace get_v1_data.ipynb

# Ou usando papermill (instale: pip install papermill)
papermill get_v1_data.ipynb output.ipynb
```

#### Converter Notebook para Python

```bash
jupyter nbconvert --to python get_v1_data.ipynb
# Gera: get_v1_data.py
```

## Fluxos de Execução

### Fluxo 1: Primeiro Uso (Projeto Existente)

Sistema já tem dados processados e índice FAISS construído.

```
1. Clonar repositório
   ↓
2. Criar venv e instalar dependências
   ↓
3. Configurar .env (GOOGLE_API_KEY)
   ↓
4. adk web
   ↓
5. Testar consultas
```

**Comandos:**
```bash
git clone <repo>
cd AMLDO
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key" > .env
adk web
```

### Fluxo 2: Adicionar Novo Documento

Você tem um novo PDF de lei e quer indexá-lo.

```
1. Colocar PDF em data/raw/
   ↓
2. Executar get_v1_data.ipynb
   ├─> Extrair texto
   ├─> Dividir hierarquicamente
   ├─> Salvar em split_docs/
   └─> Atualizar CSVs em processed/
   ↓
3. Executar get_vectorial_bank_v1.ipynb
   ├─> Carregar split_docs/
   ├─> Gerar embeddings
   ├─> Construir/atualizar índice FAISS
   └─> Persistir em vector_db/
   ↓
4. Reiniciar adk web
   ↓
5. Testar consultas sobre novo documento
```

**Comandos:**
```bash
# 1. Adicionar PDF
cp ~/Downloads/L99999.pdf data/raw/

# 2. Processar (abrir Jupyter e executar notebook)
jupyter lab
# Executar todas células de get_v1_data.ipynb
# Executar todas células de get_vectorial_bank_v1.ipynb

# 3. Reiniciar servidor
adk web
```

### Fluxo 3: Modificar Código RAG

Alterar lógica do pipeline (ex: mudar prompt, k, etc.)

```
1. Editar código (rag_v1/tools.py ou rag_v2/tools.py)
   ↓
2. Salvar arquivo
   ↓
3. Reiniciar adk web (Ctrl+C → adk web)
   ↓
4. Testar mudanças
   ↓
5. (Opcional) Commitar se melhorou
```

**Exemplo:**
```bash
# Abrir editor
code rag_v1/tools.py

# Fazer mudanças...
# Salvar

# Terminal
# Ctrl+C (parar servidor)
adk web  # Reiniciar

# Testar no browser
```

### Fluxo 4: Experimentar com Parâmetros

Testar diferentes configurações sem mudar código permanentemente.

```
1. Criar script de teste (test_params.py)
   ↓
2. Importar funções do RAG
   ↓
3. Testar diferentes parâmetros
   ↓
4. Comparar resultados
   ↓
5. Aplicar melhor configuração no código
```

**Exemplo (`test_params.py`):**
```python
from rag_v1.tools import _rag_answer

query = "Qual o limite de dispensa?"

print("=" * 80)
print("Testando k=5")
print("=" * 80)
resposta_5 = _rag_answer(query, k=5)
print(resposta_5)

print("\n" + "=" * 80)
print("Testando k=12")
print("=" * 80)
resposta_12 = _rag_answer(query, k=12)
print(resposta_12)

print("\n" + "=" * 80)
print("Testando k=20")
print("=" * 80)
resposta_20 = _rag_answer(query, k=20)
print(resposta_20)
```

**Executar:**
```bash
python test_params.py > results.txt
```

### Fluxo 5: Deploy em Servidor

Colocar sistema em produção (servidor Linux).

```
1. Configurar servidor (Ubuntu/Debian)
   ↓
2. Clonar repositório
   ↓
3. Instalar Python 3.11
   ↓
4. Configurar venv e dependências
   ↓
5. Configurar .env com variáveis
   ↓
6. Configurar systemd para rodar adk web
   ↓
7. Configurar nginx como proxy reverso
   ↓
8. Testar acesso via domínio
```

**Exemplo de service (systemd):**

`/etc/systemd/system/amldo.service`:
```ini
[Unit]
Description=AMLDO RAG Service
After=network.target

[Service]
Type=simple
User=amldo
WorkingDirectory=/opt/amldo
Environment="PATH=/opt/amldo/venv/bin"
ExecStart=/opt/amldo/venv/bin/adk web --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```

**Comandos:**
```bash
# Ativar e iniciar service
sudo systemctl enable amldo
sudo systemctl start amldo

# Ver status
sudo systemctl status amldo

# Ver logs
sudo journalctl -u amldo -f
```

## Notebooks de Processamento

### 1. `get_v1_data.ipynb`

**Objetivo:** Extrair e estruturar documentos PDF

**Entrada:**
- PDFs em `data/raw/`

**Saída:**
- Arquivos TXT em `data/split_docs/{Lei}/...`
- CSV `data/processed/v1_artigos_0.csv`
- CSV `data/processed/v1_processed_articles.csv`

**Estrutura do Notebook:**

1. **Cell 1-3: Imports e Setup**
   - PyMuPDF, Pandas, regex, os
   - Definição de constantes

2. **Cell 4-6: Extração de Texto**
   - `extract_text_from_pdf(pdf_path)`
   - Itera sobre páginas
   - Concatena texto

3. **Cell 7-10: Identificação de Estrutura**
   - Regex para detectar Títulos: `r"TÍTULO [IVX]+"`
   - Regex para Capítulos: `r"CAPÍTULO [IVX]+"`
   - Regex para Artigos: `r"Art\. \d+"`

4. **Cell 11-15: Divisão Hierárquica**
   - `split_by_structure(text, lei_id)`
   - Cria diretórios Lei/Título/Capítulo/Artigos
   - Salva arquivos TXT

5. **Cell 16-18: Geração de CSVs**
   - Extrai artigos_0 (intros)
   - Compila todos artigos
   - Salva CSVs

6. **Cell 19: Estatísticas**
   - Número de leis processadas
   - Número de artigos
   - Tamanho total

**Tempo de Execução:** ~5-10 minutos (4 PDFs)

**Como Executar:**
```bash
jupyter lab
# Abrir get_v1_data.ipynb
# Run → Run All Cells
```

### 2. `get_vectorial_bank_v1.ipynb`

**Objetivo:** Criar índice vetorial FAISS

**Entrada:**
- Arquivos TXT em `data/split_docs/`

**Saída:**
- Índice FAISS em `data/vector_db/v1_faiss_vector_db/`

**Estrutura do Notebook:**

1. **Cell 1-3: Imports e Setup**
   - LangChain, FAISS, HuggingFace
   - Definição de parâmetros (chunk_size, overlap, k)

2. **Cell 4-6: Carregamento de Documentos**
   - `load_documents_from_split_docs()`
   - Itera sobre diretórios
   - Anexa metadados (lei, titulo, capitulo, artigo)

3. **Cell 7-9: Text Splitting**
   - `RecursiveCharacterTextSplitter`
   - chunk_size=500, chunk_overlap=50
   - Adiciona `chunk_idx` aos metadados

4. **Cell 10-12: Geração de Embeddings**
   - `HuggingFaceEmbeddings`
   - Modelo: paraphrase-multilingual-MiniLM-L12-v2
   - Dimensões: 384

5. **Cell 13-15: Construção do Índice FAISS**
   - `FAISS.from_documents(chunks, embeddings)`
   - Salva em disco: `save_local()`

6. **Cell 16: Teste do Índice**
   - Query de teste
   - Busca de similaridade
   - Exibe top-5 resultados

**Tempo de Execução:** ~10-20 minutos (embeddings demorados)

**Como Executar:**
```bash
jupyter lab
# Abrir get_vectorial_bank_v1.ipynb
# Run → Run All Cells
```

**⚠️ ATENÇÃO:**
- Primeira execução baixa modelo de embeddings (~500 MB)
- Pode consumir muita memória (>4 GB RAM)

### 3. `order_rag_study.ipynb`

**Objetivo:** Análises e experimentações

**Conteúdo:**
- Testes de busca com diferentes parâmetros
- Comparação similarity vs MMR
- Análise de qualidade de respostas
- Visualizações (distribuição de similaridade, etc.)

**Uso:** Exploratório, não é necessário executar

## Operações de Manutenção

### Limpar Cache

```bash
# Cache do pip
pip cache purge

# Cache do HuggingFace (modelos baixados)
rm -rf ~/.cache/huggingface/

# Cache do Jupyter
jupyter notebook clean

# __pycache__ (Python)
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Backup de Dados

```bash
# Backup completo (sem venv)
tar -czf amldo_backup_$(date +%Y%m%d).tar.gz \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    .

# Backup apenas dos dados
tar -czf amldo_data_$(date +%Y%m%d).tar.gz data/

# Backup apenas do código
tar -czf amldo_code_$(date +%Y%m%d).tar.gz rag_v1/ rag_v2/ *.py *.ipynb
```

### Restaurar Dados

```bash
# Extrair backup
tar -xzf amldo_backup_20250130.tar.gz

# Recriar venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar .env
nano .env  # Adicionar GOOGLE_API_KEY
```

### Reindexar Tudo (Do Zero)

```bash
# 1. Limpar dados existentes
rm -rf data/split_docs/*
rm -rf data/processed/*
rm -rf data/vector_db/*

# 2. Reprocessar
jupyter nbconvert --execute --to notebook --inplace get_v1_data.ipynb
jupyter nbconvert --execute --to notebook --inplace get_vectorial_bank_v1.ipynb

# 3. Verificar
ls -lh data/vector_db/v1_faiss_vector_db/
```

### Atualizar Apenas um Documento

```bash
# Exemplo: Atualizar Lei 14.133

# 1. Remover documento antigo
rm -rf data/split_docs/L14133/
rm -rf data/vector_db/v1_faiss_vector_db/  # FAISS não suporta update, recriar

# 2. Substituir PDF
cp ~/Downloads/L14133_atualizada.pdf data/raw/L14133.pdf

# 3. Reprocessar (notebooks)
# ... executar get_v1_data.ipynb e get_vectorial_bank_v1.ipynb

# 4. Reiniciar servidor
adk web
```

## Scripts Úteis

### 1. `verify_installation.py`

```python
#!/usr/bin/env python3
"""Verifica instalação do AMLDO"""

import sys
import os

def check_python_version():
    version = sys.version_info
    if version.major == 3 and version.minor == 11:
        print("✅ Python 3.11")
    else:
        print(f"❌ Python {version.major}.{version.minor} (requer 3.11)")

def check_imports():
    imports = [
        "langchain",
        "faiss",
        "sentence_transformers",
        "google.adk",
        "pandas",
        "pymupdf"
    ]

    for imp in imports:
        try:
            __import__(imp)
            print(f"✅ {imp}")
        except ImportError:
            print(f"❌ {imp}")

def check_data():
    paths = [
        "data/vector_db/v1_faiss_vector_db",
        "data/processed/v1_artigos_0.csv",
        "data/split_docs"
    ]

    for path in paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"⚠️  {path} (não encontrado)")

def check_env():
    from dotenv import load_dotenv
    load_dotenv()

    if os.getenv("GOOGLE_API_KEY"):
        print("✅ GOOGLE_API_KEY configurada")
    else:
        print("❌ GOOGLE_API_KEY não encontrada")

if __name__ == "__main__":
    print("=" * 60)
    print("Verificação de Instalação AMLDO")
    print("=" * 60)

    print("\n[Python Version]")
    check_python_version()

    print("\n[Dependências]")
    check_imports()

    print("\n[Dados]")
    check_data()

    print("\n[Configuração]")
    check_env()

    print("\n" + "=" * 60)
```

**Uso:**
```bash
python verify_installation.py
```

### 2. `quick_test.py`

```python
#!/usr/bin/env python3
"""Teste rápido do RAG"""

import sys
sys.path.insert(0, '.')

from rag_v1.tools import consultar_base_rag
import time

queries = [
    "Qual é o limite de dispensa para obras?",
    "O que diz a LGPD sobre consentimento?",
    "Como funciona o pregão eletrônico?",
]

print("=" * 80)
print("TESTE RÁPIDO DO RAG")
print("=" * 80)

for i, query in enumerate(queries, 1):
    print(f"\n[{i}/{len(queries)}] {query}")
    print("-" * 80)

    start = time.time()
    resposta = consultar_base_rag(query)
    elapsed = time.time() - start

    print(resposta)
    print(f"\n⏱️  Tempo: {elapsed:.2f}s")
    print("=" * 80)
```

**Uso:**
```bash
python quick_test.py
```

### 3. `benchmark.py`

```python
#!/usr/bin/env python3
"""Benchmark de performance"""

import time
import statistics
from rag_v1.tools import consultar_base_rag

queries = [
    "Qual o limite de dispensa?",
    "O que é LGPD?",
    "Como funciona pregão?",
    # ... mais queries
]

latencies = []

print(f"Executando {len(queries)} consultas...")

for query in queries:
    start = time.time()
    consultar_base_rag(query)
    elapsed = time.time() - start
    latencies.append(elapsed)
    print(f"  ✓ {elapsed:.2f}s")

print("\n" + "=" * 60)
print("RESULTADOS")
print("=" * 60)
print(f"Média:    {statistics.mean(latencies):.2f}s")
print(f"Mediana:  {statistics.median(latencies):.2f}s")
print(f"Min:      {min(latencies):.2f}s")
print(f"Max:      {max(latencies):.2f}s")
print(f"Desvio:   {statistics.stdev(latencies):.2f}s")
```

**Uso:**
```bash
python benchmark.py
```

---

**Próximo:** [Estado Atual do Sistema](06-estado-atual.md)
