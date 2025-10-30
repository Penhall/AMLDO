# Arquitetura Técnica do AMLDO

## 📋 Sumário

- [Visão Arquitetural](#visão-arquitetural)
- [Camadas do Sistema](#camadas-do-sistema)
- [Componentes Principais](#componentes-principais)
- [Fluxo de Dados](#fluxo-de-dados)
- [Decisões Arquiteturais](#decisões-arquiteturais)
- [Diagramas](#diagramas)

## Visão Arquitetural

O AMLDO segue uma arquitetura em camadas baseada no padrão RAG (Retrieval-Augmented Generation), com componentes bem definidos e separados por responsabilidade.

### Princípios Arquiteturais

1. **Separação de Responsabilidades**: Agentes, ferramentas e dados separados
2. **Modularidade**: Duas versões independentes (v1 e v2) que compartilham recursos
3. **Extensibilidade**: Fácil adição de novos documentos e funcionalidades
4. **Performance**: Índice FAISS pré-construído para buscas rápidas
5. **Confiabilidade**: Respostas baseadas apenas em documentos indexados

## Camadas do Sistema

### 1. Camada de Apresentação

```
┌─────────────────────────────────┐
│     Interface Web (ADK Web)     │
│   - Conversação em tempo real   │
│   - Seleção de agentes          │
│   - Histórico de sessão         │
└─────────────────────────────────┘
```

**Tecnologia:** Google Agent Development Kit (ADK)

**Responsabilidades:**
- Renderizar interface conversacional
- Gerenciar estado da sessão
- Enviar/receber mensagens do agente
- Exibir respostas formatadas

### 2. Camada de Agentes

```
┌──────────────────┐     ┌──────────────────┐
│   RAG v1 Agent   │     │   RAG v2 Agent   │
│  (Básico)        │     │  (Aprimorado)    │
└──────────────────┘     └──────────────────┘
         │                        │
         └────────┬───────────────┘
                  │
         ┌────────▼────────┐
         │  Tool Interface │
         │  consultar_rag  │
         └─────────────────┘
```

**Tecnologia:** Google ADK + LangChain

**Responsabilidades:**
- Interpretar intenção do usuário
- Decidir quando invocar ferramentas
- Orquestrar chamadas ao RAG
- Formatar resposta final

#### Agent v1 (rag_v1/agent.py)

```python
root_agent = Agent(
    name="rag_v1",
    model="gemini-2.5-flash",
    description="Assistente especializado em licitação...",
    instruction="Você é um agente RAG. Regras: ...",
    tools=[consultar_base_rag]
)
```

**Características:**
- Implementação direta e simples
- Passa pergunta diretamente para ferramenta RAG
- Retorna resposta sem pós-processamento adicional

#### Agent v2 (rag_v2/agent.py)

```python
root_agent = Agent(
    name="rag_v2",
    model="gemini-2.5-flash",
    description="Assistente especializado em licitação...",
    instruction="Você é um agente RAG. Regras: ...",
    tools=[consultar_base_rag]
)
```

**Características:**
- Mesma interface de agente que v1
- Diferença está na implementação da ferramenta
- Contexto mais estruturado para o LLM

### 3. Camada de Ferramentas (Tools)

```
┌─────────────────────────────────────────┐
│         consultar_base_rag()            │
├─────────────────────────────────────────┤
│  v1: Busca simples + LLM                │
│  v2: Busca + Pós-proc. + Reorg. + LLM   │
└─────────────────────────────────────────┘
```

**Responsabilidades:**
- Executar busca vetorial no FAISS
- Processar documentos recuperados
- Construir prompt contextualizado
- Invocar LLM e retornar resposta

#### Implementação v1 (rag_v1/tools.py)

**Fluxo Simplificado:**

```
Pergunta
   │
   ├──> FAISS Retriever (MMR, k=12)
   │
   ├──> Documentos recuperados (raw)
   │
   ├──> Prompt simples com contexto
   │
   ├──> Gemini 2.5 Flash
   │
   └──> Resposta
```

**Código:**
```python
def _rag_answer(question: str, search_type: str = "mmr", k: int = 12):
    retriever = _get_retriever(search_type=search_type, k=k)

    prompt = ChatPromptTemplate.from_template(
        "Use APENAS o contexto para responder.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta:\n{question}"
    )

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

    return rag_chain.invoke(question)
```

#### Implementação v2 (rag_v2/tools.py)

**Fluxo Aprimorado:**

```
Pergunta
   │
   ├──> FAISS Retriever (MMR, k=12, filter: exclude artigo_0)
   │
   ├──> Documentos recuperados
   │
   ├──> Conversão para DataFrame
   │
   ├──> Ordenação hierárquica (Lei→Título→Cap→Art→Chunk)
   │
   ├──> Pós-processamento:
   │     - Agrupar por hierarquia
   │     - Injetar artigo_0 (intros) do CSV
   │     - Estruturar com tags XML
   │
   ├──> Prompt estruturado com contexto organizado
   │
   ├──> Gemini 2.5 Flash
   │
   └──> Resposta
```

**Diferenças Chave:**

1. **Filtro na Busca:**
```python
"filter": {
    "artigo": { "$nin": ['artigo_0.txt'] }
}
```

2. **Pós-Processamento:**
```python
def get_pos_processed_context(df_resultados, df_art_0):
    # Agrupa por Lei → Título → Capítulo → Artigo
    # Insere artigo_0 (intros) nas posições corretas
    # Estrutura com tags: <LEI>, <TITULO>, <CAPITULO>, <ARTIGO>
```

3. **Contexto Estruturado:**
```xml
<LEI L14133>
  Lei 14.133/2021 - Lei de Licitações (intro)

  <TITULO: TITULO_II>
    Dos Contratos Administrativos (intro)

    <CAPITULO: CAPITULO_III>
      Das Garantias (intro)

      <ARTIGO: artigo_15>
      Art. 15. A contratação poderá ser precedida...
      </ARTIGO: artigo_15>

    </CAPITULO: CAPITULO_III>
  </TITULO: TITULO_II>
</LEI L14133>
```

### 4. Camada de Recuperação (Retrieval)

```
┌─────────────────────────────────────┐
│     FAISS Vector Store              │
│  - Índice pré-construído            │
│  - Embeddings multilíngues          │
│  - Busca por similaridade/MMR       │
└─────────────────────────────────────┘
```

**Tecnologia:** FAISS (Facebook AI Similarity Search)

**Características:**
- Índice persistido em disco (`data/vector_db/v1_faiss_vector_db/`)
- Carregado uma vez no início da aplicação
- Busca eficiente em alta dimensionalidade (384 dims)

**Configuração:**
```python
modelo_embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True}
)

vector_db = FAISS.load_local(
    "data/vector_db/v1_faiss_vector_db",
    embeddings=modelo_embedding,
    allow_dangerous_deserialization=True
)

retriever = vector_db.as_retriever(
    search_type="mmr",  # Maximal Marginal Relevance
    search_kwargs={"k": 12}
)
```

### 5. Camada de Modelo de Linguagem (LLM)

```
┌─────────────────────────────────────┐
│      Gemini 2.5 Flash (Google)      │
│  - Modelo generativo rápido         │
│  - Contexto de 1M tokens            │
│  - Multilíngue (PT-BR)              │
└─────────────────────────────────────┘
```

**Inicialização:**
```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai"
)
```

**Prompt System:**
```
Use APENAS o contexto para responder.

<Contexto>:
[Documentos recuperados organizados]
</Contexto>

<Pergunta>:
[Pergunta do usuário]
</Pergunta>
```

### 6. Camada de Dados

```
data/
├── raw/                    # PDFs originais
├── split_docs/             # Documentos estruturados
├── processed/              # CSVs processados
└── vector_db/              # Índice FAISS
```

**Estrutura Hierárquica dos Documentos:**

```
{Lei}/
  └── TITULO_{X}/
       └── capitulos/
            └── CAPITULO_{Y}/
                 ├── capitulo_{Y}.txt (intro)
                 └── artigos/
                      ├── artigo_0.txt (intro do capítulo)
                      ├── artigo_1.txt
                      ├── artigo_2.txt
                      └── ...
```

**Metadados de Cada Chunk:**

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `lei` | str | Identificador da lei | `"L14133"` |
| `titulo` | str | Seção de título | `"TITULO_II"` |
| `capitulo` | str | Seção de capítulo | `"CAPITULO_III"` |
| `artigo` | str | Nome do arquivo do artigo | `"artigo_15.txt"` |
| `chunk_idx` | int | Índice do chunk no artigo | `0`, `1`, `2`... |

## Fluxo de Dados

### Fluxo Completo de uma Consulta (v2)

```
┌──────────┐
│ Usuário  │
└────┬─────┘
     │ "Qual o limite para dispensa?"
     ▼
┌─────────────────┐
│   ADK Web UI    │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│  RAG v2 Agent   │ ◄── Analisa intenção
│  (Gemini Flash) │     Decide invocar tool
└────┬────────────┘
     │ invoke: consultar_base_rag("Qual o limite...")
     ▼
┌──────────────────────────────┐
│ consultar_base_rag() [v2]    │
├──────────────────────────────┤
│ 1. Query embedding           │ ◄── HuggingFace Embeddings
│ 2. FAISS search (MMR, k=12)  │ ◄── Vector DB
│ 3. Filter artigo_0 out       │
│ 4. Sort by hierarchy         │ ◄── Pandas
│ 5. Post-process context      │ ◄── Inject artigo_0, add tags
│ 6. Build structured prompt   │
│ 7. LLM inference             │ ◄── Gemini Flash
└────┬─────────────────────────┘
     │ "Segundo a Lei 14.133/2021, Art. X..."
     ▼
┌─────────────────┐
│  RAG v2 Agent   │ ◄── Formata resposta final
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│   ADK Web UI    │ ◄── Exibe ao usuário
└────┬────────────┘
     │
     ▼
┌──────────┐
│ Usuário  │
└──────────┘
```

### Fluxo de Criação do Índice (Offline)

```
┌──────────────────┐
│  PDFs (data/raw) │
└────┬─────────────┘
     │
     ▼ [get_v1_data.ipynb]
┌─────────────────────────────┐
│ 1. Extração de texto        │ ◄── PyMuPDF
│ 2. Estruturação hierárquica │
│ 3. Divisão Lei/Tít/Cap/Art  │
└────┬────────────────────────┘
     │
     ▼
┌──────────────────────────────┐
│ data/split_docs/             │
│ Estrutura de diretórios      │
└────┬─────────────────────────┘
     │
     ▼ [get_vectorial_bank_v1.ipynb]
┌──────────────────────────────┐
│ 1. Load split_docs           │
│ 2. Chunk documents           │ ◄── LangChain Splitters
│ 3. Generate embeddings       │ ◄── HuggingFace
│ 4. Build FAISS index         │ ◄── FAISS
│ 5. Add metadata              │
│ 6. Persist to disk           │
└────┬─────────────────────────┘
     │
     ▼
┌──────────────────────────────┐
│ data/vector_db/              │
│ FAISS index files            │
└──────────────────────────────┘
```

## Decisões Arquiteturais

### 1. Por que FAISS em vez de ChromaDB/Pinecone?

**Decisão:** Usar FAISS local

**Justificativa:**
- ✅ **Performance**: FAISS é extremamente rápido para milhares de documentos
- ✅ **Sem custos**: Solução local, sem APIs pagas
- ✅ **Privacy**: Dados sensíveis não saem do servidor
- ✅ **Simplicidade**: Arquivo único, fácil versionamento
- ⚠️ **Limitação**: Não escala para milhões de documentos (não é o caso atual)

### 2. Por que Duas Versões (v1 e v2)?

**Decisão:** Manter ambas implementações

**Justificativa:**
- ✅ **Experimentação**: Comparar abordagens (simples vs. estruturado)
- ✅ **Fallback**: v1 como backup se v2 tiver problemas
- ✅ **Performance**: v1 mais rápido, v2 mais preciso
- ✅ **Aprendizado**: Mostra evolução do sistema

### 3. Por que MMR em vez de Similarity?

**Decisão:** Usar MMR (Maximal Marginal Relevance) como padrão

**Justificativa:**
- ✅ **Diversidade**: Evita chunks muito similares entre si
- ✅ **Cobertura**: Aumenta chance de pegar diferentes aspectos da lei
- ✅ **Qualidade**: Reduz redundância no contexto
- ⚠️ **Trade-off**: Pode perder chunks altamente relevantes mas similares

### 4. Por que Gemini 2.5 Flash em vez de GPT-4?

**Decisão:** Usar Gemini 2.5 Flash da Google

**Justificativa:**
- ✅ **Contexto longo**: Suporta até 1M tokens (importante para leis extensas)
- ✅ **Custo**: Mais barato que GPT-4
- ✅ **Velocidade**: Flash = rápido, baixa latência
- ✅ **Multilíngue**: Excelente suporte a português
- ⚠️ **Dependência**: Depende de API da Google

### 5. Por que Estrutura Hierárquica (v2)?

**Decisão:** Organizar contexto em Lei → Título → Capítulo → Artigo

**Justificativa:**
- ✅ **Compreensão**: LLM entende melhor a organização legal
- ✅ **Referências**: Permite citações precisas (Lei X, Art. Y)
- ✅ **Contexto**: Intros (artigo_0) fornecem overview de seções
- ✅ **Leitura**: Facilita debug e validação humana
- ⚠️ **Complexidade**: Código mais elaborado

### 6. Por que Notebooks para Processamento?

**Decisão:** Pipelines em Jupyter Notebooks

**Justificativa:**
- ✅ **Exploração**: Fácil testar e visualizar cada etapa
- ✅ **Documentação**: Cells misturam código e explicação
- ✅ **Iteração**: Rápido ajustar parâmetros e reprocessar
- ⚠️ **Produção**: Não ideal para deploy automatizado (considerar scripts Python)

## Diagramas

### Diagrama de Componentes

```
┌────────────────────────────────────────────────────────────┐
│                       AMLDO System                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐                                         │
│  │  ADK Web UI  │ ◄─────────────────┐                     │
│  └──────┬───────┘                    │                     │
│         │                            │                     │
│         ▼                            │                     │
│  ┌──────────────────────────────────┴──┐                  │
│  │    Agent Layer (Google ADK)         │                  │
│  ├─────────────────────────────────────┤                  │
│  │  ┌─────────┐      ┌──────────┐     │                  │
│  │  │ RAG v1  │      │  RAG v2  │     │                  │
│  │  │ Agent   │      │  Agent   │     │                  │
│  │  └────┬────┘      └────┬─────┘     │                  │
│  │       │                │            │                  │
│  │       └────────┬───────┘            │                  │
│  └────────────────┼────────────────────┘                  │
│                   │                                        │
│                   ▼                                        │
│  ┌─────────────────────────────────────┐                  │
│  │    Tool Layer (LangChain)           │                  │
│  ├─────────────────────────────────────┤                  │
│  │  consultar_base_rag()               │                  │
│  │  ├─ v1: Simple retrieval            │                  │
│  │  └─ v2: Structured retrieval        │                  │
│  └────────┬──────────────────┬─────────┘                  │
│           │                  │                            │
│           ▼                  ▼                            │
│  ┌────────────────┐  ┌──────────────────┐                │
│  │  FAISS Vector  │  │  Gemini 2.5      │                │
│  │  Store         │  │  Flash LLM       │                │
│  │  (Embeddings)  │  │  (Google)        │                │
│  └────────────────┘  └──────────────────┘                │
│           ▲                                                │
│           │                                                │
│  ┌────────┴─────────────────────────────┐                 │
│  │  Data Layer                          │                 │
│  ├──────────────────────────────────────┤                 │
│  │  • data/vector_db/                   │                 │
│  │  • data/split_docs/                  │                 │
│  │  • data/processed/ (CSVs)            │                 │
│  └──────────────────────────────────────┘                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Diagrama de Sequência (Consulta v2)

```sequence
Usuário->ADK UI: "Qual o limite?"
ADK UI->Agent v2: Mensagem do usuário
Agent v2->Agent v2: Analisa intenção
Agent v2->Tool v2: consultar_base_rag("Qual o limite?")
Tool v2->Embeddings: Gera embedding da query
Embeddings-->Tool v2: Vector [384 dims]
Tool v2->FAISS: search(vector, k=12, mmr, filter)
FAISS-->Tool v2: 12 documentos + metadados
Tool v2->Tool v2: Sort hierarquia
Tool v2->Tool v2: Pós-processa contexto
Tool v2->Gemini: Prompt + contexto estruturado
Gemini-->Tool v2: Resposta gerada
Tool v2-->Agent v2: Texto da resposta
Agent v2->Agent v2: Formata resposta
Agent v2-->ADK UI: Resposta final
ADK UI-->Usuário: Exibe resposta
```

---

**Próximo:** [Pipeline RAG Detalhado](02-pipeline-rag.md)
