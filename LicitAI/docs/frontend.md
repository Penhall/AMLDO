
# Frontend da PoC (Streamlit)

A interface principal da PoC está em `frontend/pages/home.py` e oferece:

1. **Upload e ingestão de normas**
   - Recebe PDF/TXT.
   - Usa `backend.ingestion.ingest.ingest_norma` para gerar um `.txt` normalizado.

2. **Estruturação em artigos**
   - Usa `backend.structure.structure.estrutura_norma` para dividir em artigos e salvar JSONL.

3. **Indexação vetorial**
   - Usa `backend.indexer.indexer.indexar_normas` com uma função de embedding (`dummy_embedding` por padrão).
   - Gera índice FAISS em `vector_store/normas.index` e metadados em `vector_store/normas_metadata.json`.

4. **Busca semântica (RAG simplificado)**
   - Usa `backend.rag.rag_engine.search_normas` para retornar trechos relevantes.

## Como executar

No diretório raiz do projeto:

```bash
streamlit run frontend/pages/home.py
```

Certifique-se de ter instalado:

```bash
pip install streamlit PyPDF2 faiss-cpu
```

Em produção, substitua `dummy_embedding` por uma função de embedding real
(OpenAI, Sentence-Transformers, etc.).
