
"""Agente responsável pelo UC06 - Avaliar Aderência por Critério (Regra + RAG)."""

from typing import Any, List, Optional
from .base_agent import BaseCrewAgent


def create_compliance_agent(
    llm: Optional[Any] = None,
    tools: Optional[List[Any]] = None,
) -> BaseCrewAgent:
    return BaseCrewAgent(
        name="compliance_agent",
        role="Avaliador de Aderência em Licitações",
        goal=(
            "Avaliar de forma fundamentada se a empresa atende aos requisitos do edital, "
            "indicando pontos fortes, pendências e riscos de inabilitação."
        ),
        backstory=(
            "Você atua como um analista jurídico especializado em licitações, combinando "
            "interpretação legal com análise de documentos da empresa."
        ),
        tools=tools or [],
        llm=llm,
    )
