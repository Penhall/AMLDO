# =============================================================================
# AMLDO - Dockerfile Multi-stage
# Sistema RAG para Legislação de Licitações
# Versão: 0.3.0
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Base - Dependências comuns
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS base

LABEL maintainer="AMLDO Team"
LABEL version="0.3.0"
LABEL description="Sistema RAG para licitações públicas e compliance"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Criar usuário não-root
RUN useradd -m -u 1000 amldo

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml README.md ./
COPY requirements/ requirements/

# Atualizar pip
RUN pip install --upgrade pip setuptools wheel

# -----------------------------------------------------------------------------
# Stage 2: FastAPI
# -----------------------------------------------------------------------------
FROM base AS fastapi

# Instalar dependências para FastAPI
RUN pip install -r requirements/base.txt

# Copiar código fonte
COPY --chown=amldo:amldo src/ src/
COPY --chown=amldo:amldo data/ data/

# Instalar pacote
RUN pip install -e .

# Criar diretórios necessários
RUN mkdir -p data/raw data/processed data/vector_db data/metrics logs \
    && chown -R amldo:amldo data/ logs/

# Trocar para usuário não-root
USER amldo

# Expor porta
EXPOSE 8000

# Variáveis de ambiente
ENV API_HOST=0.0.0.0 \
    API_PORT=8000 \
    ENVIRONMENT=production

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando
CMD ["python", "-m", "amldo.interfaces.api.run"]

# -----------------------------------------------------------------------------
# Stage 3: Streamlit
# -----------------------------------------------------------------------------
FROM base AS streamlit

# Instalar dependências para Streamlit
RUN pip install -r requirements/base.txt \
    && pip install streamlit

# Copiar código fonte
COPY --chown=amldo:amldo src/ src/
COPY --chown=amldo:amldo data/ data/

# Instalar pacote
RUN pip install -e .

# Criar diretórios necessários
RUN mkdir -p data/raw data/processed data/vector_db logs \
    && chown -R amldo:amldo data/ logs/

# Trocar para usuário não-root
USER amldo

# Expor porta
EXPOSE 8501

# Variáveis de ambiente
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    ENVIRONMENT=production

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando
CMD ["streamlit", "run", "src/amldo/interfaces/streamlit/app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]

# -----------------------------------------------------------------------------
# Stage 4: Google ADK
# -----------------------------------------------------------------------------
FROM base AS adk

# Instalar dependências para ADK (mais pesado)
RUN pip install -r requirements/base.txt \
    && pip install google-adk

# Copiar código fonte
COPY --chown=amldo:amldo src/ src/
COPY --chown=amldo:amldo data/ data/
COPY --chown=amldo:amldo rag_v1/ rag_v1/
COPY --chown=amldo:amldo rag_v2/ rag_v2/
COPY --chown=amldo:amldo rag_v3/ rag_v3/

# Instalar pacote
RUN pip install -e .

# Criar diretórios necessários
RUN mkdir -p data/raw data/processed data/vector_db logs \
    && chown -R amldo:amldo data/ logs/

# Trocar para usuário não-root
USER amldo

# Expor porta
EXPOSE 8080

# Variáveis de ambiente
ENV ENVIRONMENT=production

# Comando
CMD ["adk", "web", "--port", "8080", "--host", "0.0.0.0"]

# -----------------------------------------------------------------------------
# Stage 5: Desenvolvimento (todas as interfaces)
# -----------------------------------------------------------------------------
FROM base AS dev

# Instalar TODAS as dependências
RUN pip install -r requirements/base.txt \
    && pip install streamlit google-adk \
    && pip install -r requirements/dev.txt || true

# Copiar todo o código
COPY --chown=amldo:amldo . .

# Instalar pacote
RUN pip install -e .

# Criar diretórios
RUN mkdir -p data/raw data/processed data/vector_db data/metrics logs \
    && chown -R amldo:amldo data/ logs/

# Expor todas as portas
EXPOSE 8000 8501 8080

# Variáveis de ambiente
ENV ENVIRONMENT=development

# Comando padrão
CMD ["python", "scripts/run.py"]

# =============================================================================
# Build Instructions:
#
# Build específico:
#   docker build --target fastapi -t amldo-api:latest .
#   docker build --target streamlit -t amldo-streamlit:latest .
#   docker build --target adk -t amldo-adk:latest .
#   docker build --target dev -t amldo-dev:latest .
#
# Ou use docker-compose (recomendado):
#   docker-compose up -d
#   docker-compose up fastapi
#   docker-compose up streamlit
#   docker-compose up adk
# =============================================================================
