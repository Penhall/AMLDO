
"""Agente responsável pelo UC03 - Indexar Base Vetorial."""

from typing import Any, List, Optional
from .base_agent import BaseCrewAgent


def create_indexing_agent(
    llm: Optional[Any] = None,
    tools: Optional[List[Any]] = None,
) -> BaseCrewAgent:
    return BaseCrewAgent(
        name="indexing_agent",
        role="Engenheiro de Busca Jurídica",
        goal=(
            "Criar e manter índices vetoriais eficientes que permitam "
            "busca semântica rápida e precisa sobre as normas."
        ),
        backstory=(
            "Você pensa em termos de similaridade semântica e performance de busca. "
            "Seu trabalho garante que consultas complexas possam ser respondidas rapidamente."
        ),
        tools=tools or [],
        llm=llm,
    )
