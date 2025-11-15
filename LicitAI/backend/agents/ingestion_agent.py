
"""Agente responsável pelo UC01 - Inserir Normas (Leis/Decretos/Editais)."""

from typing import Any, List, Optional
from .base_agent import BaseCrewAgent


def create_ingestion_agent(
    llm: Optional[Any] = None,
    tools: Optional[List[Any]] = None,
) -> BaseCrewAgent:
    return BaseCrewAgent(
        name="ingestion_agent",
        role="Administrador de Corpus Jurídico",
        goal=(
            "Ingerir leis, decretos e editais em formato PDF/HTML e produzir "
            "um corpus de texto limpo, pronto para estruturação."
        ),
        backstory=(
            "Você é o responsável por garantir que toda a base normativa esteja "
            "corretamente carregada no sistema, sem perdas ou ruídos críticos."
        ),
        tools=tools or [],
        llm=llm,
    )
