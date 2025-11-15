"""
RAG v2 - Tools com pós-processamento hierárquico de contexto.

Implementação avançada do RAG que:
- Busca documentos relevantes no FAISS (MMR search)
- Filtra artigo_0.txt da retrieval
- Reorganiza contexto hierarquicamente: Lei → Título → Capítulo → Artigo
- Injeta "artigo 0" (introduções de capítulos/títulos) do CSV
- Produz estrutura XML clara para o LLM
"""

import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

from amldo.core.config import settings
from amldo.core.exceptions import VectorStoreError, LLMError, RetrievalError


# =============================================================================
# Inicialização de Modelos e Dados
# =============================================================================

# Parâmetros do RAG (agora vêm de settings)
K = settings.search_k
SEARCH_TYPE = settings.search_type

# LLM
llm = init_chat_model(settings.llm_model, model_provider=settings.llm_provider)

# Dataframe com artigos 0 (introduções de capítulos/títulos)
try:
    df_art_0 = pd.read_csv(settings.artigos_0_csv_path_absolute)
except FileNotFoundError as e:
    raise VectorStoreError(
        f"Arquivo artigos_0 não encontrado: {settings.artigos_0_csv_path_absolute}"
    ) from e

# Modelo de embedding
modelo_embedding = HuggingFaceEmbeddings(
    model_name=settings.embedding_model,
    encode_kwargs={"normalize_embeddings": True},
)

# FAISS index já salvo em disco
try:
    vector_db = FAISS.load_local(
        str(settings.vector_db_path_absolute),
        embeddings=modelo_embedding,
        allow_dangerous_deserialization=settings.get_faiss_allow_dangerous_deserialization(),
    )
except Exception as e:
    raise VectorStoreError(
        f"Falha ao carregar vector store de {settings.vector_db_path_absolute}: {e}"
    ) from e


# =============================================================================
# Funções Internas
# =============================================================================


def _get_retriever(vector_db=vector_db, search_type: str = SEARCH_TYPE, k: int = K):
    """
    Cria o retriever do FAISS com filtro para excluir artigo_0.txt.

    Args:
        vector_db: Instância do FAISS vector store
        search_type: Tipo de busca ("mmr", "similarity", etc)
        k: Número de documentos a recuperar

    Returns:
        Retriever configurado
    """
    return vector_db.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k, "filter": {"artigo": {"$nin": ["artigo_0.txt"]}}},
    )


def get_art_0(law: str, title: str, chapter: str, df_art_0: pd.DataFrame) -> str | None:
    """
    Obtém o texto do artigo 0 correspondente (introdução de capítulo/título).

    Args:
        law: Lei (ex: "L14133")
        title: Título (ex: "TITULO_II")
        chapter: Capítulo (ex: "CAPITULO_III")
        df_art_0: DataFrame com artigos 0

    Returns:
        Texto do artigo 0 ou None se não encontrado
    """
    cond = (df_art_0["lei"] == law) & (df_art_0["titulo"] == title) & (df_art_0["capitulo"] == chapter)
    resultados = df_art_0[cond]
    if resultados.shape[0] > 0:
        return "\n".join(resultados["texto"].tolist())
    return None


