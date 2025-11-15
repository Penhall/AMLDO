"""
Exceções customizadas do AMLDO.

Define hierarquia de exceções para facilitar tratamento de erros específicos.
"""


class AMLDOException(Exception):
    """Exceção base para todos os erros do AMLDO."""

    pass


# =============================================================================
# Exceções de Configuração
# =============================================================================


class ConfigurationError(AMLDOException):
    """Erro de configuração (variáveis de ambiente, paths, etc)."""

    pass


class MissingAPIKeyError(ConfigurationError):
    """API key obrigatória não foi fornecida."""

    pass


class InvalidPathError(ConfigurationError):
    """Path fornecido não existe ou é inválido."""

    pass


# =============================================================================
# Exceções de Pipeline
# =============================================================================


class PipelineError(AMLDOException):
    """Erro genérico no pipeline de processamento."""

    pass


class IngestionError(PipelineError):
    """Erro na ingestão de documentos (leitura de PDF/TXT)."""

    pass


class StructureError(PipelineError):
    """Erro na estruturação de documentos (extração de artigos)."""

    pass


class IndexingError(PipelineError):
    """Erro na criação de índices vetoriais."""

    pass


class EmbeddingError(PipelineError):
    """Erro na geração de embeddings."""

    pass


# =============================================================================
# Exceções de RAG
# =============================================================================


class RAGError(AMLDOException):
    """Erro genérico no sistema RAG."""

    pass


class VectorStoreError(RAGError):
    """Erro ao carregar ou consultar vector store."""

    pass


class RetrievalError(RAGError):
    """Erro na recuperação de documentos."""

    pass


class LLMError(RAGError):
    """Erro na chamada ao LLM."""

    pass


# =============================================================================
# Exceções de Agentes
# =============================================================================


class AgentError(AMLDOException):
    """Erro genérico em agentes."""

    pass


class AgentOrchestratorError(AgentError):
    """Erro no orquestrador de agentes."""

    pass


class AgentExecutionError(AgentError):
    """Erro na execução de um agente específico."""

    pass


# =============================================================================
# Exceções de Validação
# =============================================================================


class ValidationError(AMLDOException):
    """Erro de validação de dados."""

    pass


class DocumentValidationError(ValidationError):
    """Erro na validação de documentos."""

    pass


class MetadataValidationError(ValidationError):
    """Erro na validação de metadados."""

    pass
