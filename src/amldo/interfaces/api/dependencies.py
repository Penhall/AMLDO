"""
Dependências compartilhadas da API FastAPI.

Funções de dependência para injeção no FastAPI.
"""

from typing import Annotated
from fastapi import Depends

from amldo.core.config import Settings, settings


def get_settings() -> Settings:
    """
    Retorna as configurações globais do sistema.

    Returns:
        Settings: Objeto de configurações pydantic-settings
    """
    return settings


# Type alias para injeção de dependência
SettingsDep = Annotated[Settings, Depends(get_settings)]
