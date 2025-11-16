"""
RAG v3 - Similarity Search Variant

Versão experimental do RAG usando similarity search ao invés de MMR.
"""

# from .agent import root_agent  # Requer Google ADK instalado
from .tools import consultar_base_rag

# Tentar importar agent se ADK estiver disponível
try:
    from .agent import root_agent
    __all__ = ["root_agent", "consultar_base_rag"]
except ImportError:
    # Google ADK não instalado - apenas exports ferramenta
    __all__ = ["consultar_base_rag"]
