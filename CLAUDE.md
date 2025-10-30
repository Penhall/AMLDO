# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AMLDO is a RAG (Retrieval-Augmented Generation) application specialized in Brazilian procurement law (licitação), compliance, governance, and internal regulations. The system uses FAISS vector store with multilingual embeddings to answer questions based on legal documents.

## Environment Setup

**Required:** Python 3.11

```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Register Jupyter kernel (if using notebooks)
python -m ipykernel install --user --name=venv --display-name "amldo_kernel"
```

**Environment Variables:** Create a `.env` file in the root with:
- `GOOGLE_API_KEY` (required for Gemini API)

## Running the Application

**Demo Web Interface:**
```bash
# With venv activated
adk web
```
Then select the agent 'RAG' (either `rag_v1` or `rag_v2`)

## Architecture

### Agent System (Google ADK)

The project uses Google's Agent Development Kit (ADK) to create conversational agents. There are two versions:

- **rag_v1/**: Basic RAG implementation
  - Simple retrieval from FAISS with MMR search
  - Returns raw context directly to LLM

- **rag_v2/**: Enhanced RAG with context post-processing
  - Filters out `artigo_0.txt` from retrieval
  - Restructures context hierarchically: Lei → Título → Capítulo → Artigo
  - Injects "artigo 0" content (chapter/title introductions) from CSV
  - Produces more organized legal document structure for LLM

Both versions expose a `root_agent` (defined in `agent.py`) that uses the `consultar_base_rag` tool (defined in `tools.py`).

### RAG Pipeline

**Embedding Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Multilingual support optimized for Portuguese legal text
- Normalized embeddings

**Vector Store:** FAISS index at `data/vector_db/v1_faiss_vector_db`
- Pre-built index (not created at runtime)
- Must enable `allow_dangerous_deserialization=True` when loading

**LLM:** Gemini 2.5 Flash via LangChain's `init_chat_model`
- Provider: `google_genai`

**Search Configuration:**
- Type: MMR (Maximal Marginal Relevance) for diversity
- K: 12 documents retrieved

### Data Structure

```
data/
├── raw/               # Original PDF legal documents
│   ├── D10024.pdf     # Decreto 10024
│   ├── L13709.pdf     # Lei 13709
│   ├── L14133.pdf     # Lei 14133
│   └── Lcp123.pdf     # Lei Complementar 123
├── split_docs/        # Hierarchically split documents
│   └── {Lei}/TITULO_{X}/capitulos/CAPITULO_{Y}/artigos/artigo_{N}.txt
├── processed/         # Preprocessed data
│   ├── v1_artigos_0.csv          # Chapter/title introductions (artigo 0)
│   └── v1_processed_articles.csv # All processed articles
└── vector_db/
    └── v1_faiss_vector_db/        # FAISS index files
```

Each document chunk has metadata:
- `lei`: Law identifier (e.g., "L14133")
- `titulo`: Title section (e.g., "TITULO_II")
- `capitulo`: Chapter section (e.g., "CAPITULO_III")
- `artigo`: Article filename (e.g., "artigo_15.txt")
- `chunk_idx`: Chunk index within article

### Key Implementation Details

**v2 Context Post-Processing (rag_v2/tools.py:58-93):**
- Sorts retrieved chunks by document hierarchy
- Groups by Lei → Título → Capítulo → Artigo
- Inserts "artigo_0" text (introductory paragraphs) from `df_art_0` at appropriate hierarchy levels
- Wraps content in XML-like tags for clear structure
- This helps LLM understand document organization and relationships

**Agent Instructions:**
Both agents are instructed to:
1. Always call `consultar_base_rag` for regulatory/legal questions
2. Respond only with information from retrieved context (no hallucination)
3. Never mention internal tool usage to users
4. Handle general conversation without tool calls

## Development Workflow

**Testing Changes to RAG:**
1. Modify `rag_v1/tools.py` or `rag_v2/tools.py`
2. Run `adk web` and test with queries
3. Check response quality and context relevance

**Adding New Documents:**
1. Place PDF in `data/raw/`
2. Process using notebooks in root:
   - `get_v1_data.ipynb`: Extract and split documents
   - `get_vectorial_bank_v1.ipynb`: Build FAISS index
3. Ensure metadata fields match existing structure

**Notebooks:**
- `order_rag_study.ipynb`: Analysis and experimentation
- `get_v1_data.ipynb`: Document processing pipeline
- `get_vectorial_bank_v1.ipynb`: Vector store creation

## Important Notes

- **No tests are present** in the project currently
- The `tmp_pkg/` directory contains extracted langchain_google_genai package (likely for debugging/patches)
- FAISS deserialization security: The code uses `allow_dangerous_deserialization=True` which is necessary for loading pickle-based FAISS indices but should only be used with trusted data sources
- Both RAG versions share the same vector database but differ in how they process and present retrieved context
