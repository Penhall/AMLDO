"""
Script para executar a API FastAPI.

Uso:
    python -m amldo.interfaces.api.run
    ou
    amldo-api (após instalar o pacote)
"""

import uvicorn
from amldo.core.config import settings


def main():
    """
    Inicia o servidor Uvicorn com a aplicação FastAPI.

    Configurações vêm de settings (environment variables ou defaults).
    """
    uvicorn.run(
        "amldo.interfaces.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
