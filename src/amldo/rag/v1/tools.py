"""
RAG v1 - Tools para consulta à base de conhecimento.

Implementação básica do RAG que:
- Busca documentos relevantes no FAISS (MMR search)
- Retorna contexto direto para o LLM
- Sem pós-processamento hierárquico
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

from amldo.core.config import settings
from amldo.core.exceptions import VectorStoreError, LLMError, RetrievalError


# =============================================================================
# Inicialização de Modelos
# =============================================================================

# LLM usado dentro do RAG
_llm_kwargs: dict = {}
if settings.llm_provider == "google_genai":
    _llm_kwargs["google_api_key"] = settings.google_api_key

llm = init_chat_model(settings.llm_model, model_provider=settings.llm_provider, **_llm_kwargs)

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


def _get_retriever(vector_db=vector_db, search_type: str | None = None, k: int | None = None):
    """
    Cria o retriever do FAISS.

    Args:
        vector_db: Instância do FAISS vector store
        search_type: Tipo de busca ("mmr", "similarity", etc). Usa settings se None.
        k: Número de documentos a recuperar. Usa settings se None.

    Returns:
        Retriever configurado
    """
    search_type = search_type or settings.search_type
    k = k or settings.search_k

    return vector_db.as_retriever(search_type=search_type, search_kwargs={"k": k})


def _rag_answer(question: str, search_type: str | None = None, k: int | None = None) -> str:
    """
    Pipeline RAG básico: busca contexto no FAISS e gera resposta.

    Args:
        question: Pergunta do usuário
        search_type: Tipo de busca. Usa settings.search_type se None.
        k: Número de docs a recuperar. Usa settings.search_k se None.

    Returns:
        Resposta gerada pelo LLM baseada no contexto recuperado

    Raises:
        RetrievalError: Se falhar ao recuperar documentos
        LLMError: Se falhar ao gerar resposta
    """
    try:
        retriever = _get_retriever(search_type=search_type, k=k)
    except Exception as e:
        raise RetrievalError(f"Falha ao criar retriever: {e}") from e

    prompt = ChatPromptTemplate.from_template(
        "Use APENAS o contexto para responder.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta:\n{question}"
    )

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

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
        RetrievalError: Se falhar ao recuperar documentos
        LLMError: Se falhar ao gerar resposta
    """
    return _rag_answer(pergunta, search_type=settings.search_type, k=settings.search_k)
