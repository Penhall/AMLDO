"""
Página de Pipeline - Processamento de documentos.

Permite upload e processamento completo de normas/editais:
1. Upload e ingestão (PDF/TXT)
2. Estruturação em artigos
3. Indexação vetorial (FAISS)
"""

import os
from pathlib import Path
from typing import List

import streamlit as st

# Imports dos módulos refatorados
from amldo.pipeline.ingestion.ingest import ingest_norma
from amldo.pipeline.structure.structure import estrutura_norma
from amldo.pipeline.indexer.indexer import indexar_normas
from amldo.pipeline.embeddings import get_embedding_function
from amldo.core.config import settings
from amldo.core.exceptions import IngestionError, StructureError, IndexingError


st.set_page_config(page_title="Pipeline - AMLDO", layout="wide")

st.title("🔄 Pipeline de Processamento de Documentos")

st.markdown(
    """
    **Fluxo completo de processamento:**

    1. **Ingestão**: Upload de norma (PDF/TXT) → extração de texto
    2. **Estruturação**: Divisão em artigos usando regex
    3. **Indexação**: Geração de embeddings e criação de índice FAISS

    **IMPORTANTE**: Esta versão usa embeddings REAIS (não dummy) via sentence-transformers.
    """
)

st.divider()

# =============================================================================
# Sessão 1: Upload e Ingestão
# =============================================================================

st.header("1. Upload e Ingestão de Norma")

uploaded_file = st.file_uploader(
    "Envie uma lei/decreto/edital em PDF ou TXT", type=["pdf", "txt", "md"]
)

col1, col2 = st.columns(2)

with col1:
    if uploaded_file is not None:
        st.success(f"Arquivo recebido: {uploaded_file.name}")

        if st.button("Ingerir Norma", type="primary"):
            with st.spinner("Processando arquivo..."):
                try:
                    # Salvar temporariamente em data/uploads
                    upload_dir = Path("data/uploads")
                    upload_dir.mkdir(parents=True, exist_ok=True)
                    temp_path = upload_dir / uploaded_file.name
                    temp_path.write_bytes(uploaded_file.getvalue())

                    # Ingestão
                    raw_txt_path = ingest_norma(str(temp_path))
                    st.session_state["raw_txt_path"] = raw_txt_path
                    st.success(f"✅ Texto bruto salvo em: `{raw_txt_path}`")

                    # Preview
                    with open(raw_txt_path, "r", encoding="utf-8") as f:
                        preview = f.read()[:500]
                    st.text_area("Preview do texto (primeiros 500 chars)", preview, height=150)

                except IngestionError as e:
                    st.error(f"❌ Erro na ingestão: {e}")
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {e}")
    else:
        st.caption("Aguardando upload de arquivo...")

with col2:
    if "raw_txt_path" in st.session_state:
        st.info(f"Última ingestão: `{st.session_state['raw_txt_path']}`")

# =============================================================================
# Sessão 2: Estruturação em Artigos
# =============================================================================

st.divider()
st.header("2. Estruturação em Artigos")

raw_txt_path = st.session_state.get("raw_txt_path")
default_structured_path = "data/normas_structured/artigos.jsonl"

if raw_txt_path:
    st.write(f"Arquivo de texto bruto atual: `{raw_txt_path}`")

    if st.button("Estruturar Norma em Artigos", type="primary"):
        with st.spinner("Dividindo texto em artigos..."):
            try:
                structured_path = estrutura_norma(raw_txt_path, default_structured_path)
                st.session_state["structured_path"] = structured_path
                st.success(f"✅ Artigos estruturados salvos em: `{structured_path}`")

                # Contagem de artigos
                import json

                with open(structured_path, "r", encoding="utf-8") as f:
                    count = sum(1 for line in f if line.strip())
                st.metric("Total de artigos extraídos", count)

            except StructureError as e:
                st.error(f"❌ Erro na estruturação: {e}")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")
else:
    st.warning("⚠️ Nenhuma norma ingerida ainda. Complete a etapa 1 primeiro.")

# =============================================================================
# Sessão 3: Indexação Vetorial
# =============================================================================

st.divider()
st.header("3. Indexação Vetorial FAISS")

structured_path = st.session_state.get("structured_path")

index_path = "vector_store/normas.index"
metadata_path = "vector_store/normas_metadata.json"

if structured_path:
    st.write(f"Base estruturada atual: `{structured_path}`")

    st.info(
        f"""
        **Configuração de embeddings:**
        - Modelo: `{settings.embedding_model}`
        - Dimensão: {settings.embedding_dimension}
        - Provider: sentence-transformers (embeddings reais, não dummy!)
        """
    )

    if st.button("Gerar Índice Vetorial", type="primary"):
        with st.spinner("Gerando embeddings e criando índice FAISS..."):
            try:
                os.makedirs("vector_store", exist_ok=True)

                # Usa embeddings reais via EmbeddingManager
                embedding_fn = get_embedding_function()

                idx_path, meta_path = indexar_normas(
                    structured_path,
                    embedding_fn=embedding_fn,  # Embeddings reais!
                    index_path=index_path,
                    metadata_path=metadata_path,
                )

                st.session_state["index_path"] = idx_path
                st.session_state["metadata_path"] = meta_path

                st.success(f"✅ Índice criado em: `{idx_path}`")
                st.success(f"✅ Metadados salvos em: `{meta_path}`")

                st.balloons()

            except IndexingError as e:
                st.error(f"❌ Erro na indexação: {e}")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")
else:
    st.warning("⚠️ Nenhuma base estruturada disponível para indexação. Complete a etapa 2 primeiro.")

# =============================================================================
# Status Geral
# =============================================================================

st.divider()
st.subheader("Status do Pipeline")

col1, col2, col3 = st.columns(3)

with col1:
    status_ingestao = "✅" if "raw_txt_path" in st.session_state else "⏸️"
    st.metric("1. Ingestão", status_ingestao)

with col2:
    status_estrutura = "✅" if "structured_path" in st.session_state else "⏸️"
    st.metric("2. Estruturação", status_estrutura)

with col3:
    status_index = "✅" if "index_path" in st.session_state else "⏸️"
    st.metric("3. Indexação", status_index)

st.caption(
    """
    💡 **Próximos passos:**
    - Vá para a página **RAG Query** para testar consultas no índice criado
    - Ou processe mais documentos repetindo este fluxo
    """
)
