
"""Agente responsável pelo UC04 - Cadastrar Empresa e Enviar Documentos."""

from typing import Any, List, Optional
from .base_agent import BaseCrewAgent


def create_company_docs_agent(
    llm: Optional[Any] = None,
    tools: Optional[List[Any]] = None,
) -> BaseCrewAgent:
    return BaseCrewAgent(
        name="company_docs_agent",
        role="Leitor de Documentos do Concorrente",
        goal=(
            "Transformar os documentos enviados pela empresa licitante em um "
            "perfil estruturado que possa ser comparado com os requisitos do edital."
        ),
        backstory=(
            "Você é especialista em interpretar documentos empresariais e certidões, "
            "extraindo apenas o que é útil para análise de habilitação."
        ),
        tools=tools or [],
        llm=llm,
    )
