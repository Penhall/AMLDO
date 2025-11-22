"""
Página RAG Query - Consultas à base de conhecimento.

Interface para consultar a base vetorial usando RAG v1 ou v2.
"""

import streamlit as st
from pathlib import Path

# Imports dos módulos RAG
from amldo.rag.v1.tools import consultar_base_rag as consultar_v1
from amldo.rag.v2.tools import consultar_base_rag as consultar_v2
from amldo.core.config import settings
from amldo.core.exceptions import RAGError
from amldo.interfaces.streamlit.theme import apply_theme

st.set_page_config(page_title="RAG Query - AMLDO", page_icon="🌿", layout="wide")

# Aplicar tema Nature
apply_theme()

st.title("🔍 Consultas RAG")

st.markdown(
    """
    Consulte a base de conhecimento sobre licitações, compliance e governança.

    **Versões disponíveis:**
    - **RAG v1**: Retrieval simples com contexto direto
    - **RAG v2**: Contexto hierárquico (Lei → Título → Capítulo → Artigo)
    """
)

# =============================================================================
# Verificação de disponibilidade
# =============================================================================

vector_db_exists = settings.vector_db_path_absolute.exists()

if not vector_db_exists:
    st.error(
        f"""
        ❌ **Vector store não encontrado!**

        Esperado em: `{settings.vector_db_path_absolute}`

        **Como resolver:**
        1. Vá para a página **Pipeline** e processe documentos
        2. Ou verifique se o path em `.env` está correto (VECTOR_DB_PATH)
        """
    )
    st.stop()

st.success(f"✅ Vector store encontrado: `{settings.vector_db_path_absolute}`")

# =============================================================================
# Seleção de versão RAG
# =============================================================================

st.divider()

col1, col2 = st.columns([1, 3])

with col1:
    rag_version = st.radio(
        "Versão RAG:",
        options=["v1", "v2"],
        index=1,  # v2 por padrão
        help="v1 = contexto simples, v2 = contexto hierárquico estruturado",
    )

with col2:
    if rag_version == "v1":
        st.info(
            """
            **RAG v1**: Busca MMR e retorna documentos diretamente ao LLM.
            Mais rápido, contexto menos estruturado.
            """
        )
    else:
        st.info(
            """
            **RAG v2**: Busca MMR + pós-processamento hierárquico.
            Organiza contexto por Lei → Título → Capítulo → Artigo.
            Injeta "artigo 0" (introduções de capítulos).
            """
        )

# =============================================================================
# Configurações de busca
# =============================================================================

st.divider()
st.subheader("Configurações de Busca")

col1, col2 = st.columns(2)

with col1:
    search_k = st.slider(
        "Número de documentos a recuperar (k)",
        min_value=1,
        max_value=30,
        value=settings.search_k,
        help="Quantos documentos mais relevantes buscar",
    )

with col2:
    st.metric("Tipo de busca", settings.search_type.upper())
    st.caption("MMR = Maximal Marginal Relevance (balanceia relevância e diversidade)")

# =============================================================================
# Interface de consulta
# =============================================================================

st.divider()
st.subheader("Faça sua Consulta")

# Exemplos de perguntas
with st.expander("💡 Ver exemplos de perguntas"):
    st.markdown(
        """
        - Quais são os valores limite para dispensa de licitação?
        - O que é pregão eletrônico segundo a Lei 14.133?
        - Quais documentos são necessários para habilitação?
        - O que diz a lei sobre contratação emergencial?
        - Como funciona o regime diferenciado de contratações (RDC)?
        """
    )

query = st.text_area(
    "Digite sua pergunta:",
    height=100,
    placeholder="Ex: Quais são os valores limite para dispensa de licitação?",
)

if st.button("🔍 Consultar", type="primary", disabled=not query):
    if not query.strip():
        st.warning("Por favor, digite uma pergunta.")
    else:
        with st.spinner(f"Consultando base de conhecimento usando RAG {rag_version}..."):
            try:
                # Seleciona função RAG baseada na versão
                consultar_fn = consultar_v1 if rag_version == "v1" else consultar_v2

                # Executa consulta
                resposta = consultar_fn(query)

                # Exibe resposta
                st.divider()
                st.subheader("📝 Resposta")

                st.markdown(resposta)

                # Metadados
                with st.expander("ℹ️ Metadados da consulta"):
                    st.json(
                        {
                            "versao_rag": rag_version,
                            "modelo_llm": settings.llm_model,
                            "modelo_embedding": settings.embedding_model,
                            "search_type": settings.search_type,
                            "k": search_k,
                            "vector_db": str(settings.vector_db_path_absolute),
                        }
                    )

            except RAGError as e:
                st.error(f"❌ Erro na consulta RAG: {e}")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")
                with st.expander("Ver detalhes do erro"):
                    st.exception(e)

# =============================================================================
# Histórico (se implementado)
# =============================================================================

st.divider()

if "query_history" not in st.session_state:
    st.session_state["query_history"] = []

if query and st.session_state.get("last_response"):
    st.session_state["query_history"].append(
        {"query": query, "response": st.session_state["last_response"], "version": rag_version}
    )

if st.session_state["query_history"]:
    with st.expander(f"📜 Histórico de consultas ({len(st.session_state['query_history'])})"):
        for idx, item in enumerate(reversed(st.session_state["query_history"][-5:]), 1):
            st.markdown(f"**{idx}. [{item['version']}]** {item['query'][:100]}...")

# =============================================================================
# Informações adicionais
# =============================================================================

st.divider()
st.caption(
    """
    💡 **Dicas:**
    - Perguntas específicas geram melhores respostas
    - RAG v2 é melhor para perguntas que requerem contexto estruturado
    - RAG v1 é mais rápido para consultas simples
    """
)
