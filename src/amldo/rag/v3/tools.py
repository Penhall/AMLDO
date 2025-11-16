"""
RAG v3 - Tools com similarity search.

Implementação experimental do RAG que:
- Usa similarity search ao invés de MMR (configurável)
- Busca documentos relevantes no FAISS
- Filtra artigo_0.txt da retrieval
- Reorganiza contexto hierarquicamente: Lei → Título → Capítulo → Artigo
- Injeta "artigo 0" (introduções de capítulos/títulos) do CSV
- Produz estrutura XML clara para o LLM

Diferença vs RAG v2: search_type default é "similarity" ao invés de "mmr"
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

# Parâmetros do RAG v3 (vêm de settings)
K = settings.rag_v3_k
SEARCH_TYPE = settings.rag_v3_search_type

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
        search_type: Tipo de busca ("similarity", "mmr", etc)
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
        resultados = "\n".join(resultados["texto"].tolist())
        return resultados
    return None


def get_pos_processed_context(df_resultados: pd.DataFrame, df_art_0: pd.DataFrame) -> str:
    """
    Pós-processa contexto recuperado, organizando hierarquicamente.

    Estrutura de saída:
        <LEI L14133>
          [artigo 0 do título se houver]
          <TITULO: TITULO_II>
            [artigo 0 do capítulo se houver]
            <CAPITULO: CAPITULO_III>
              <ARTIGO: artigo_15>
                [texto do chunk]
              </ARTIGO: artigo_15>
            </CAPITULO: CAPITULO_III>
          </TITULO: TITULO_II>
        </LEI L14133>

    Args:
        df_resultados: DataFrame com resultados da busca
        df_art_0: DataFrame com artigos 0

    Returns:
        Contexto formatado em XML
    """
    df_cap = df_resultados[["lei", "titulo", "capitulo"]].drop_duplicates().reset_index(drop=True)
    context = ""

    for law in df_cap["lei"].unique():
        context += f"\n\n<LEI {law}>\n"
        df_law = df_cap[df_cap["lei"] == law].copy()

        for title in df_law["titulo"].unique():
            # Artigo 0 do título (se houver)
            art_0 = get_art_0(law, title, "CAPITULO_0", df_art_0)
            if art_0:
                context += f"{art_0}\n"

            if title != "TITULO_0":
                context += f"<TITULO: {title}>\n"

            df_title = df_law[df_law["titulo"] == title].copy()

            for chapter in df_title["capitulo"].unique():
                # Artigo 0 do capítulo (se houver)
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

    # Limpeza de formatação
    return context.replace("\n[[SECTION:", "[[SECTION:")


def _rag_answer(question: str, search_type: str = SEARCH_TYPE, k: int = K) -> str:
    """
    Pipeline RAG v3 completo: busca contexto no FAISS e gera resposta.

    Workflow:
        1. Busca documentos relevantes (similarity search)
        2. Filtra e ordena resultados
        3. Pós-processa contexto hierarquicamente
        4. Gera resposta com LLM

    Args:
        question: Pergunta do usuário
        search_type: Tipo de busca (similarity, mmr)
        k: Número de documentos a recuperar

    Returns:
        Resposta gerada pelo LLM

    Raises:
        RetrievalError: Se falhar na busca
        LLMError: Se falhar na geração de resposta
    """
    try:
        # 1. Buscar documentos
        retriever = _get_retriever(search_type=search_type, k=k)
        contexto = retriever.invoke(question)

        # 2. Extrair e estruturar resultados
        linhas = []
        for doc in contexto:
            linhas.append({"texto": doc.page_content, **doc.metadata})

        # 3. Ordenar hierarquicamente
        df_resultados = pd.DataFrame(linhas).sort_values(
            ["lei", "titulo", "capitulo", "artigo", "chunk_idx"]
        ).reset_index(drop=True)

        # 4. Pós-processar contexto
        context = get_pos_processed_context(df_resultados, df_art_0)

        # 5. Criar prompt
        prompt = ChatPromptTemplate.from_template(
            "Use APENAS o contexto para responder.\n\n"
            "<Contexto>:\n{context}\n</Contexto>\n\n"
            "<Pergunta>:\n{question}</Pergunta>\n\n"
        )

        # 6. Executar chain
        rag_chain = (
            {"question": RunnablePassthrough(), "context": lambda _: context}
            | prompt
            | llm
            | StrOutputParser()
        )

        resposta = rag_chain.invoke(question)
        return resposta

    except Exception as e:
        if "retriever" in str(e).lower() or "faiss" in str(e).lower():
            raise RetrievalError(f"Erro ao buscar documentos: {e}") from e
        else:
            raise LLMError(f"Erro ao gerar resposta: {e}") from e


def consultar_base_rag(pergunta: str) -> str:
    """
    Retorna uma resposta baseada EXCLUSIVAMENTE nos documentos internos indexados
    na base vetorial FAISS (com embeddings multilíngues).

    **RAG v3** usa similarity search por padrão (configurável via settings).

    Use esta função quando a dúvida envolver:
    - licitação, dispensa de licitação por valor, contratos, governança, compliance,
      regulatório, normas internas, leis, decretos, portarias etc.;
    - perguntas do tipo "com base nos documentos", "na nossa base", "na legislação interna".

    Args:
        pergunta (str): Pergunta completa do usuário em linguagem natural.
                        Passe o texto inteiro, sem resumir.

    Returns:
        str: Texto de resposta gerado a partir do contexto recuperado.
             Se não existir contexto relevante, a resposta pode indicar
             que não encontrou informação na base.

    Raises:
        RetrievalError: Se falhar na busca de documentos
        LLMError: Se falhar na geração de resposta

    Example:
        >>> resposta = consultar_base_rag("Qual o limite de dispensa de licitação?")
        >>> print(resposta)
        "De acordo com a Lei 14.133/2021, o limite de dispensa..."
    """
    return _rag_answer(pergunta, search_type=SEARCH_TYPE, k=K)
