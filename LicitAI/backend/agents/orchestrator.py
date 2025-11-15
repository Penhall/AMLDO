
"""Módulo de orquestração dos agentes CrewAI da PoC de Licitações."""

from typing import Any, Dict, List, Optional

from .base_agent import BaseCrewAgent
from .ingestion_agent import create_ingestion_agent
from .structuring_agent import create_structuring_agent
from .indexing_agent import create_indexing_agent
from .company_docs_agent import create_company_docs_agent
from .validation_agent import create_validation_agent
from .compliance_agent import create_compliance_agent


def build_all_agents(
    llm: Optional[Any] = None,
    shared_tools: Optional[List[Any]] = None,
) -> Dict[str, BaseCrewAgent]:
    tools = shared_tools or []

    agents: Dict[str, BaseCrewAgent] = {
        "ingestion": create_ingestion_agent(llm=llm, tools=tools),
        "structuring": create_structuring_agent(llm=llm, tools=tools),
        "indexing": create_indexing_agent(llm=llm, tools=tools),
        "company_docs": create_company_docs_agent(llm=llm, tools=tools),
        "validation": create_validation_agent(llm=llm, tools=tools),
        "compliance": create_compliance_agent(llm=llm, tools=tools),
    }

    return agents
