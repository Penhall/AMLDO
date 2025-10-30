# Guia do Desenvolvedor AMLDO

## 📋 Sumário

- [Setup do Ambiente](#setup-do-ambiente)
- [Primeiros Passos](#primeiros-passos)
- [Estrutura do Código](#estrutura-do-código)
- [Desenvolvimento Local](#desenvolvimento-local)
- [Debugging e Testes](#debugging-e-testes)
- [Boas Práticas](#boas-práticas)
- [Troubleshooting](#troubleshooting)

## Setup do Ambiente

### Pré-requisitos

- **Python 3.11** (obrigatório)
- **Git** para controle de versão
- **~2 GB de espaço** em disco (modelos + dados)
- **API Key do Google** (Gemini)

### Instalação Passo a Passo

#### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd AMLDO
```

#### 2. Criar Ambiente Virtual

**Linux/macOS:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python3.11 -m venv venv
venv\Scripts\activate
```

**Verificar ativação:**
```bash
which python  # Linux/macOS
where python  # Windows
# Deve apontar para venv/bin/python ou venv\Scripts\python.exe
```

#### 3. Atualizar pip

```bash
pip install --upgrade pip
```

#### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Tempo estimado:** 5-10 minutos (download de ~1.5 GB)

**Principais dependências instaladas:**
- LangChain e LangChain Community
- FAISS CPU
- Sentence Transformers (com PyTorch)
- Google ADK e Gemini SDK
- Pandas, PyMuPDF

#### 5. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
GOOGLE_API_KEY=your_google_api_key_here
```

**Como obter API Key:**
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma API Key
3. Copie e cole no `.env`

**⚠️ IMPORTANTE:** Nunca commite o arquivo `.env` (já está no `.gitignore`)

#### 6. (Opcional) Registrar Kernel Jupyter

Se for usar os notebooks:

```bash
python -m ipykernel install --user --name=venv --display-name "amldo_kernel"
```

**Verificação:**
- Abra Jupyter Lab/Notebook
- Vá em Kernel → Change Kernel
- Deve aparecer "amldo_kernel"

### Verificação da Instalação

Execute o seguinte script de teste:

```python
# test_setup.py
import sys
print(f"Python: {sys.version}")

# Test imports
try:
    import langchain
    print("✅ LangChain instalado")
except ImportError:
    print("❌ LangChain não encontrado")

try:
    import faiss
    print("✅ FAISS instalado")
except ImportError:
    print("❌ FAISS não encontrado")

try:
    from sentence_transformers import SentenceTransformer
    print("✅ Sentence Transformers instalado")
except ImportError:
    print("❌ Sentence Transformers não encontrado")

try:
    import google.adk
    print("✅ Google ADK instalado")
except ImportError:
    print("❌ Google ADK não encontrado")

# Test environment
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv("GOOGLE_API_KEY"):
    print("✅ GOOGLE_API_KEY configurada")
else:
    print("❌ GOOGLE_API_KEY não encontrada no .env")

# Test data
import os
if os.path.exists("data/vector_db/v1_faiss_vector_db"):
    print("✅ Banco vetorial encontrado")
else:
    print("⚠️ Banco vetorial não encontrado (rode os notebooks)")

print("\n🎉 Setup completo!")
```

Execute:
```bash
python test_setup.py
```

## Primeiros Passos

### 1. Rodar a Interface Web

```bash
# Com venv ativado
adk web
```

**Saída esperada:**
```
Starting Google Agent Development Kit Web Interface...
Server running at http://localhost:8080
```

**Navegue para:** http://localhost:8080

**Selecione um agente:**
- `rag_v1` (básico)
- `rag_v2` (aprimorado)

**Teste uma consulta:**
```
Qual é o limite de valor para dispensa de licitação em obras?
```

### 2. Explorar o Código

**Estrutura mínima para entender:**

```
AMLDO/
├── rag_v1/
│   ├── agent.py          ← COMECE AQUI (definição do agente v1)
│   └── tools.py          ← Pipeline RAG básico
│
├── rag_v2/
│   ├── agent.py          ← Agente v2 (similar ao v1)
│   └── tools.py          ← Pipeline RAG aprimorado (mais complexo)
│
└── data/
    ├── vector_db/        ← Banco vetorial (pré-construído)
    └── processed/        ← CSVs (usados pelo v2)
```

**Leitura sugerida (ordem):**
1. `rag_v1/agent.py` (30 linhas, simples)
2. `rag_v1/tools.py` (80 linhas, pipeline básico)
3. `rag_v2/tools.py` (160 linhas, pipeline avançado)

### 3. Testar Modificações

**Exemplo: Mudar número de documentos recuperados**

Edite `rag_v1/tools.py`:

```python
# Antes
K = 12

# Depois
K = 8  # Recupera menos documentos (mais rápido, menos contexto)
```

**Reinicie o servidor:**
```bash
# Ctrl+C para parar
adk web  # Rodar novamente
```

**Teste e compare** as respostas com k=12 vs k=8

## Estrutura do Código

### Arquitetura de Módulos

```
rag_v1/
├── __init__.py           # Expõe 'agent'
├── agent.py              # Definição do Agent (ADK)
│   ├── root_agent        # Instância principal
│   ├── name              # Nome do agente
│   ├── model             # LLM usado (gemini-2.5-flash)
│   ├── description       # Descrição curta
│   ├── instruction       # Prompt de sistema
│   └── tools             # Lista de ferramentas [consultar_base_rag]
│
└── tools.py              # Implementação da ferramenta RAG
    ├── modelo_embedding  # HuggingFace Embeddings
    ├── vector_db         # FAISS Index
    ├── llm               # Gemini Flash
    ├── _get_retriever()  # Cria retriever FAISS
    ├── _rag_answer()     # Pipeline RAG
    └── consultar_base_rag()  # Função exposta ao agente
```

### Pontos de Extensão

#### 1. Adicionar Nova Ferramenta ao Agente

**Exemplo: Calculadora de prazos**

```python
# rag_v1/tools.py

def calcular_prazo_licitacao(tipo_licitacao: str, valor: float) -> str:
    """
    Calcula prazo mínimo para publicação de edital.

    Args:
        tipo_licitacao: "pregao", "concorrencia", etc.
        valor: Valor estimado da contratação

    Returns:
        Prazo em dias
    """
    if tipo_licitacao == "pregao":
        return "8 dias úteis (art. 54, Lei 14.133)"
    elif tipo_licitacao == "concorrencia":
        if valor > 1000000:
            return "30 dias (art. 54, §2º, Lei 14.133)"
        return "15 dias (art. 54, Lei 14.133)"
    return "Consulte a legislação para esse tipo"

# rag_v1/agent.py
from .tools import consultar_base_rag, calcular_prazo_licitacao

root_agent = Agent(
    name="rag_v1",
    model="gemini-2.5-flash",
    tools=[consultar_base_rag, calcular_prazo_licitacao],  # ← Adicionar
    # ...
)
```

#### 2. Mudar Modelo de LLM

```python
# rag_v1/tools.py

# Antes
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

# Depois: Usar GPT-4 (requer OPENAI_API_KEY no .env)
llm = init_chat_model("gpt-4", model_provider="openai")

# Ou: Usar modelo local (Ollama)
llm = init_chat_model("llama3", model_provider="ollama")
```

#### 3. Customizar Prompt

```python
# rag_v1/tools.py

# Antes
prompt = ChatPromptTemplate.from_template(
    "Use APENAS o contexto para responder.\n\n"
    "Contexto:\n{context}\n\n"
    "Pergunta:\n{question}"
)

# Depois: Prompt mais específico
prompt = ChatPromptTemplate.from_template(
    "Você é um assistente jurídico especializado em licitações.\n\n"
    "INSTRUÇÕES:\n"
    "1. Responda APENAS com base no contexto fornecido\n"
    "2. Cite o artigo e lei de onde veio a informação\n"
    "3. Se não souber, diga 'Não encontrei essa informação'\n\n"
    "CONTEXTO:\n{context}\n\n"
    "PERGUNTA:\n{question}\n\n"
    "RESPOSTA:"
)
```

#### 4. Adicionar Filtros Personalizados (v2)

```python
# rag_v2/tools.py

# Exemplo: Buscar apenas na Lei 14.133
retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 12,
        "filter": {
            "lei": "L14133",  # ← Filtro por lei
            "artigo": {"$nin": ['artigo_0.txt']}
        }
    }
)
```

## Desenvolvimento Local

### Workflow Típico

```
1. Ativar venv
   ↓
2. Fazer mudanças no código
   ↓
3. Testar localmente (adk web)
   ↓
4. Debuggar (se necessário)
   ↓
5. Commitar mudanças
```

### Hot Reload

**Problema:** ADK web não recarrega código automaticamente

**Soluções:**

**Opção 1: Reiniciar manualmente**
```bash
# Terminal 1
adk web
# Ctrl+C para parar
# Fazer mudanças
adk web  # Reiniciar
```

**Opção 2: Usar watchdog (avançado)**
```bash
pip install watchdog

# watch.py
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = subprocess.Popen(['adk', 'web'])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Detected change in {event.src_path}, restarting...")
            self.process.terminate()
            self.process = subprocess.Popen(['adk', 'web'])

observer = Observer()
observer.schedule(RestartHandler(), path='rag_v1', recursive=True)
observer.schedule(RestartHandler(), path='rag_v2', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

### Testar Sem Interface Web

```python
# test_rag.py
from rag_v1.tools import consultar_base_rag

query = "Qual o limite de dispensa para obras?"
resposta = consultar_base_rag(query)
print(resposta)
```

Execute:
```bash
python test_rag.py
```

**Vantagem:** Mais rápido para iterar, não precisa da UI

## Debugging e Testes

### Logs e Debug

#### 1. Ativar Logs do LangChain

```python
# rag_v1/tools.py
import langchain
langchain.debug = True  # ← Adicionar no início

# Agora todas as chains mostrarão logs detalhados
```

**Exemplo de saída:**
```
[chain/start] [1:chain:RunnableSequence] Entering Chain run...
[retriever/start] [1:retriever:VectorStoreRetriever] Entering Retriever run...
[retriever/end] [1:retriever:VectorStoreRetriever] Retrieved 12 documents
[llm/start] [1:llm:ChatGoogleGenerativeAI] Entering LLM run...
[llm/end] [1:llm:ChatGoogleGenerativeAI] Response: "Segundo o Art. 75..."
```

#### 2. Inspecionar Documentos Recuperados

```python
# rag_v1/tools.py

def _rag_answer(question: str, search_type: str = "mmr", k: int = 12) -> str:
    retriever = _get_retriever(search_type=search_type, k=k)

    # ← DEBUG: Imprimir documentos recuperados
    docs = retriever.get_relevant_documents(question)
    print(f"\n{'='*80}")
    print(f"QUERY: {question}")
    print(f"{'='*80}")
    for i, doc in enumerate(docs, 1):
        print(f"\n[Doc {i}] {doc.metadata}")
        print(f"{doc.page_content[:200]}...")
    print(f"{'='*80}\n")

    # ...resto do código
```

#### 3. Medir Latência

```python
# rag_v1/tools.py
import time

def consultar_base_rag(pergunta: str) -> str:
    start = time.time()

    resposta = _rag_answer(pergunta, search_type="mmr", k=12)

    elapsed = time.time() - start
    print(f"⏱️ Latência: {elapsed:.2f}s")

    return resposta
```

### Testes Unitários (Exemplo)

Crie `tests/test_rag_v1.py`:

```python
import pytest
from rag_v1.tools import consultar_base_rag

def test_consulta_basica():
    """Testa consulta simples"""
    resposta = consultar_base_rag("O que é licitação?")
    assert len(resposta) > 0
    assert "licitação" in resposta.lower()

def test_consulta_limite_dispensa():
    """Testa consulta sobre limites"""
    resposta = consultar_base_rag("Qual o limite de dispensa para obras?")
    assert "50.000" in resposta or "cinquenta mil" in resposta.lower()
    assert "art" in resposta.lower()  # Deve citar artigo

def test_consulta_inexistente():
    """Testa pergunta sem resposta na base"""
    resposta = consultar_base_rag("Qual a capital da França?")
    # Deve indicar que não encontrou na base
    assert any(palavra in resposta.lower() for palavra in
               ["não encontr", "base", "contexto", "não há"])

@pytest.mark.parametrize("query,expected_law", [
    ("LGPD", "13.709"),
    ("pregão eletrônico", "10.024"),
    ("microempresa", "123"),
])
def test_identificacao_lei(query, expected_law):
    """Testa se recupera da lei correta"""
    resposta = consultar_base_rag(query)
    assert expected_law in resposta
```

**Rodar testes:**
```bash
pip install pytest
pytest tests/
```

### Debugging com VSCode

**Configuração `.vscode/launch.json`:**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Test RAG",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/test_rag.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "ADK Web",
            "type": "python",
            "request": "launch",
            "module": "google.adk.web",
            "console": "integratedTerminal"
        }
    ]
}
```

**Uso:**
1. Coloque breakpoints no código
2. F5 para iniciar debug
3. Inspecione variáveis, stack, etc.

## Boas Práticas

### 1. Controle de Versão

**Commits semânticos:**

```bash
# Boa prática
git commit -m "feat: adiciona filtro por lei no retriever v2"
git commit -m "fix: corrige ordenação de chunks no pós-processamento"
git commit -m "docs: atualiza guia com novos exemplos"
git commit -m "refactor: simplifica lógica de injeção de artigo_0"

# Evite
git commit -m "changes"
git commit -m "fix bug"
```

**Branches:**

```bash
# Feature nova
git checkout -b feature/adiciona-calculadora-prazos

# Bug fix
git checkout -b fix/corrige-filtro-mmr

# Experimento
git checkout -b experiment/testa-gpt4
```

### 2. Documentação de Código

```python
def consultar_base_rag(pergunta: str) -> str:
    """
    Consulta a base vetorial RAG e retorna resposta fundamentada.

    Esta função é exposta ao agente ADK como ferramenta. Ela:
    1. Busca documentos relevantes no FAISS
    2. Constrói prompt com contexto
    3. Invoca LLM (Gemini) para gerar resposta

    Args:
        pergunta: Pergunta do usuário em linguagem natural.
                  Exemplo: "Qual o limite de dispensa?"

    Returns:
        Resposta gerada pelo LLM baseada nos documentos.
        Exemplo: "Segundo o Art. 75 da Lei 14.133..."

    Raises:
        ValueError: Se pergunta for vazia
        Exception: Se falha na comunicação com LLM

    Example:
        >>> resposta = consultar_base_rag("O que é licitação?")
        >>> print(resposta)
        "Licitação é o procedimento administrativo..."

    Notes:
        - Usa MMR search com k=12 por padrão
        - Resposta limitada ao contexto recuperado
        - Ver `_rag_answer()` para detalhes do pipeline
    """
    if not pergunta:
        raise ValueError("Pergunta não pode ser vazia")

    return _rag_answer(pergunta, search_type="mmr", k=12)
```

### 3. Configuração Centralizad a

**Crie `config.py`:**

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
LLM_MODEL = "gemini-2.5-flash"
LLM_PROVIDER = "google_genai"
LLM_TEMPERATURE = 0.0  # Determinístico

# Embeddings
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_NORMALIZE = True

# Retrieval
SEARCH_TYPE = "mmr"  # ou "similarity"
SEARCH_K = 12
SEARCH_FETCH_K = 50
SEARCH_LAMBDA = 0.5

# Paths
DATA_DIR = "data"
VECTOR_DB_PATH = f"{DATA_DIR}/vector_db/v1_faiss_vector_db"
PROCESSED_CSV_PATH = f"{DATA_DIR}/processed/v1_artigos_0.csv"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY não encontrada no .env")
```

**Use em `tools.py`:**

```python
from config import *

llm = init_chat_model(LLM_MODEL, model_provider=LLM_PROVIDER)
modelo_embedding = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={"normalize_embeddings": EMBEDDING_NORMALIZE}
)
vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings=modelo_embedding)
```

## Troubleshooting

### Erro: "GOOGLE_API_KEY not found"

**Sintoma:**
```
Exception: GOOGLE_API_KEY não configurada
```

**Solução:**
1. Verifique se `.env` existe na raiz
2. Abra `.env` e confirme: `GOOGLE_API_KEY=AIza...`
3. Recarregue terminal (ou `source .env`)

### Erro: "No module named 'faiss'"

**Sintoma:**
```
ModuleNotFoundError: No module named 'faiss'
```

**Solução:**
```bash
pip install faiss-cpu==1.12.0
```

### Erro: "allow_dangerous_deserialization"

**Sintoma:**
```
ValueError: Loading FAISS with pickle requires allow_dangerous_deserialization=True
```

**Solução:**
Já corrigido no código:
```python
vector_db = FAISS.load_local(
    ...,
    allow_dangerous_deserialization=True
)
```

### Latência Alta (>10s)

**Causas:**
1. **Primeira carga:** Modelos sendo baixados (~1 GB)
2. **Modelo de embeddings:** Rodando em CPU (sem GPU)
3. **LLM lento:** Gemini com contexto muito grande

**Soluções:**
- Reduza `k` (de 12 para 8)
- Use modelo de embeddings menor
- Considere usar GPU (mude para `faiss-gpu`)

### Respostas Genéricas (Não Baseadas em Documentos)

**Sintoma:** LLM responde com conhecimento geral, não dos docs

**Debug:**
```python
# Imprimir contexto enviado ao LLM
print(f"Contexto: {context}")
```

**Causas:**
1. Documentos recuperados não são relevantes (busca falhou)
2. Prompt não enfatiza "APENAS contexto"

**Soluções:**
- Ajuste embeddings (modelo ou chunk size)
- Reforce prompt: "NUNCA use conhecimento externo"
- Use temperatura=0 (mais determinístico)

---

**Próximo:** [Comandos e Fluxos](05-comandos-fluxos.md)
