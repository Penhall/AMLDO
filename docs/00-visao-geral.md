# Visão Geral do Projeto AMLDO

## 📋 Sumário

- [Introdução](#introdução)
- [Objetivo do Sistema](#objetivo-do-sistema)
- [Contexto de Negócio](#contexto-de-negócio)
- [Principais Funcionalidades](#principais-funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)

## Introdução

O **AMLDO** (sigla do projeto) é um sistema de RAG (Retrieval-Augmented Generation) especializado em legislação brasileira, focado em:

- Licitações e contratos públicos
- Dispensa de licitação por valor
- Compliance e governança corporativa
- Normativos internos e legislação aplicável

O sistema utiliza inteligência artificial generativa combinada com busca semântica em documentos legais para fornecer respostas precisas e fundamentadas exclusivamente no conteúdo dos documentos indexados.

## Objetivo do Sistema

### Problema que Resolve

Profissionais que trabalham com licitações, compliance e governança precisam constantemente consultar múltiplos documentos legais (leis, decretos, portarias) para:

- Esclarecer dúvidas sobre procedimentos licitatórios
- Verificar limites de valores para dispensa
- Garantir conformidade com normas e regulamentos
- Embasar decisões em legislação vigente

**Desafio:** A busca manual em documentos PDF é demorada, imprecisa e sujeita a erros.

### Solução Proposta

O AMLDO oferece um **assistente conversacional inteligente** que:

1. **Entende perguntas em linguagem natural** (português brasileiro)
2. **Busca semanticamente** nos documentos legais indexados
3. **Retorna respostas fundamentadas** citando exclusivamente o conteúdo oficial
4. **Organiza o contexto hierarquicamente** (Lei → Título → Capítulo → Artigo)
5. **Evita alucinações** ao restringir respostas ao conhecimento indexado

## Contexto de Negócio

### Documentos Suportados

Atualmente, o sistema possui os seguintes documentos legais indexados:

| Documento | Descrição | Relevância |
|-----------|-----------|------------|
| **Lei 14.133/2021** | Nova Lei de Licitações e Contratos Administrativos | Lei principal que rege licitações públicas no Brasil |
| **Lei 13.709/2018** | Lei Geral de Proteção de Dados (LGPD) | Proteção de dados pessoais e privacidade |
| **Lei Complementar 123/2006** | Estatuto Nacional da Microempresa e Empresa de Pequeno Porte | Tratamento diferenciado para ME/EPP em licitações |
| **Decreto 10.024/2019** | Regulamenta licitação na modalidade pregão (eletrônico) | Procedimentos específicos para pregões |

### Público-Alvo

- **Gestores públicos** responsáveis por processos licitatórios
- **Equipes de compliance** de empresas públicas e privadas
- **Advogados** especializados em direito administrativo
- **Auditores** internos e externos
- **Consultorias** em governança corporativa

## Principais Funcionalidades

### 1. Consulta Conversacional

Usuários podem fazer perguntas em linguagem natural:

```
"Qual é o limite de valor para dispensa de licitação?"
"Como funciona o tratamento diferenciado para microempresas?"
"Quais são os requisitos para participar de um pregão eletrônico?"
```

### 2. Busca Semântica Avançada

- **Embeddings multilíngues** otimizados para português
- **Busca por MMR** (Maximal Marginal Relevance) para diversidade de resultados
- **Ranking por relevância** semântica, não apenas palavras-chave

### 3. Respostas Fundamentadas

- Respostas baseadas **exclusivamente** nos documentos indexados
- **Sem alucinações**: sistema informa quando não encontra informação relevante
- Contexto organizado hierarquicamente para melhor compreensão

### 4. Interface Web Interativa

- Interface conversacional via **Google ADK Web**
- Seleção de versões do agente (v1 ou v2)
- Histórico de conversação mantido durante a sessão

## Tecnologias Utilizadas

### Linguagem e Ambiente

- **Python 3.11**: Linguagem principal
- **Virtual Environment**: Isolamento de dependências
- **Jupyter Notebooks**: Processamento e análise de dados

### Frameworks de IA

- **LangChain**: Orquestração de pipelines RAG
- **Google ADK** (Agent Development Kit): Framework de agentes conversacionais
- **Gemini 2.5 Flash**: Modelo de linguagem (LLM) da Google

### Embeddings e Busca

- **Sentence Transformers**: Geração de embeddings
  - Modelo: `paraphrase-multilingual-MiniLM-L12-v2`
- **FAISS** (Facebook AI Similarity Search): Banco vetorial para busca rápida

### Processamento de Documentos

- **PyMuPDF**: Extração de texto de PDFs
- **Pandas**: Manipulação e organização de dados tabulares
- **LangChain Text Splitters**: Chunking de documentos

### Outras Bibliotecas

- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **HuggingFace**: Acesso a modelos de embeddings

## Estrutura do Projeto

```
AMLDO/
├── data/                           # Dados do projeto
│   ├── raw/                        # PDFs originais das leis
│   ├── split_docs/                 # Documentos hierarquicamente divididos
│   ├── processed/                  # CSVs com dados processados
│   └── vector_db/                  # Índice FAISS persistido
│
├── rag_v1/                         # Versão 1 do agente RAG
│   ├── __init__.py
│   ├── agent.py                    # Definição do agente
│   └── tools.py                    # Função de consulta RAG básica
│
├── rag_v2/                         # Versão 2 do agente RAG (melhorado)
│   ├── __init__.py
│   ├── agent.py                    # Definição do agente
│   └── tools.py                    # Consulta RAG com pós-processamento
│
├── docs/                           # Documentação do projeto
│
├── get_v1_data.ipynb              # Notebook: extração e divisão de documentos
├── get_vectorial_bank_v1.ipynb    # Notebook: criação do índice FAISS
├── order_rag_study.ipynb          # Notebook: análises e experimentos
│
├── .env                            # Variáveis de ambiente (GOOGLE_API_KEY)
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação de setup
└── CLAUDE.md                       # Guia para desenvolvimento com Claude Code
```

### Componentes Principais

| Componente | Descrição |
|------------|-----------|
| **rag_v1/** | Implementação básica do RAG com busca direta |
| **rag_v2/** | Versão aprimorada com organização hierárquica do contexto |
| **data/vector_db/** | Banco vetorial FAISS pré-construído (não gerado em runtime) |
| **data/split_docs/** | Documentos divididos em estrutura Lei/Título/Capítulo/Artigo |
| **Notebooks** | Pipelines de processamento e experimentação |

## Diferenças Entre Versões

### RAG v1 (Básico)

- Busca direta no FAISS
- Retorna contexto "cru" para o LLM
- Mais simples e rápido

### RAG v2 (Aprimorado)

- Filtra artigos introdutórios (`artigo_0.txt`) da busca principal
- Reorganiza contexto por hierarquia documental
- Injeta artigos introdutórios nas posições corretas
- Usa tags XML-like para estruturar (`<LEI>`, `<TITULO>`, `<CAPITULO>`, `<ARTIGO>`)
- Melhora compreensão do LLM sobre organização legal

## Próximos Passos

Para começar a trabalhar com o projeto:

1. **[Guia do Desenvolvedor](04-guia-desenvolvedor.md)**: Setup do ambiente
2. **[Arquitetura Técnica](01-arquitetura-tecnica.md)**: Detalhes técnicos do sistema
3. **[Pipeline RAG](02-pipeline-rag.md)**: Como funciona o RAG internamente
4. **[Casos de Uso](07-casos-de-uso.md)**: Exemplos práticos de utilização

---

**Versão da Documentação:** 1.0
**Última Atualização:** 2025-10-30
