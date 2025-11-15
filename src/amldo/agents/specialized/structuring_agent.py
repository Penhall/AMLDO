
"""Agente responsável pelo UC02 - Estruturar e Consolidar Artigos."""

from typing import Any, List, Optional
from .base_agent import BaseCrewAgent


def create_structuring_agent(
    llm: Optional[Any] = None,
    tools: Optional[List[Any]] = None,
) -> BaseCrewAgent:
    return BaseCrewAgent(
        name="structuring_agent",
        role="Organizador de Corpus Jurídico",
        goal=(
            "Transformar o texto bruto das normas em uma base estruturada, "
            "com artigos e metadados prontos para indexação."
        ),
        backstory=(
            "Você conhece a organização típica de leis brasileiras e é capaz de "
            "identificar cabeçalhos, numeração de artigos e hierarquia de capítulos."
        ),
        tools=tools or [],
        llm=llm,
    )
