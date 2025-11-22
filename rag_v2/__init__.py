"""
RAG v2 - Wrapper para compatibilidade com Google ADK.

Este módulo serve como ponto de entrada para o Google ADK descobrir
o agente RAG v2 com contexto hierárquico.
"""

from amldo.rag.v2.agent import root_agent

__all__ = ["root_agent"]
