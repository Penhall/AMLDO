"""
App principal Streamlit para AMLDO.

Interface web integrada que fornece acesso a:
- Pipeline de processamento de documentos
- Consultas RAG
- Visualização de resultados
"""

import streamlit as st

st.set_page_config(
    page_title="AMLDO - Sistema de Análise de Licitações",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📚 AMLDO - Sistema de Análise de Licitações")

st.markdown(
    """
    Sistema RAG especializado em licitações, compliance e governança baseado em legislação brasileira.

    **Selecione uma página no menu lateral:**
    - **Pipeline**: Processe novos documentos (upload → estrutura → índice)
    - **RAG Query**: Consulte a base de conhecimento existente
    - **Home**: Esta página
    """
)

st.divider()

st.subheader("Sobre o AMLDO")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        ### Funcionalidades

        - ✅ **RAG v1 e v2**: Consultas com contexto hierárquico
        - ✅ **Pipeline de processamento**: Ingestion → Structure → Index
        - ✅ **Embeddings reais**: sentence-transformers multilíngue
        - ✅ **Base pré-processada**: Lei 14.133, Lei 13.709, LCP 123, Decreto 10.024
        - ⚙️ **Agentes CrewAI**: Sistema multi-agente (em desenvolvimento)
        """
    )

with col2:
    st.markdown(
        """
        ### Arquitetura

        - **LLM**: Gemini 2.5 Flash
        - **Embeddings**: paraphrase-multilingual-MiniLM-L12-v2
        - **Vector Store**: FAISS (12 docs, MMR search)
        - **Framework**: Google ADK + LangChain
        - **Interface**: Streamlit
        """
    )

st.divider()

st.info(
    """
    💡 **Dica**: Use o menu lateral para navegar entre as páginas.

    - Para processar novos documentos, vá para **Pipeline**
    - Para fazer consultas, vá para **RAG Query**
    """
)


def main():
    """Entry point para executar via command line."""
    pass


if __name__ == "__main__":
    main()
