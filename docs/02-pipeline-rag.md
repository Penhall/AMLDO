# Pipeline RAG do AMLDO

## 📋 Sumário

- [Introdução ao RAG](#introdução-ao-rag)
- [Pipeline v1 - Básico](#pipeline-v1---básico)
- [Pipeline v2 - Aprimorado](#pipeline-v2---aprimorado)
- [Embeddings e Similaridade](#embeddings-e-similaridade)
- [Estratégias de Busca](#estratégias-de-busca)
- [Construção de Prompts](#construção-de-prompts)
- [Otimizações e Tuning](#otimizações-e-tuning)

## Introdução ao RAG

### O que é RAG?

**RAG (Retrieval-Augmented Generation)** é um padrão arquitetural que combina:

1. **Retrieval (Recuperação)**: Busca de informações relevantes em uma base de conhecimento
2. **Augmented (Aumentada)**: Enriquecimento do contexto do modelo
3. **Generation (Geração)**: Criação de resposta usando LLM

### Por que RAG?

| Problema | Solução RAG |
|----------|-------------|
| LLMs têm conhecimento limitado ao treinamento | Busca informações atualizadas em documentos |
| LLMs "alucinam" informações inexistentes | Respostas fundamentadas em documentos reais |
| Dados sensíveis não podem ir para OpenAI/Google | Conhecimento fica local, só query vai para API |
| Contexto fixo do modelo (4k-128k tokens) | Busca apenas trechos relevantes (~12 chunks) |

### Arquitetura RAG do AMLDO

```
┌──────────────┐
│   Pergunta   │ "Qual o limite de dispensa?"
└──────┬───────┘
       │
       ▼
┌────────────────────────────────────┐
│  1. INDEXAÇÃO (Offline)            │
│  ┌──────────────────────────────┐  │
│  │ PDFs → Chunks → Embeddings   │  │
│  │         → FAISS Index        │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  2. RETRIEVAL (Online)             │
│  ┌──────────────────────────────┐  │
│  │ Query Embedding → FAISS      │  │
│  │         → Top-K Docs         │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  3. AUGMENTATION (v2 only)         │
│  ┌──────────────────────────────┐  │
│  │ Sort Hierarchy → Inject      │  │
│  │  Intros → Structure XML      │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  4. GENERATION                     │
│  ┌──────────────────────────────┐  │
│  │ Prompt + Context → Gemini    │  │
│  │         → Resposta           │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Resposta   │ "Segundo Art. 75, Lei 14.133..."
└──────────────┘
```

## Pipeline v1 - Básico

### Visão Geral

Pipeline direto e eficiente, sem pós-processamento do contexto.

**Arquivo:** `rag_v1/tools.py`

### Etapas Detalhadas

#### 1. Inicialização (Carga do Sistema)

```python
# Carregamento do modelo de embeddings
modelo_embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True}
)

# Carregamento do índice FAISS (pré-construído)
vector_db = FAISS.load_local(
    "data/vector_db/v1_faiss_vector_db",
    embeddings=modelo_embedding,
    allow_dangerous_deserialization=True  # ⚠️ Somente com dados confiáveis
)

# Inicialização do LLM
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
```

**Tempo:** ~5-10 segundos (primeira vez)
**Memória:** ~500MB (modelo de embeddings + índice FAISS)

#### 2. Criação do Retriever

```python
def _get_retriever(vector_db=vector_db, search_type: str = "mmr", k: int = 12):
    return vector_db.as_retriever(
        search_type=search_type,  # "mmr" ou "similarity"
        search_kwargs={"k": k}    # número de documentos
    )
```

**Parâmetros:**
- `search_type="mmr"`: Maximal Marginal Relevance (diversidade)
- `k=12`: Retorna 12 chunks mais relevantes

#### 3. Execução da Consulta

```python
def _rag_answer(question: str, search_type: str = "mmr", k: int = 12) -> str:
    retriever = _get_retriever(search_type=search_type, k=k)

    # Template do prompt
    prompt = ChatPromptTemplate.from_template(
        "Use APENAS o contexto para responder.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta:\n{question}"
    )

    # Chain do LangChain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    resposta = rag_chain.invoke(question)
    return resposta
```

**Fluxo:**

1. **Query Embedding:**
   - `question` → `modelo_embedding.embed_query()` → `vector[384]`

2. **FAISS Search:**
   - Busca MMR com k=12
   - Retorna documentos ordenados por relevância e diversidade

3. **Contexto Direto:**
   ```
   Contexto:
   [Chunk 1 - Lei 14.133, Art. 75]
   [Chunk 2 - Lei 14.133, Art. 76]
   [Chunk 3 - Decreto 10.024, Art. 10]
   ...
   [Chunk 12]

   Pergunta:
   Qual o limite de dispensa?
   ```

4. **Geração (Gemini):**
   - LLM processa prompt completo
   - Gera resposta baseada apenas no contexto fornecido

**Tempo de Resposta:** ~2-5 segundos

### Vantagens v1

✅ **Simplicidade**: Código limpo e direto
✅ **Performance**: Rápido, sem overhead de processamento
✅ **Confiabilidade**: Menos pontos de falha
✅ **Debug fácil**: Contexto simples de inspecionar

### Limitações v1

❌ **Contexto desorganizado**: Chunks podem estar fora de ordem legal
❌ **Sem intros**: Perde contexto de títulos/capítulos
❌ **Redundância**: Pode incluir `artigo_0.txt` na busca (duplicação)

## Pipeline v2 - Aprimorado

### Visão Geral

Pipeline com pós-processamento sofisticado para organizar o contexto hierarquicamente.

**Arquivo:** `rag_v2/tools.py`

### Etapas Detalhadas

#### 1. Inicialização (Adicional)

```python
# Carrega CSV com artigos introdutórios
df_art_0 = pd.read_csv('data/processed/v1_artigos_0.csv')
```

**Estrutura de `v1_artigos_0.csv`:**

| lei | titulo | capitulo | texto |
|-----|--------|----------|-------|
| L14133 | TITULO_0 | CAPITULO_0 | Lei nº 14.133, de 1º de abril de 2021... |
| L14133 | TITULO_II | CAPITULO_0 | TÍTULO II - DOS CONTRATOS ADMINISTRATIVOS... |
| L14133 | TITULO_II | CAPITULO_III | CAPÍTULO III - DAS GARANTIAS... |

#### 2. Retriever com Filtro

```python
def _get_retriever(vector_db=vector_db, search_type: str = SEARCH_TYPE, k: int = K):
    return vector_db.as_retriever(
        search_type=search_type,
        search_kwargs={
            "k": k,
            "filter": {
                "artigo": { "$nin": ['artigo_0.txt'] }  # Exclui artigo_0
            }
        }
    )
```

**Por que filtrar `artigo_0.txt`?**
- Esses arquivos contêm intros de capítulos/títulos
- Serão inseridos manualmente nas posições corretas
- Evita duplicação e desorganização

#### 3. Recuperação e Organização

```python
def _rag_answer(question: str, search_type: str = SEARCH_TYPE, k: int = K) -> str:
    retriever = _get_retriever(search_type=search_type, k=k)

    # Invoca retriever
    contexto = retriever.invoke(question)

    # Converte para DataFrame
    linhas = []
    for doc in contexto:
        linhas.append({
            "texto": doc.page_content,
            **doc.metadata  # lei, titulo, capitulo, artigo, chunk_idx
        })

    # Ordenação hierárquica
    df_resultados = pd.DataFrame(linhas).sort_values(
        ['lei', 'titulo', 'capitulo', 'artigo', 'chunk_idx']
    ).reset_index(drop=True)

    # ...continua
```

**Exemplo de Ordenação:**

| lei | titulo | capitulo | artigo | chunk_idx | texto |
|-----|--------|----------|--------|-----------|-------|
| L14133 | TITULO_I | CAPITULO_I | artigo_1.txt | 0 | Art. 1º Esta Lei... |
| L14133 | TITULO_I | CAPITULO_I | artigo_1.txt | 1 | ...continuação... |
| L14133 | TITULO_II | CAPITULO_III | artigo_15.txt | 0 | Art. 15. A contratação... |

#### 4. Pós-Processamento do Contexto

Esta é a **inovação principal do v2**.

```python
def get_pos_processed_context(df_resultados, df_art_0):
    df_cap = df_resultados[['lei', 'titulo', 'capitulo']].drop_duplicates()
    context = ''

    for law in df_cap['lei'].unique():
        context += f'\n\n<LEI {law}>\n'

        # Artigo_0 da lei (intro geral)
        art_0 = get_art_0(law, 'TITULO_0', 'CAPITULO_0', df_art_0)
        if art_0:
            context += f'{art_0}\n'

        df_law = df_cap[df_cap['lei']==law]

        for title in df_law['titulo'].unique():
            # Artigo_0 do título (intro do título)
            art_0 = get_art_0(law, title, 'CAPITULO_0', df_art_0)
            if art_0:
                context += f'{art_0}\n'

            if title != 'TITULO_0':
                context += f'<TITULO: {title}>\n'

            df_title = df_law[df_law['titulo']==title]

            for chapter in df_title['capitulo'].unique():
                # Artigo_0 do capítulo (intro do capítulo)
                art_0 = get_art_0(law, title, chapter, df_art_0)
                if art_0:
                    context += f'{art_0}\n'

                if chapter != 'CAPITULO_0':
                    context += f'<CAPITULO: {chapter}>\n'

                # Recupera chunks deste capítulo
                mask = (df_resultados['lei']==law) & \
                       (df_resultados['titulo']==title) & \
                       (df_resultados['capitulo']==chapter)
                df_chapter = df_resultados[mask]

                for artigo in df_chapter['artigo'].unique():
                    df_article = df_chapter[df_chapter['artigo']==artigo]
                    context += f'<ARTIGO: {artigo.replace(".txt", "")}>\n'

                    for _, row in df_article.iterrows():
                        context += f"{row['texto']}\n"

                    context += f'</ARTIGO: {artigo.replace(".txt", "")}>\n'

                if chapter != 'CAPITULO_0':
                    context += f'</CAPITULO: {chapter}>\n'

            if title != 'TITULO_0':
                context += f'</TITULO: {title}>\n'

        context += f'</LEI {law}>\n'

    return context
```

**Resultado (Exemplo):**

```xml
<LEI L14133>
Lei nº 14.133, de 1º de abril de 2021
Dispõe sobre licitações e contratos administrativos.

<TITULO: TITULO_II>
TÍTULO II - DOS CONTRATOS ADMINISTRATIVOS

<CAPITULO: CAPITULO_III>
CAPÍTULO III - DAS GARANTIAS

<ARTIGO: artigo_15>
Art. 15. A contratação poderá ser precedida de garantia, a critério da Administração,
nas contratações de obras, serviços e compras.

§ 1º Caberá ao contratado optar por uma das seguintes modalidades de garantia:
I - caução em dinheiro;
II - seguro-garantia;
III - fiança bancária.
</ARTIGO: artigo_15>

</CAPITULO: CAPITULO_III>
</TITULO: TITULO_II>
</LEI L14133>
```

#### 5. Geração com Contexto Estruturado

```python
prompt = ChatPromptTemplate.from_template(
    "Use APENAS o contexto para responder.\n\n"
    f"<Contexto>:\n{context}\n</Contexto>\n\n"
    "<Pergunta>:\n{question}</Pergunta>\n\n"
)

rag_chain = (
    {"question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

resposta = rag_chain.invoke(question)
return resposta
```

### Vantagens v2

✅ **Contexto organizado**: Hierarquia legal preservada
✅ **Intros incluídas**: LLM entende estrutura completa
✅ **Referências precisas**: Fácil citar Lei, Título, Capítulo, Artigo
✅ **Melhor compreensão**: LLM vê relacionamento entre seções
✅ **Legibilidade**: Contexto mais fácil de auditar

### Limitações v2

❌ **Complexidade**: Mais código, mais pontos de falha
❌ **Performance**: ~1-2s mais lento (pós-processamento)
❌ **Memória**: Carrega CSV adicional (`df_art_0`)

## Embeddings e Similaridade

### Modelo de Embeddings

**Modelo:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

**Características:**
- **Dimensionalidade:** 384 (menor que muitos modelos, mais eficiente)
- **Multilíngue:** Treinado em 50+ idiomas, incluindo português
- **Normalizado:** Embeddings com norma L2 = 1 (facilita cálculo de similaridade)
- **Domínio:** Paráfrase (entende reformulações da mesma ideia)

### Como Funciona?

```python
# Exemplo simplificado
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True}
)

# Query
query = "Qual o limite de dispensa?"
query_vector = embedding_model.embed_query(query)  # [384 floats]

# Documento
doc = "Art. 75. É dispensável a licitação quando o valor for inferior a R$ 50.000,00"
doc_vector = embedding_model.embed_documents([doc])[0]  # [384 floats]

# Similaridade (cosseno)
similarity = np.dot(query_vector, doc_vector)  # ≈ 0.82 (alta similaridade)
```

### Cálculo de Similaridade

**Cosseno Similarity:**

$$
\text{similarity}(A, B) = \frac{A \cdot B}{||A|| \times ||B||}
$$

Como embeddings são normalizados ($||A|| = ||B|| = 1$):

$$
\text{similarity}(A, B) = A \cdot B
$$

**Valores:**
- `1.0`: Idênticos semanticamente
- `0.8-0.9`: Muito similares
- `0.6-0.8`: Relacionados
- `< 0.6`: Pouco relacionados

## Estratégias de Busca

### 1. Similarity Search (Similaridade Pura)

```python
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 12}
)
```

**Como funciona:**
1. Calcula similaridade entre query e TODOS os chunks
2. Ordena por similaridade (maior → menor)
3. Retorna top-12

**Vantagens:**
✅ Máxima relevância individual
✅ Mais rápido (sem pós-processamento)

**Desvantagens:**
❌ Pode retornar chunks muito similares entre si (redundância)
❌ Perde diversidade de aspectos

### 2. MMR - Maximal Marginal Relevance (Padrão)

```python
retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 12,
        "fetch_k": 50,     # Busca 50 candidatos
        "lambda_mult": 0.5  # Balance relevância vs diversidade
    }
)
```

**Como funciona:**

1. **Fase 1:** Busca `fetch_k` candidatos mais similares (ex: 50)
2. **Fase 2:** Itera `k` vezes (ex: 12):
   - Calcula score: `λ * sim(query, doc) - (1-λ) * max(sim(doc, docs_já_selecionados))`
   - Seleciona documento com maior score
   - Remove da lista de candidatos

**Parâmetro `lambda_mult`:**
- `λ = 1.0`: Apenas relevância (= similarity search)
- `λ = 0.5`: Balance (padrão)
- `λ = 0.0`: Apenas diversidade (pode perder relevância)

**Vantagens:**
✅ Reduz redundância
✅ Cobre mais aspectos da lei
✅ Melhor para perguntas amplas

**Desvantagens:**
❌ Pode perder chunks altamente relevantes mas similares
❌ Mais lento (~2x)

### Comparação Prática

**Query:** "Quais são os limites de dispensa?"

**Similarity Search (top-5):**
1. Art. 75, I - Dispensa até R$ 50.000,00 (obras)
2. Art. 75, I - Dispensa até R$ 50.000,00 (obras) [parágrafo seguinte]
3. Art. 75, I - Dispensa até R$ 50.000,00 (obras) [continuação]
4. Art. 75, II - Dispensa até R$ 10.000,00 (compras)
5. Art. 75, II - Dispensa até R$ 10.000,00 (compras) [parágrafo]

**MMR (top-5):**
1. Art. 75, I - Dispensa até R$ 50.000,00 (obras)
2. Art. 75, II - Dispensa até R$ 10.000,00 (compras)
3. Art. 74 - Conceito de dispensa de licitação
4. Art. 76 - Procedimento para dispensa
5. LCP 123, Art. 48 - Dispensa para MEI

→ **MMR traz mais contexto variado!**

## Construção de Prompts

### Prompt v1 (Simples)

```python
prompt = ChatPromptTemplate.from_template(
    "Use APENAS o contexto para responder.\n\n"
    "Contexto:\n{context}\n\n"
    "Pergunta:\n{question}"
)
```

**Exemplo renderizado:**

```
Use APENAS o contexto para responder.

Contexto:
Art. 75. É dispensável a licitação: I - para contratação que envolva valores...
[mais 11 chunks]

Pergunta:
Qual o limite de dispensa para obras?
```

### Prompt v2 (Estruturado)

```python
prompt = ChatPromptTemplate.from_template(
    "Use APENAS o contexto para responder.\n\n"
    f"<Contexto>:\n{context}\n</Contexto>\n\n"
    "<Pergunta>:\n{question}</Pergunta>\n\n"
)
```

**Exemplo renderizado:**

```
Use APENAS o contexto para responder.

<Contexto>:
<LEI L14133>
Lei nº 14.133, de 1º de abril de 2021

<TITULO: TITULO_IV>
TÍTULO IV - DAS DISPENSAS E DA INEXIGIBILIDADE DE LICITAÇÃO

<CAPITULO: CAPITULO_I>
CAPÍTULO I - DAS DISPENSAS

<ARTIGO: artigo_75>
Art. 75. É dispensável a licitação:
I - para contratação que envolva valores inferiores a R$ 50.000,00 (cinquenta mil reais)...
</ARTIGO: artigo_75>

</CAPITULO: CAPITULO_I>
</TITULO: TITULO_IV>
</LEI L14133>
</Contexto>

<Pergunta>:
Qual o limite de dispensa para obras?
</Pergunta>
```

### Prompts System (Gemini)

O Gemini recebe automaticamente instruções de sistema via Google ADK:

```
Você é um agente RAG especializado em licitação, dispensa por valor,
compliance, governança e normativos internos.

Regras:
1. Use a ferramenta consultar_base_rag para perguntas sobre legislação
2. Responda SOMENTE com informações do contexto fornecido
3. NÃO invente informação
4. Se não encontrar resposta, diga claramente
5. Nunca mencione "estou usando ferramenta X"
```

## Otimizações e Tuning

### Parâmetros Ajustáveis

#### 1. Número de Documentos (k)

```python
k = 12  # Padrão atual
```

**Impacto:**
- ↑ `k`: Mais contexto, maior chance de resposta completa, mais tokens, mais caro
- ↓ `k`: Menos contexto, mais rápido, mais barato, risco de perder info

**Recomendações:**
- Perguntas simples: `k=5-8`
- Perguntas complexas: `k=12-20`
- Limite prático: `k=30` (contexto fica muito grande)

#### 2. Lambda (MMR)

```python
search_kwargs = {
    "k": 12,
    "lambda_mult": 0.5  # Ajustável
}
```

**Experimentos:**
- `λ=0.7`: Mais relevância, menos diversidade
- `λ=0.5`: Balance (padrão)
- `λ=0.3`: Mais diversidade, menos relevância individual

#### 3. Fetch K (MMR)

```python
search_kwargs = {
    "k": 12,
    "fetch_k": 50  # Candidatos iniciais
}
```

**Impacto:**
- ↑ `fetch_k`: Mais candidatos para escolher, mais diversidade, mais lento
- ↓ `fetch_k`: Menos opções, mais rápido

**Recomendação:** `fetch_k = 3-5 × k`

### Tuning de Embeddings

**Chunk Size:**

```python
# get_vectorial_bank_v1.ipynb
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Ajustável
    chunk_overlap=50     # Ajustável
)
```

**Trade-offs:**
- **Chunks grandes (1000+)**: Mais contexto por chunk, menos chunks necessários, mas menos precisão
- **Chunks pequenos (200-500)**: Mais precisão, mais chunks recuperados, risco de fragmentação

**Atual:** 500 chars é um bom balance para legislação

### Métricas de Avaliação

#### 1. Relevância

Medir se documentos recuperados são relevantes:

```python
# Exemplo: conjunto de teste com perguntas e artigos esperados
queries_test = [
    {"query": "Qual limite dispensa obras?", "expected": ["artigo_75"]},
    # ...
]

for test in queries_test:
    docs = retriever.get_relevant_documents(test["query"])
    artigos_recuperados = [d.metadata["artigo"] for d in docs]
    hit = any(exp in artigos_recuperados for exp in test["expected"])
    # Calcular hit@k, MRR, etc.
```

#### 2. Resposta Correta

Avaliar qualidade da resposta final:

```python
# Usar LLM como juiz ou comparação com respostas gold
def avaliar_resposta(pergunta, resposta_gerada, resposta_esperada):
    prompt = f"""
    Avalie se a resposta gerada está correta:

    Pergunta: {pergunta}
    Resposta Gerada: {resposta_gerada}
    Resposta Esperada: {resposta_esperada}

    Score (0-10):
    """
    # ...
```

#### 3. Latência

```python
import time

start = time.time()
resposta = consultar_base_rag("Qual o limite?")
latency = time.time() - start

print(f"Latência: {latency:.2f}s")
```

**Targets:**
- v1: < 3s
- v2: < 5s

---

**Próximo:** [Estrutura de Dados](03-estrutura-dados.md)