def get_pos_processed_context(df_resultados: pd.DataFrame, df_art_0: pd.DataFrame) -> str:
    """
    Pós-processa o contexto recuperado, organizando hierarquicamente.

    Estrutura gerada:
    <LEI L14133>
      <TITULO: TITULO_II>
        <CAPITULO: CAPITULO_III>
          <ARTIGO: artigo_15>
            [texto do artigo]
          </ARTIGO>
        </CAPITULO>
      </TITULO>
    </LEI>

    Args:
        df_resultados: DataFrame com documentos recuperados
        df_art_0: DataFrame com artigos 0 (introduções)

    Returns:
        String com contexto hierarquicamente estruturado
    """
    df_cap = df_resultados[["lei", "titulo", "capitulo"]].drop_duplicates().reset_index(drop=True)
    context = ""

    for law in df_cap["lei"].unique():
        context += f"\n\n<LEI {law}>\n"
        df_law = df_cap[df_cap["lei"] == law].copy()

        for title in df_law["titulo"].unique():
            # Artigo 0 no nível de título
            art_0 = get_art_0(law, title, "CAPITULO_0", df_art_0)
            if art_0:
                context += f"{art_0}\n"

            if title != "TITULO_0":
                context += f"<TITULO: {title}>\n"

            df_title = df_law[df_law["titulo"] == title].copy()

            for chapter in df_title["capitulo"].unique():
                # Artigo 0 no nível de capítulo
                art_0 = get_art_0(law, title, chapter, df_art_0)
                if art_0:
                    context += f"{art_0}\n"

                if chapter != "CAPITULO_0":
                    context += f"<CAPITULO: {chapter}>\n"

                # Filtrar artigos deste capítulo
                cond_lei = df_resultados["lei"] == law
                cond_titulo = df_resultados["titulo"] == title
                cond_capitulo = df_resultados["capitulo"] == chapter
                mask = cond_lei & cond_titulo & cond_capitulo
                df_chapter = df_resultados[mask].copy()

                for artigo in df_chapter["artigo"].unique():
                    df_article = df_chapter[df_chapter["artigo"] == artigo].copy()
                    context += f'<ARTIGO: {artigo.replace(".txt", "")}>\n'
                    for _, row in df_article.iterrows():
                        context += f"{row['texto']}\n"
                    context += f'</ARTIGO: {artigo.replace(".txt", "")}>\n'

                if chapter != "CAPITULO_0":
                    context += f"</CAPITULO: {chapter}>\n"

            if title != "TITULO_0":
                context += f"</TITULO: {title}>\n"

        context += f"</LEI {law}>\n"

    return context.replace("\n[[SECTION:", "[[SECTION:")


def _rag_answer(question: str, search_type: str = SEARCH_TYPE, k: int = K) -> str:
    """
    Pipeline RAG v2 com pós-processamento hierárquico.

    Args:
        question: Pergunta do usuário
        search_type: Tipo de busca
        k: Número de docs a recuperar

    Returns:
        Resposta gerada pelo LLM

    Raises:
        RetrievalError: Se falhar ao recuperar documentos
        LLMError: Se falhar ao gerar resposta
    """
    try:
        retriever = _get_retriever(search_type=search_type, k=k)
        contexto = retriever.invoke(question)
    except Exception as e:
        raise RetrievalError(f"Falha ao recuperar documentos: {e}") from e

    # Separação dos resultados do retriever
    linhas = []
    for doc in contexto:
        linhas.append({"texto": doc.page_content, **doc.metadata})

    # Ordenação dos resultados hierarquicamente
    df_resultados = pd.DataFrame(linhas).sort_values(
        ["lei", "titulo", "capitulo", "artigo", "chunk_idx"]
    ).reset_index(drop=True)

    # Pós-processamento do contexto
    context = get_pos_processed_context(df_resultados, df_art_0)

    prompt = ChatPromptTemplate.from_template(
        "Use APENAS o contexto para responder.\n\n"
        f"<Contexto>:\n{context}\n</Contexto>\n\n"
        "<Pergunta>:\n{question}</Pergunta>\n\n"
    )

    rag_chain = {"question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    try:
        resposta = rag_chain.invoke(question)
        return resposta
    except Exception as e:
        raise LLMError(f"Falha ao gerar resposta: {e}") from e


# =============================================================================
# Ferramenta Pública (Tool para Google ADK)
# =============================================================================


def consultar_base_rag(pergunta: str) -> str:
    """
    Retorna uma resposta baseada EXCLUSIVAMENTE nos documentos internos indexados
    na base vetorial FAISS (com embeddings multilíngues).

    Versão v2 com pós-processamento hierárquico de contexto.

    Use esta função quando a dúvida envolver:
    - licitação, dispensa de licitação por valor, contratos, governança, compliance,
      regulatório, normas internas, leis, decretos, portarias etc.;
    - perguntas do tipo "com base nos documentos", "na nossa base", "na legislação interna".

    Args:
        pergunta (str): Pergunta completa do usuário em linguagem natural.
                        Passe o texto inteiro, sem resumir.

    Returns:
        str: Texto de resposta gerado a partir do contexto recuperado e estruturado.
             Se não existir contexto relevante, a resposta pode indicar
             que não encontrou informação na base.

    Raises:
        RetrievalError: Se falhar ao recuperar documentos
        LLMError: Se falhar ao gerar resposta
    """
    return _rag_answer(pergunta, search_type=SEARCH_TYPE, k=K)
