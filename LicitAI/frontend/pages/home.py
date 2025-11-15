
"""Página inicial Streamlit para a PoC de Licitações."""

import os
from pathlib import Path
from typing import List

import streamlit as st

from backend.ingestion.ingest import ingest_norma
from backend.structure.structure import estrutura_norma
from backend.indexer.indexer import indexar_normas
from backend.rag.rag_engine import search_normas


st.set_page_config(page_title="PoC - Análise de Editais", layout="wide")

st.title("PoC - Sistema Inteligente de Análise de Editais de Licitação")


st.markdown(
    """
    Esta interface conecta o fluxo mínimo de backend:

    1. Ingestão de normas (PDF/TXT) → `backend.ingestion.ingest`;
    2. Estruturação em artigos → `backend.structure.structure`;
    3. Indexação vetorial → `backend.indexer.indexer`;
    4. Busca semântica (RAG) → `backend.rag.rag_engine`.

    Os agentes CrewAI já estão definidos em `backend.agents.*` e
    poderão ser conectados em uma etapa seguinte.
    """
)


# --- Helper: dummy embedding function (para a PoC offline) ---

def dummy_embedding(texts: List[str]) -> List[List[float]]:
    """Função de embedding simplificada para PoC.

    IMPORTANTE: Esta função NÃO produz embeddings semânticos de verdade.
    Ela existe apenas para permitir que o fluxo FAISS funcione estruturalmente
    sem depender de um provedor externo de embeddings.

    Em produção, substitua por algo como:
    - OpenAI embeddings;
    - Sentence-Transformers;
    - Outro provedor de sua preferência.
    """
    vectors: List[List[float]] = []
    for t in texts:
        length = float(len(t))
        # Vetor 3D simples baseado no tamanho do texto
        vectors.append([length, length % 100.0, length / 100.0])
    return vectors


# --- Sessão: Upload e ingestão de norma ---

st.header("1. Upload e Ingestão de Norma")

uploaded_file = st.file_uploader("Envie uma lei/decreto/edital em PDF ou TXT", type=["pdf", "txt", "md"])

col1, col2 = st.columns(2)

with col1:
    if uploaded_file is not None:
        st.success(f"Arquivo recebido: {uploaded_file.name}")

        if st.button("Ingerir Norma"):
            # salvar temporariamente em data/uploads
            upload_dir = Path("data/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            temp_path = upload_dir / uploaded_file.name
            temp_path.write_bytes(uploaded_file.getvalue())

            raw_txt_path = ingest_norma(str(temp_path))
            st.session_state["raw_txt_path"] = raw_txt_path
            st.info(f"Texto bruto salvo em: `{raw_txt_path}`")
    else:
        st.caption("Aguardando upload de arquivo...")


# --- Sessão: Estruturação em artigos ---

st.header("2. Estruturação em Artigos")

raw_txt_path = st.session_state.get("raw_txt_path")
default_structured_path = "data/normas_structured/artigos.jsonl"

if raw_txt_path:
    st.write(f"Arquivo de texto bruto atual: `{raw_txt_path}`")

    if st.button("Estruturar Norma em Artigos"):
        structured_path = estrutura_norma(raw_txt_path, default_structured_path)
        st.session_state["structured_path"] = structured_path
        st.success(f"Artigos estruturados salvos em: `{structured_path}`")
else:
    st.caption("Nenhuma norma ingerida ainda.")


# --- Sessão: Indexação Vetorial ---

st.header("3. Indexação Vetorial FAISS")

structured_path = st.session_state.get("structured_path")

index_path = "vector_store/normas.index"
metadata_path = "vector_store/normas_metadata.json"

if structured_path:
    st.write(f"Base estruturada atual: `{structured_path}`")

    if st.button("Gerar Índice Vetorial"):
        os.makedirs("vector_store", exist_ok=True)
        idx_path, meta_path = indexar_normas(
            structured_path,
            embedding_fn=dummy_embedding,
            index_path=index_path,
            metadata_path=metadata_path,
        )
        st.session_state["index_path"] = idx_path
        st.session_state["metadata_path"] = meta_path
        st.success(f"Índice criado em: `{idx_path}`")
        st.success(f"Metadados salvos em: `{meta_path}`")
else:
    st.caption("Nenhuma base estruturada disponível para indexação.")


# --- Sessão: Busca Semântica (RAG simplificado) ---

st.header("4. Busca Semântica nas Normas (RAG)")

query = st.text_input("Consulta (ex.: 'regularidade fiscal', 'habilitação da empresa')")

index_ready = Path(index_path).exists() and Path(metadata_path).exists()

if not index_ready:
    st.warning("Índice e metadados ainda não foram gerados. Complete as etapas 1–3.")
else:
    if query:
        if st.button("Buscar nas Normas"):
            results = search_normas(
                query,
                embedding_fn=dummy_embedding,
                index_path=index_path,
                metadata_path=metadata_path,
                k=5,
            )

            if not results:
                st.info("Nenhum resultado encontrado.")
            else:
                st.subheader("Resultados:")
                for r in results:
                    with st.expander(f"{r['id']} - {r['label']} (score={r['score']:.2f})"):
                        st.write(r["text"])
    else:
        st.caption("Digite uma consulta para testar a busca.")


st.divider()
st.caption(
    "Backend: ingestão, estruturação, indexação e RAG já operacionais. "
    "Próximo passo: conectar os agentes CrewAI (`backend.agents`) para "
    "gerar pareceres de aderência a partir dessa base."
)
