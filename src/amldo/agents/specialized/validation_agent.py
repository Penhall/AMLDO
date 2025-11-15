
"""Agente responsável pelo UC05 - Validar Integridade e Extrair Campos."""

from typing import Any, List, Optional
from .base_agent import BaseCrewAgent


def create_validation_agent(
    llm: Optional[Any] = None,
    tools: Optional[List[Any]] = None,
) -> BaseCrewAgent:
    return BaseCrewAgent(
        name="validation_agent",
        role="Validador de Documentos",
        goal=(
            "Garantir que a documentação enviada pela empresa esteja íntegra e "
            "minimamente consistente antes da análise jurídica de aderência."
        ),
        backstory=(
            "Você atua como uma barreira de qualidade, pegando problemas "
            "simples antes que o avaliador jurídico precise intervir."
        ),
        tools=tools or [],
        llm=llm,
    )
