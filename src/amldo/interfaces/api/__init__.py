"""
API REST FastAPI para AMLDO.

Interface web para consultas RAG, upload de documentos e métricas.
"""

from .main import app

__all__ = ["app"]
