# Estrutura de Dados do AMLDO

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Documentos Brutos (raw)](#documentos-brutos-raw)
- [Documentos Divididos (split_docs)](#documentos-divididos-split_docs)
- [Dados Processados (processed)](#dados-processados-processed)
- [Banco Vetorial (vector_db)](#banco-vetorial-vector_db)
- [Formato de Metadados](#formato-de-metadados)
- [Fluxo de Transformação](#fluxo-de-transformação)

## Visão Geral

O AMLDO organiza dados em **4 camadas**, cada uma representando um estágio de processamento:

```
PDFs (raw) → Arquivos de Texto (split_docs) → CSVs (processed) → Vetores (vector_db)
```

| Camada | Formato | Propósito | Gerado por |
|--------|---------|-----------|------------|
| `raw/` | PDF | Documentos originais | Manual (download) |
| `split_docs/` | TXT | Hierarquia Lei/Título/Cap/Art | `get_v1_data.ipynb` |
| `processed/` | CSV | Dados tabulares | `get_v1_data.ipynb` |
| `vector_db/` | FAISS | Índice vetorial | `get_vectorial_bank_v1.ipynb` |

## Estrutura de Diretórios

```
data/
│
├── raw/                                  # Camada 1: PDFs Originais
│   ├── D10024.pdf                        # Decreto 10.024/2019
│   ├── L13709.pdf                        # Lei 13.709/2018 (LGPD)
│   ├── L14133.pdf                        # Lei 14.133/2021
│   └── Lcp123.pdf                        # Lei Complementar 123/2006
│
├── split_docs/                           # Camada 2: Textos Estruturados
│   ├── D10024/
│   │   └── TITULO_0/
│   │       └── capitulos/
│   │           ├── CAPITULO_0/
│   │           │   ├── capitulo_0.txt
│   │           │   └── artigos/
│   │           │       └── artigo_0.txt
│   │           ├── CAPITULO_I/
│   │           │   ├── capitulo_1.txt
│   │           │   └── artigos/
│   │           │       ├── artigo_0.txt
│   │           │       ├── artigo_1.txt
│   │           │       ├── artigo_2.txt
│   │           │       └── ...
│   │           └── ...
│   ├── L13709/
│   │   └── [mesma estrutura]
│   ├── L14133/
│   │   ├── TITULO_0/
│   │   ├── TITULO_I/
│   │   ├── TITULO_II/
│   │   │   └── capitulos/
│   │   │       ├── CAPITULO_I/
│   │   │       ├── CAPITULO_II/
│   │   │       └── CAPITULO_III/
│   │   └── ...
│   └── Lcp123/
│       └── [mesma estrutura]
│
├── processed/                            # Camada 3: CSVs
│   ├── v1_artigos_0.csv                  # Artigos introdutórios
│   └── v1_processed_articles.csv        # Todos os artigos processados
│
└── vector_db/                            # Camada 4: FAISS Index
    └── v1_faiss_vector_db/
        ├── index.faiss                   # Índice de busca
        └── index.pkl                     # Metadados e mapeamentos
```

## Documentos Brutos (raw)

### Localização

```
data/raw/
```

### Conteúdo

| Arquivo | Descrição | Páginas | Tamanho |
|---------|-----------|---------|---------|
| `L14133.pdf` | Lei 14.133/2021 - Lei de Licitações e Contratos | ~200 | ~1.5 MB |
| `L13709.pdf` | Lei 13.709/2018 - LGPD | ~40 | ~300 KB |
| `Lcp123.pdf` | Lei Complementar 123/2006 - Estatuto da ME/EPP | ~80 | ~800 KB |
| `D10024.pdf` | Decreto 10.024/2019 - Pregão Eletrônico | ~30 | ~250 KB |

### Nomenclatura

**Padrão:** `{tipo}{número}.pdf`

| Tipo | Prefixo | Exemplo |
|------|---------|---------|
| Lei | `L` | `L14133.pdf` |
| Lei Complementar | `Lcp` | `Lcp123.pdf` |
| Decreto | `D` | `D10024.pdf` |
| Portaria | `P` | `P123.pdf` |
| Instrução Normativa | `IN` | `IN456.pdf` |

### Adição de Novos Documentos

Para adicionar um novo documento:

1. Baixe o PDF oficial
2. Renomeie seguindo o padrão acima
3. Coloque em `data/raw/`
4. Execute `get_v1_data.ipynb` para processar
5. Execute `get_vectorial_bank_v1.ipynb` para reindexar

## Documentos Divididos (split_docs)

### Localização

```
data/split_docs/{Lei}/TITULO_{X}/capitulos/CAPITULO_{Y}/artigos/
```

### Estrutura Hierárquica

A estrutura reflete a organização legal brasileira:

```
Lei
├── Título 0 (introdução da lei)
│   └── Capítulo 0 (sem capítulos formais)
│       └── Artigos
│
├── Título I
│   ├── Capítulo 0 (introdução do título)
│   ├── Capítulo I
│   │   └── Artigos
│   ├── Capítulo II
│   │   └── Artigos
│   └── ...
│
├── Título II
│   └── ...
│
└── ...
```

### Tipos de Arquivos

#### 1. `capitulo_{N}.txt`

**Conteúdo:** Nome/descrição do capítulo

**Exemplo (`capitulo_1.txt`):**
```
CAPÍTULO I
DAS DISPOSIÇÕES GERAIS
```

#### 2. `artigo_0.txt`

**Conteúdo:** Introdução da seção (antes do primeiro artigo numerado)

**Exemplo (Lei 14.133, Título II, artigo_0.txt):**
```
TÍTULO II
DOS CONTRATOS ADMINISTRATIVOS

Este título trata das normas aplicáveis aos contratos administrativos decorrentes de licitação.
```

**Uso:** Inserido manualmente pelo pipeline v2 para dar contexto

#### 3. `artigo_{N}.txt`

**Conteúdo:** Texto completo do artigo N

**Exemplo (`artigo_75.txt`):**
```
Art. 75. É dispensável a licitação:

I - para contratação que envolva valores inferiores a R$ 50.000,00 (cinquenta mil reais), no caso de obras e serviços de engenharia ou de serviços de manutenção de veículos automotores;

II - para contratação que envolva valores inferiores a R$ 10.000,00 (dez mil reais), no caso de compras ou de serviços, exceto os serviços de engenharia;

III - para contratação dos serviços técnicos especializados de que trata o inciso II do caput do art. 74 desta Lei com valores inferiores a R$ 30.000,00 (trinta mil reais).

§ 1º Os valores estabelecidos nos incisos I, II e III do caput deste artigo serão o dobro quando se tratar de consórcios públicos...
```

### Exemplo Real de Hierarquia

**Caminho:**
```
data/split_docs/L14133/TITULO_IV/capitulos/CAPITULO_I/artigos/artigo_75.txt
```

**Interpretação:**
- **Lei:** 14.133/2021
- **Título:** IV (Das Dispensas e da Inexigibilidade de Licitação)
- **Capítulo:** I (Das Dispensas)
- **Artigo:** 75

## Dados Processados (processed)

### Localização

```
data/processed/
```

### 1. `v1_artigos_0.csv`

**Propósito:** Armazena artigos introdutórios (artigo_0.txt) para injeção no pipeline v2

**Estrutura:**

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `lei` | str | Identificador da lei | `L14133` |
| `titulo` | str | Título da seção | `TITULO_II` |
| `capitulo` | str | Capítulo da seção | `CAPITULO_III` |
| `texto` | str | Conteúdo do artigo_0 | `TÍTULO II - DOS CONTRATOS...` |

**Exemplo de Linhas:**

```csv
lei,titulo,capitulo,texto
L14133,TITULO_0,CAPITULO_0,"Lei nº 14.133, de 1º de abril de 2021. Dispõe sobre licitações e contratos administrativos."
L14133,TITULO_II,CAPITULO_0,"TÍTULO II - DOS CONTRATOS ADMINISTRATIVOS"
L14133,TITULO_II,CAPITULO_III,"CAPÍTULO III - DAS GARANTIAS"
```

**Uso:**
```python
df_art_0 = pd.read_csv('data/processed/v1_artigos_0.csv')

# Buscar intro do Título II, Capítulo III da Lei 14.133
intro = df_art_0[
    (df_art_0['lei'] == 'L14133') &
    (df_art_0['titulo'] == 'TITULO_II') &
    (df_art_0['capitulo'] == 'CAPITULO_III')
]['texto'].values[0]
```

### 2. `v1_processed_articles.csv`

**Propósito:** Registro completo de todos os artigos processados

**Estrutura:**

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `lei` | str | Identificador da lei | `L14133` |
| `titulo` | str | Título da seção | `TITULO_IV` |
| `capitulo` | str | Capítulo da seção | `CAPITULO_I` |
| `artigo` | str | Nome do arquivo do artigo | `artigo_75.txt` |
| `texto` | str | Conteúdo completo | `Art. 75. É dispensável...` |
| `num_tokens` | int | Número de tokens (estimado) | `450` |
| `num_chars` | int | Número de caracteres | `2341` |

**Uso:**
- Auditoria de conteúdo processado
- Estatísticas (distribuição de tamanho de artigos)
- Debugging (verificar se artigo foi extraído corretamente)

## Banco Vetorial (vector_db)

### Localização

```
data/vector_db/v1_faiss_vector_db/
```

### Arquivos

#### 1. `index.faiss`

**Formato:** Binário FAISS

**Conteúdo:**
- Vetores de embeddings (384 dimensões cada)
- Estrutura de índice para busca rápida
- Algoritmo: HNSW ou Flat (depende da construção)

**Tamanho:** ~10-50 MB (depende do número de chunks)

#### 2. `index.pkl`

**Formato:** Pickle Python

**Conteúdo:**
- Mapeamento `chunk_id → metadata`
- Textos originais dos chunks
- Docstore para recuperação

**Estrutura (simplificada):**
```python
{
    "docstore": {
        "uuid-1234": Document(
            page_content="Art. 75. É dispensável...",
            metadata={
                "lei": "L14133",
                "titulo": "TITULO_IV",
                "capitulo": "CAPITULO_I",
                "artigo": "artigo_75.txt",
                "chunk_idx": 0
            }
        ),
        # ...mais documentos
    },
    "index_to_docstore_id": {
        0: "uuid-1234",
        1: "uuid-5678",
        # ...
    }
}
```

### Características do Índice

**Número de Vetores:** ~2.000-5.000 (depende do chunking)

**Dimensionalidade:** 384 (modelo paraphrase-multilingual-MiniLM-L12-v2)

**Tipo de Índice:** FlatL2 ou HNSW
- **FlatL2**: Busca exaustiva, precisa, rápida para <100k vetores
- **HNSW**: Busca aproximada, escalável, para >100k vetores

**Busca:**
```python
# Similaridade
results = index.similarity_search(query, k=12)

# MMR
results = index.max_marginal_relevance_search(query, k=12, fetch_k=50)
```

## Formato de Metadados

### Metadados de Cada Chunk

Cada chunk no FAISS possui os seguintes metadados:

```python
metadata = {
    "lei": str,          # Identificador da lei
    "titulo": str,       # Seção de título
    "capitulo": str,     # Seção de capítulo
    "artigo": str,       # Nome do arquivo do artigo
    "chunk_idx": int,    # Índice do chunk dentro do artigo
    "source": str        # Caminho completo do arquivo (opcional)
}
```

### Exemplo Completo

```python
Document(
    page_content="""
    Art. 75. É dispensável a licitação:

    I - para contratação que envolva valores inferiores a R$ 50.000,00
    (cinquenta mil reais), no caso de obras e serviços de engenharia ou de
    serviços de manutenção de veículos automotores;
    """,
    metadata={
        "lei": "L14133",
        "titulo": "TITULO_IV",
        "capitulo": "CAPITULO_I",
        "artigo": "artigo_75.txt",
        "chunk_idx": 0,
        "source": "data/split_docs/L14133/TITULO_IV/capitulos/CAPITULO_I/artigos/artigo_75.txt"
    }
)
```

### Uso dos Metadados

#### 1. Filtragem (v2)

```python
retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 12,
        "filter": {
            "artigo": {"$nin": ['artigo_0.txt']}  # Exclui artigo_0
        }
    }
)
```

#### 2. Ordenação Hierárquica (v2)

```python
df.sort_values(['lei', 'titulo', 'capitulo', 'artigo', 'chunk_idx'])
```

#### 3. Agrupamento

```python
# Agrupar chunks por artigo
grouped = df.groupby(['lei', 'titulo', 'capitulo', 'artigo'])

for (lei, titulo, cap, art), group in grouped:
    print(f"{lei} - {titulo} - {cap} - {art}")
    print(group['texto'].tolist())
```

## Fluxo de Transformação

### Pipeline Completo

```
┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 1: Extração e Estruturação (get_v1_data.ipynb)            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  data/raw/L14133.pdf                                             │
│         │                                                        │
│         ├─> PyMuPDF (extração de texto)                          │
│         │                                                        │
│         ├─> Regex (identificação de estrutura)                   │
│         │    - Detectar Títulos (TÍTULO I, II, III...)          │
│         │    - Detectar Capítulos (CAPÍTULO I, II, III...)      │
│         │    - Detectar Artigos (Art. 1º, Art. 2º...)           │
│         │                                                        │
│         ├─> Divisão em arquivos hierárquicos                     │
│         │                                                        │
│         └─> Salvar em data/split_docs/L14133/                    │
│                                                                  │
│  Simultaneamente:                                                │
│         ├─> Gerar data/processed/v1_artigos_0.csv                │
│         └─> Gerar data/processed/v1_processed_articles.csv       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 2: Vetorização (get_vectorial_bank_v1.ipynb)              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  data/split_docs/                                                │
│         │                                                        │
│         ├─> Carregar todos os artigos                            │
│         │                                                        │
│         ├─> Text Splitting (LangChain)                           │
│         │    - chunk_size=500                                    │
│         │    - chunk_overlap=50                                  │
│         │                                                        │
│         ├─> Gerar Embeddings (HuggingFace)                       │
│         │    - Modelo: paraphrase-multilingual-MiniLM-L12-v2    │
│         │    - Dimensões: 384                                    │
│         │                                                        │
│         ├─> Adicionar Metadados (lei, titulo, capitulo, artigo) │
│         │                                                        │
│         ├─> Construir Índice FAISS                               │
│         │                                                        │
│         └─> Salvar data/vector_db/v1_faiss_vector_db/            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ ETAPA 3: Uso em Runtime (rag_v1/rag_v2)                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Carrega FAISS + Embeddings + df_art_0.csv (uma vez)            │
│         │                                                        │
│         └─> Pronto para consultas!                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Dependências Entre Camadas

```
raw/ (manual)
  │
  └─> split_docs/ (get_v1_data.ipynb)
       │
       ├─> processed/ (get_v1_data.ipynb)
       │
       └─> vector_db/ (get_vectorial_bank_v1.ipynb)
            │
            └─> Usado por rag_v1 e rag_v2 (runtime)
```

### Reprocessamento

**Quando reprocessar?**

1. **Adicionar/atualizar documentos em `raw/`**
   - Execute `get_v1_data.ipynb` (regenera `split_docs/` e `processed/`)
   - Execute `get_vectorial_bank_v1.ipynb` (regenera `vector_db/`)

2. **Mudar chunk_size ou overlap**
   - Execute apenas `get_vectorial_bank_v1.ipynb`
   - (não precisa reprocessar `split_docs/`)

3. **Mudar modelo de embeddings**
   - Execute apenas `get_vectorial_bank_v1.ipynb`
   - (não precisa reprocessar `split_docs/`)

## Estatísticas dos Dados

### Resumo Quantitativo

| Métrica | Valor Aproximado |
|---------|------------------|
| **PDFs originais** | 4 documentos |
| **Páginas totais** | ~350 páginas |
| **Artigos extraídos** | ~500 artigos |
| **Chunks gerados** | ~2.500-5.000 chunks |
| **Tamanho total (texto)** | ~5 MB |
| **Tamanho FAISS index** | ~30 MB |

### Distribuição por Lei

| Lei | Artigos | Páginas | Chunks (aprox.) |
|-----|---------|---------|-----------------|
| L14133 | ~190 | 200 | 2000 |
| L13709 | ~65 | 40 | 600 |
| Lcp123 | ~150 | 80 | 1000 |
| D10024 | ~40 | 30 | 400 |

---

**Próximo:** [Guia do Desenvolvedor](04-guia-desenvolvedor.md)
