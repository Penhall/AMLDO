"""
RAG v3 - Wrapper para compatibilidade com Google ADK.

Este módulo serve como ponto de entrada para o Google ADK descobrir
o agente RAG v3 com similarity search.
"""

from amldo.rag.v3.agent import root_agent

__all__ = ["root_agent"]
