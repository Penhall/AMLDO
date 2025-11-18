"""
FastAPI Application para AMLDO.

API REST para consultas RAG, upload e processamento de documentos.

Versão: 0.3.0
"""

from pathlib import Path
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from amldo.core.config import settings
from amldo.interfaces.api.routers import query, upload, metrics

# Criar aplicação FastAPI
app = FastAPI(
    title="AMLDO API",
    description=(
        "API REST para sistema RAG especializado em licitações, "
        "compliance e governança baseado em legislação brasileira"
    ),
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminhos para templates e arquivos estáticos
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Configurar templates Jinja2
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Montar arquivos estáticos
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Incluir routers
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(upload.router, prefix="/api", tags=["Upload & Processing"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])


# =============================================================================
# Rotas de Páginas HTML
# =============================================================================


@app.get("/", response_class=HTMLResponse, summary="Página inicial")
async def root(request: Request):
    """
    Página inicial da aplicação.

    Renderiza index.html com links para as principais funcionalidades.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/consulta", response_class=HTMLResponse, summary="Página de consulta")
async def consulta_page(request: Request):
    """
    Página de consulta RAG.

    Interface web para fazer perguntas ao sistema.
    """
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/processamento", response_class=HTMLResponse, summary="Página de processamento")
async def processamento_page(request: Request):
    """
    Página de processamento de documentos.

    Interface web para upload e processamento de PDFs.
    """
    return templates.TemplateResponse("process.html", {"request": request})


# =============================================================================
# Eventos de Lifecycle
# =============================================================================


@app.on_event("startup")
async def startup_event():
    """
    Executado quando a aplicação inicia.

    Cria diretórios necessários se não existirem.
    """
    # Criar diretórios necessários
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/vector_db").mkdir(parents=True, exist_ok=True)
    Path("data/metrics").mkdir(parents=True, exist_ok=True)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("🚀 AMLDO API iniciada com sucesso!")
    print(f"📊 Documentação: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"🔍 ReDoc: http://{settings.api_host}:{settings.api_port}/redoc")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado quando a aplicação é encerrada.
    """
    print("👋 AMLDO API encerrada")


# =============================================================================
# Health Check
# =============================================================================


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Verifica se a API está funcionando.

    **Retorna:**
    - status: "ok"
    - version: Versão da API
    - rag_versions: Versões RAG disponíveis
    """
    return {
        "status": "ok",
        "version": "0.3.0",
        "service": "AMLDO API",
        "rag_versions": ["v1", "v2", "v3"],
        "default_rag_version": settings.default_rag_version,
    }


# =============================================================================
# Tratamento de Erros
# =============================================================================


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handler para 404 Not Found."""
    return templates.TemplateResponse(
        "index.html",  # Pode criar uma página 404.html depois
        {"request": request, "error": "Página não encontrada"},
        status_code=404,
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handler para 500 Internal Server Error."""
    return {
        "error": "Internal Server Error",
        "detail": "Ocorreu um erro interno no servidor",
        "status_code": 500,
    }
