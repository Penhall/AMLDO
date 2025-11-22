"""
RAG v3 - Similarity Search Variant

Versão experimental do RAG usando similarity search ao invés de MMR.
"""

from . import agent
from .tools import consultar_base_rag

__all__ = ["agent", "consultar_base_rag"]
