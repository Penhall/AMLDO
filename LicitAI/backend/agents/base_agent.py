
from dataclasses import dataclass, field
from typing import Any, List, Optional

try:
    # crewai é opcional em ambiente local.
    from crewai import Agent as CrewAgent
except ImportError:  # pragma: no cover
    CrewAgent = Any  # type: ignore


@dataclass
class BaseCrewAgent:
    """Agente base customizado para a PoC de Licitações.

    Este wrapper existe para:
    - padronizar metadados (nome, papel, objetivo, backstory)
    - centralizar configuração de LLM e ferramentas
    - permitir log/telemetria futura num único ponto
    """

    name: str
    role: str
    goal: str
    backstory: str
    tools: List[Any] = field(default_factory=list)
    llm: Optional[Any] = None
    verbose: bool = True

    def build(self) -> Any:
        """Constrói uma instância crewai.Agent real a partir desta configuração."""
        if CrewAgent is Any:
            raise ImportError(
                "crewai não está instalado. "
                "Instale com `pip install crewai` para usar os agentes."
            )

        return CrewAgent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            llm=self.llm,
            verbose=self.verbose,
        )

    @classmethod
    def from_config(cls, name: str, config: dict) -> "BaseCrewAgent":
        return cls(
            name=name,
            role=config.get("role", ""),
            goal=config.get("goal", ""),
            backstory=config.get("backstory", ""),
            tools=config.get("tools", []),
            llm=config.get("llm"),
            verbose=config.get("verbose", True),
        )
