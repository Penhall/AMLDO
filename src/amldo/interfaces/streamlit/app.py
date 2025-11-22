"""
App principal Streamlit para AMLDO.

Interface web integrada com tema Chat ONN (claro/roxo).
Fornece acesso a:
- Pipeline de processamento de documentos
- Consultas RAG
- Visualização de resultados
"""

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="AMLDO Streamlit | Sistema RAG",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Importar e aplicar tema Chat ONN
from amldo.interfaces.streamlit.theme import apply_theme
apply_theme()

# Header customizado estilo Chat ONN
st.markdown("""
<div class="chat-onn-header">
    <h1>💜 AMLDO Streamlit</h1>
    <p>Sistema RAG para Legislação de Licitações</p>
    <span class="chat-onn-badge">Chat ONN Theme</span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    Interface web com tema **Chat ONN** - claro, moderno e intuitivo.

    **Navegue pelo menu lateral:**
    - **Pipeline**: Processe novos documentos (upload → estrutura → índice)
    - **RAG Query**: Consulte a base de conhecimento existente
    """
)

st.divider()

# Conteúdo principal em cards
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Funcionalidades")
    st.markdown(
        """
        - **RAG v1 e v2**: Consultas com contexto hierárquico
        - **Pipeline completo**: Ingestion → Structure → Index
        - **Embeddings reais**: sentence-transformers multilíngue
        - **Base pré-processada**: Lei 14.133, Lei 13.709, LCP 123, Decreto 10.024
        - **Agentes CrewAI**: Sistema multi-agente (em desenvolvimento)
        """
    )

with col2:
    st.subheader("🏛️ Arquitetura")
    st.markdown(
        """
        - **LLM**: Gemini 2.5 Flash
        - **Embeddings**: paraphrase-multilingual-MiniLM-L12-v2
        - **Vector Store**: FAISS (12 docs, MMR search)
        - **Framework**: Google ADK + LangChain
        - **Interface**: Streamlit + Chat ONN Theme
        """
    )

st.divider()

# Info box
st.info(
    """
    **💡 Dica**: Use o menu lateral para navegar entre as páginas.

    - Para processar novos documentos, vá para **Pipeline**
    - Para fazer consultas, vá para **RAG Query**
    """
)

# Métricas estilo Chat ONN
st.subheader("📊 Status do Sistema")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Documentos", "4", help="Leis indexadas na base")

with col2:
    st.metric("Artigos", "500+", help="Total de artigos processados")

with col3:
    st.metric("RAG Version", "v2", help="Versão recomendada")

with col4:
    st.metric("Status", "Online", delta="OK")

# Footer
st.divider()
st.caption(
    """
    AMLDO v0.3.0 | Streamlit + Chat ONN Theme |
    Sistema RAG especializado em licitações, compliance e governança.
    """
)


def main():
    """Entry point para executar via command line."""
    pass


if __name__ == "__main__":
    main()
